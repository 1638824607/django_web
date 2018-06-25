#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: liangliangyy
@license: MIT Licence 
@contact: liangliangyy@gmail.com
@site: https://www.lylinux.org/
@software: PyCharm
@file: search_indexes.py
@time: 2017/1/7 上午12:44
"""
from haystack import indexes
from blog.models import Article, Category, Tag


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        article_list = self.get_model().objects.filter(status='p')
        return article_list


"""
class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    name = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(status='p')
"""
