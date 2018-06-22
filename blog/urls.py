#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: urls.py
@time: 2016/11/2 下午7:15
"""

from django.urls import path
import blog.views as blog

app_name = "blog"
urlpatterns = [
    # 文章列表
    path('', blog.ArticleListView.as_view(), name='index'),

    # 文章详情
    path('article_detail/<int:article_id>/', blog.ArticleDetailView.as_view(), name='article_detail'),

    # 分类列表
    path('category/<category_id>', blog.ArticleDetailView.as_view(), name='detail'),

    # 标签详情
    path('tag_detail/<tag_id>', blog.TagListView.as_view(), name='tag_detail'),

    # 登陆
    path('sign_in/', blog.SignInView.as_view(), name='sign_in'),

    # 注册
]
