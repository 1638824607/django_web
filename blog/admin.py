# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.timezone import now
from django.contrib import auth
from .models import Article, Category, Tag, Links, SideBar, BlogSettings, Comment, User


class ArticleAdmin(admin.ModelAdmin):

    # 表单不展示字段
    exclude = ['created_time', 'last_mod_time', 'pub_time']

    # 列表展示字段
    list_display = (
        'title',
        'status',
        'comment_status',
        'views',
        'article_order',
        'category',
        'pub_time',
        'article_tags'     # 自定义展示字段函数1
    )

    # 增加选中集合工具
    filter_horizontal = ('tags',)

    # 添加过滤器 筛选条件
    # 字段有外键的 例如  外键字段__外键表字段 category__name
    list_filter = ('type', 'category__name', 'tags')

    # 重写模型添加和修改方法
    def save_model(self, request, obj, form, change):
        if change:
            # save
            obj.last_mod_time = now()
        else:
            # add11
            obj.created_time = now()

        if obj.status == 'p':
            obj.pub_time = now()

        import re
        # obj.body = re.sub('<[^>]+>', '', obj.body)

        from django.core.cache import cache
        cache.clear()
        super(ArticleAdmin, self).save_model(request, obj, form, change)

    # 针对多对多字段类型列表展示 ManyToManyField
    def article_tags(self, obj):
        tags = ""
        for tag in obj.tags.all():
            tags = tag.name + "," + tags
        return tags.strip(',')

    # 自定义字段显示增加表格title显示
    article_tags.short_description = '标签'


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'last_login', 'date_joined')
    list_display_links = ('id', 'username')


# 注册模型为后台展示和数据增删改查
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Links)
admin.site.register(SideBar)
admin.site.register(BlogSettings)
admin.site.register(Comment)
admin.site.register(User, UserAdmin)