from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# from DjangoUeditor.models import UEditorField


# Create your models here.

class UserProfile(AbstractUser):
    nick_name = models.CharField('呢称', max_length=50, default='好学长')
    gender = models.CharField('性别', default='male', max_length=6, choices=(("male", "男"), ("female", "女")))
    mobile = models.CharField('手机号', max_length=11, null=True)
    image = models.ImageField(upload_to="image/%Y/%m", default="img/Logo_40.png", max_length=200, verbose_name='用户头像')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(choices=(("register", "注册"), ("forget", u"找回密码")), max_length=10, verbose_name='验证码类型')
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )

    title = models.CharField(max_length=256, verbose_name='文章标题')
    author = models.ForeignKey(UserProfile, verbose_name='作者')
    content = models.TextField('文章内容')
    # content = UEditorField(verbose_name='文章内容', width=1000, height=500, imagePath="ueditor/", filePath="ueditor/",default='')
    pub_date = models.DateTimeField(auto_now_add=True, editable=True, verbose_name='发布日期')
    update_time = models.DateTimeField(auto_now=True, null=True)
    published = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES, default='d')
    comment_num = models.IntegerField(default=0, verbose_name='评论数')
    keep_num = models.IntegerField(default=0, verbose_name='收藏数')
    recommend = models.IntegerField(default=0, verbose_name='推荐指数', help_text="默认为0，不推荐")

    abstract = models.TextField('摘要', max_length=200, help_text="可选，如若为空将摘取正文的前54个字符")
    views = models.PositiveIntegerField('浏览量', default=0)
    likes = models.PositiveIntegerField('点赞数', default=0)
    topped = models.BooleanField('置顶', default=False)

    category = models.ForeignKey('Category', verbose_name='分类', null=True, on_delete=models.SET_NULL)
    tag = models.ManyToManyField('Tag', verbose_name='标签')

    image = models.ImageField(upload_to='img/%Y/%m', verbose_name='文章配图')

    class Meta:
        verbose_name = '文章详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField('类名', max_length=20)
    intro = models.TextField('介绍', default='')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('标签名', max_length=10)
    intro = models.TextField('介绍', default='')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, null=True, verbose_name='评论用户')
    article = models.ForeignKey(Article, null=True, verbose_name='评论文章')
    content = models.TextField(verbose_name='评论内容')
    pub_date = models.DateTimeField(auto_now_add=True, editable=True, verbose_name='发布时间')
    poll_num = models.IntegerField(default=0)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class Like(models.Model):
    user = models.ForeignKey(UserProfile, null=True)
    article = models.ForeignKey(Article, null=True)
    comment = models.ForeignKey(Comment, null=True)


class Resource(models.Model):
    author = models.ForeignKey(UserProfile, verbose_name='作者')
    name = models.CharField('资源名', max_length=10)
    intro = models.TextField('介绍', default='')
    img = models.ImageField(upload_to='img/%Y/%m', verbose_name='资源配图')
    category = models.ForeignKey('Category', verbose_name='资源分类', null=True, on_delete=models.SET_NULL)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    article = models.ForeignKey(Article, null=True, verbose_name='关联的文章')
    download = models.URLField(verbose_name='下载地址', default='https://github.com/haoxuezhang')

    class Meta:
        verbose_name = '资源分享'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class AboutMe(models.Model):
    name = models.CharField('介绍描述', max_length=10)
    content = models.TextField('介绍自己的内容', default='')
    # content = UEditorField(verbose_name='介绍自己的内容', width=1000, height=500, imagePath="ueditor/", filePath="ueditor/",default='')

    blockcontent = models.TextField('介绍博客的内容', default='')
    # blockcontent = UEditorField(verbose_name='介绍博客的内容', width=1000, height=500, imagePath="ueditor/", filePath="ueditor/",default='')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '关于自己'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Notice(models.Model):
    name = models.CharField('公告描述', max_length=10)
    content = models.TextField('公告内容', default='')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class FriendLink(models.Model):
    name = models.CharField('链接名字', max_length=200);
    url = models.URLField('外链地址')
    image = models.ImageField(upload_to='img/link', verbose_name='链接配图', default="img/link/handshake.png")

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
