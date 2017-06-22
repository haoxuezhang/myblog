from django.contrib import admin
from .models import UserProfile, Article, Comment, Like, Category, Tag, Resource, AboutMe, Notice

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Tag)
admin.site.register(Resource)
admin.site.register(AboutMe)
admin.site.register(Notice)

