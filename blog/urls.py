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

    path('page/<int:page>/', blog.ArticleListView.as_view(), name='index_page'),

    # 文章详情
    path('article_detail/<int:article_id>/', blog.ArticleDetailView.as_view(), name='article_detail'),

    # 分类列表
    path('category/<int:category_id>/', blog.CategoryDetailView.as_view(), name='category_detail'),
    path('category/<int:category_id>/<int:page>/', blog.CategoryDetailView.as_view(), name='category_detail_page'),

    # 标签详情
    path('tag_detail/<int:tag_id>', blog.TagDetailView.as_view(), name='tag_detail'),
    path('tag_detail/<int:tag_id>/<int:page>/', blog.TagDetailView.as_view(), name='tag_detail_page'),

    # 文章归档
    path('archives.html', blog.ArchivesView.as_view(), name='archives'),

    # post评论
    path('article/postcomment', blog.CommentPostView.as_view(), name='postcomment'),

    # 登出
    path('logout/', blog.LogoutView.as_view(), name='logout'),

    # 登陆
    path('login/', blog.LoginView.as_view(), name='login'),

    # 注册

    # 刷新缓存
    path('refresh/', blog.refresh_memcache, name='refreshs')
]
