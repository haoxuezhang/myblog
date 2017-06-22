from django.shortcuts import render
from django.db.models.aggregates import Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import UserProfile, Article, Category, Comment, Like, Resource, AboutMe, Tag, Notice, FriendLink, EmailVerifyRecord
from .forms import *
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password
# from markdown2 import markdown
import markdown
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .email_send import send_register_email


# Create your views here.
class IndexView(View):
    def get(self, request):
        article_list = Article.objects.filter(published='p').order_by('-pub_date')
        notice_list = Notice.objects.all().order_by('-created_time')[0:5]
        hot_list = Article.objects.all().order_by('-views')[0:15]
        share_list = Resource.objects.all().order_by('-created_time')[0:15]
        for notice in notice_list:
            notice.content = markdown.markdown(notice.content,
                                               extensions=[
                                                   'markdown.extensions.extra',
                                                   'markdown.extensions.codehilite',
                                                   'markdown.extensions.toc',
                                               ])

        category_id = request.GET.get('category', '')
        if category_id:
            article_list = article_list.filter(category_id=int(category_id))

        tag_id = request.GET.get('tag', '')
        if tag_id:
            article_list = article_list.filter(tag_id=int(tag_id))

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(article_list, 15, request=request)
        articles = p.page(page)

        context = {
            'article_list': articles,
            'notice_list': notice_list,
            'hot_list': hot_list,
            'share_list': share_list,
        }
        return render(request, 'home.html', context)


class ArticleView(View):
    def get(self, request):
        find = 0
        article_list = Article.objects.filter(published='p').order_by('-pub_date')
        tag_list = Tag.objects.annotate(num_article_tag=Count('article')).all().order_by('name')
        recommend_list = Article.objects.exclude(recommend=0).order_by('recommend')[0:20]

        category_id = request.GET.get('category', '')
        if category_id:
            article_list = article_list.filter(category_id=int(category_id))

        tag_id = request.GET.get('tag', '')
        if tag_id:
            article_list = article_list.filter(tag=int(tag_id))

        keywords = request.GET.get('keywords', '')
        if keywords:
            article_keywords = article_list.filter(Q(title__icontains=keywords) | Q(content__icontains=keywords))
            if article_list.count() <= 0:
                find = 2
            else:
                find = 1
                article_list = article_keywords

        category_list = Category.objects.annotate(num_article_category=Count('article')).all().order_by('name')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(article_list, 15, request=request)
        articles = p.page(page)

        context = {
            'article_list': articles,
            'category_list': category_list,
            'tag_list': tag_list,
            'recommend_list': recommend_list,
            'keywords': keywords,
            'find': find,
        }
        return render(request, 'article.html', context)


class ArticleDetail(View):
    def get(self, request, article_id):
        article = Article.objects.get(id=int(article_id))
        article.views += 1
        article.save()
        like_article_list = Article.objects.filter(Q(category_id=article.category_id)).exclude(id=article.id).order_by('-pub_date')[0:20]
        category_list = Category.objects.all().order_by('name')
        article.content = markdown.markdown(article.content,
                                            extensions=[
                                                'markdown.extensions.extra',
                                                'markdown.extensions.codehilite',
                                                'markdown.extensions.toc',
                                            ])
        context = {
            'article': article,
            'category_list': category_list,
            'like_article_list': like_article_list,
        }
        return render(request, 'detail.html', context)


class ResourceView(View):
    def get(self, request):
        resource_list = Resource.objects.all().order_by('-created_time')
        context = {
            'resource_list': resource_list
        }
        return render(request, 'resource.html', context)


class AboutMeView(View):
    def get(self, request):
        aboutme = AboutMe.objects.all().order_by('-created_time')[0]
        aboutme.content = markdown.markdown(aboutme.content,
                                            extensions=[
                                                'markdown.extensions.extra',
                                                'markdown.extensions.codehilite',
                                                'markdown.extensions.toc',
                                            ])
        aboutme.blockcontent = markdown.markdown(aboutme.blockcontent,
                                            extensions=[
                                                'markdown.extensions.extra',
                                                'markdown.extensions.codehilite',
                                                'markdown.extensions.toc',
                                            ])
        context = {
            'aboutme': aboutme,
        }
        return render(request, 'about.html', context)


class FriendLink(View):
    def get(self, request):
        link_list = FriendLink.objects.all().order_by('name')
        context = {
            'link_list': link_list,
        }
        return render(request, 'about.html', context)


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None



# 用户注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'login.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            user_name = request.POST.get('username', '')
            if UserProfile.objects.filter(email=email):
                return render(request, 'login.html', {"register_form": register_form, "msg": "用户已经存在"})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = email
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            send_register_email(email, "register")
            user_profile.save()
            return render(request, 'login.html', {"msg": "注册成功，请先登录邮箱激活账号"})
        else:
            return render(request, 'login.html', {"register_form": register_form, "msg": "您填入的信息不合法"})

        # 验证用户注册后，在邮件里点击注册链接

# 验证用户注册后，在邮件里点击注册链接


class ActiveUserView(View):
    def get(self, request, active_code):
        # 为什么用 filter ？ 因为用户可能注册了好多次，一个 email 对应了好多个 code
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for records in all_records:
                email = records.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, 'login.html', {"msg": "激活成功，请登录"})
        else:
            return render(request, 'login.html')

        return render(request, 'login.html')


# 用户登录
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            password = request.POST.get('password', '')
            # 上面的 authenticate 方法 return user
            user = authenticate(username=user_name, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活！'})
            else:
                return render(request, 'login.html', {'msg': '用户名或者密码错误！'})
        else:
            return render(request, 'login.html', {'form_errors': login_form.errors})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))



# 全局 404 处理函数
def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


# 全局 500 处理函数
def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response