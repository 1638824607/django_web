# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.cache import cache
from blog.models import Article, Category, Tag
import logging


logger = logging.getLogger('shenblog')


# 列表视图基类
class BlogListView(ListView):
    # 子类重写
    def get_queryset_cache_key(self):
        raise NotImplementedError()

    # 子类重写
    def get_queryset_data(self):
        raise NotImplementedError()

    def get_queryset_from_cache(self, cache_key):
        cache_value = cache.get(cache_key)
        if(cache_value):
            # logger.info('get view cache.key:{key}'.format(key=cache_key))
            return cache_value
        else:
            cache_value = self.get_queryset_data()
            cache.set(cache_key, cache_value)
            # logger.info('set view cache.key:{key}'.format(key=cache_key))
            return cache_value

    # 获取数据
    def get_queryset(self):
        key = self.get_queryset_cache_key()
        value = self.get_queryset_from_cache(key)
        return value


# 首页面
class ArticleListView(BlogListView):
    page_type = ''
    template_name = 'blog/article_list.html'

    context_object_name = 'article_list'

    def get_queryset_data(self):
        article_list = Article.objects.filter(type='a', status='p')
        return article_list

    def get_queryset_cache_key(self):
        cache_key = 'index_{page}'.format(page=3)
        return cache_key


# 详情页面
class ArticleDetailView(BlogListView):
    template_name = 'blog/article_detail.html'

    def get_queryset_data(self):
        article_list = 'shenruxiang'
        return article_list

    def get_queryset_cache_key(self):
        cache_key = 'index_{page}'.format(page=1)
        return cache_key
