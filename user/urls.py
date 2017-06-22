from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='article.html'), name='index'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^article$', views.ArticleView.as_view(), name='article_list'),
    url(r'^resource$', views.ResourceView.as_view(), name='resource_list'),
    url(r'^aboutme$', views.AboutMeView.as_view(), name='aboutme'),
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    url(r'^register', views.RegisterView.as_view(), name='register'),
    url(r'^article/(?P<article_id>\d+)$', views.ArticleDetail.as_view(), name='detail'),
    # url(r'^active/(?P<active_code>.*)/$', views.ArticleDetail.as_view(), name='active'),
    url(r'^active/(?P<active_code>.*)/$', views.ActiveUserView.as_view(), name='active'),
]