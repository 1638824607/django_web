# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.core.cache import cache
from django.http import HttpResponse
from blog.models import Article, Category, Tag
import logging
from django.conf import settings

logger = logging.getLogger('shenblog')


# 列表视图基类
class BlogListView(ListView):
    # 设置页面类型 文章列表 分类列表 标签列表
    page_type = ''

    # 更改默认的分页数
    paginate_by = settings.PAGINATE_BY

    # 设置分页参数
    page_kwarg = 'page'

    @property
    def page_number(self):
        # 默认分页get参数为page 例如page=2
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        return page

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

    template_name = 'blog/article_list.html'

    context_object_name = 'article_list'

    def get_queryset_data(self):
        article_list = Article.objects.filter(type='a', status='p')
        return article_list

    def get_queryset_cache_key(self):
        cache_key = 'index_{page}'.format(page=self.page_number)
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


# 分类页面
class CategoryDetailView(ArticleListView):
    page_type = "分类目录归档"

    def get_queryset_data(self):
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, id=category_id)

        categoryname = category.name
        self.categoryname = categoryname

        # 获取当前分类下所有分类id  py3 map返回的是迭代器
        categoryids = list(map(lambda c: c.id, category.get_sub_categorys()))

        # 联表查询分类集合下的文章
        article_list = Article.objects.filter(category__id__in=categoryids, status='p')

        return article_list

    def get_queryset_cache_key(self):
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, id=category_id)
        categoryname = category.name
        self.categoryname = categoryname
        cache_key = 'category_list_{category_id}_{page}'.format(category_id=category_id, page=self.page_number)
        return cache_key

    def get_context_data(self, **kwargs):
        categoryname = self.categoryname
        try:
            categoryname = categoryname.split('/')[-1]
        except:
            pass
        kwargs['page_type'] = CategoryDetailView.page_type
        kwargs['tag_name'] = categoryname
        return super(CategoryDetailView, self).get_context_data(**kwargs)


# 标签详情
class TagDetailView(ArticleListView):
    page_type = '分类标签归档'

    def get_queryset_data(self):
        tag_id = self.kwargs['tag_id']
        tag = get_object_or_404(Tag, id=tag_id)
        tag_name = tag.name
        self.name = tag_name
        article_list = Article.objects.filter(tags__id=tag_id)
        return article_list

    def get_queryset_cache_key(self):
        tag_id = self.kwargs['tag_id']
        tag = get_object_or_404(Tag, id=tag_id)
        self.name = tag.name
        cache_key = 'tag_{tag_id}_{page}'.format(tag_id=tag_id, page=self.page_number)
        return cache_key

    def get_context_data(self, **kwargs):
        tag_name = self.name
        kwargs['page_type'] = TagDetailView.page_type
        kwargs['tag_name'] = tag_name
        return super(TagDetailView, self).get_context_data(**kwargs)


# 登陆
class SignInView(ListView):
    template_name = 'blog/article_detail.html'
    context_object_name = 'tag_list'

    def get_queryset(self):
        tags_list = []
        tags = Tag.objects.all()
        for t in tags:
            t.article_set.count()


# 刷新缓存
def refresh_memcache(request):
    try:
        if request.user.is_superuser:
            if cache and cache is not None:
                cache.clear()
            return HttpResponse("刷新缓存成功")
        else:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden()
    except Exception as e:
        return HttpResponse(e)
