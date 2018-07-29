#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: shenruxiang
@license: MIT Licence
@contact: 1638824607@qq.com
@site: https://www.shenruxiang.org/
@software: PyCharm
@file: context_processors.py
@time: 2018/6/12 下午3:25
"""
from .models import Category, Article
from django.core.cache import cache
import logging
logger = logging.getLogger('shenblog')


# 获取网站基本配置
def seo_processor(request):
    key = 'seo_processor'
    value = cache.get(key)
    if value:
        # logger.info('get processor cache.')

        return value
    else:
        # logger.info('set processor cache.')

        from blog.models import BlogSettings

        site_base_url = 'http://127.0.0.1:8000/'

        if not BlogSettings.objects.count():
            sitename = '忘境之湖'
            site_description = '岁月静好，时光如初'
            site_seo_description = '基于Django的博客系统'
            site_seo_keywords = 'Django,Python'
            article_sub_length = 300
            sidebar_article_count = 10
            sidebar_comment_count = 5
            open_site_comment = True
            beiancode = '京ICP备16037842号'
            gongan_beiancode = '京ICP备16037842号'
            analyticscode = '代码统计'
        else:
            setting = BlogSettings.objects.first()

            sitename = setting.sitename
            site_description = setting.site_description
            site_seo_description = setting.site_seo_description
            site_seo_keywords = setting.site_keywords
            article_sub_length = setting.article_sub_length
            open_site_comment = setting.open_site_comment
            sidebar_article_count = setting.sidebar_article_count
            sidebar_comment_count = setting.sidebar_comment_count
            beiancode = setting.beiancode
            gongan_beiancode = setting.gongan_beiancode
            analyticscode = setting.analyticscode

        nav_category_list = Category.objects.all()
        nav_pages = Article.objects.filter(type='p', status='p')

        value = {
            'SITE_NAME': sitename,
            'SITE_SEO_DESCRIPTION': site_seo_description,
            'SITE_DESCRIPTION': site_description,
            'SITE_KEYWORDS': site_seo_keywords,
            'SITE_BASE_URL': site_base_url,
            'ARTICLE_SUB_LENGTH': article_sub_length,
            'SIDEBAE_ARTICLE_COUNT': sidebar_article_count,
            'SIDEBAR_COMMENT_COUNT': sidebar_comment_count,
            'nav_category_list': nav_category_list,
            'nav_pages': nav_pages,
            'OPEN_SITE_COMMENT': open_site_comment,
            'BEIAN_CODE': beiancode,
            'BEIAN_CODE_GONGAN': gongan_beiancode,
            'ANALYTICS_CODE': analyticscode,
        }
        cache.set(key, value, 60 * 60 * 10)
        return value
