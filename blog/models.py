# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from django.utils.timezone import now
from django.urls import reverse
from DjangoUeditor.models import UEditorField
from django.contrib.auth import get_user_model


class BaseModel(models.Model):
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)

    class Meta:
        abstract = True


# 文章表
class Article(BaseModel):
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )
    COMMENT_STATUS = (
        ('o', '打开'),
        ('c', '关闭'),
    )
    TYPE = (
        ('a', '文章'),
        ('p', '页面'),
    )
    title = models.CharField('标题', max_length=200, unique=True)
    # body = models.TextField('正文')
    # 继承百度UEditor文本编辑器
    body = UEditorField('正文', height=300, width=1000, default=u'', blank=True, imagePath="uploads/images/",
                        toolbars='besttome', filePath='uploads/files/')
    pub_time = models.DateTimeField('发布时间', blank=True, null=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES, default='p')
    comment_status = models.CharField('评论状态', max_length=1, choices=COMMENT_STATUS, default='o')
    type = models.CharField('类型', max_length=1, choices=TYPE, default='a')
    views = models.PositiveIntegerField('浏览量', default=0)
    author = models.CharField('文章作者', max_length=32, null=False, default='shenruxiang')
    article_order = models.IntegerField('排序,数字越大越靠前', blank=False, null=False, default=0)
    category = models.ForeignKey('Category', verbose_name='分类', on_delete=models.CASCADE, blank=False, null=False)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-article_order', '-pub_time']
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        get_latest_by = 'created_time'

    def get_absolute_url(self):
        return reverse('blog:article_detail', args=(self.pk,))


# 文章分类表
class Category(BaseModel):
    name = models.CharField('分类名', max_length=30, unique=True)
    parent_category = models.ForeignKey('self', verbose_name="父级分类", blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('blog:category_detail', args=(self.pk,))

    def __str__(self):
        return self.name

    # 获得当前分类目录所有子集
    def get_sub_categorys(self):
        categorys = []
        all_categorys = Category.objects.all()

        def parse(category):
            if category not in categorys:
                categorys.append(category)
            childs = all_categorys.filter(parent_category=category)
            for child in childs:
                if category not in categorys:
                    categorys.append(child)
                parse(child)

        parse(self)
        return categorys


# 文章标签
class Tag(BaseModel):
    name = models.CharField('标签名', max_length=30, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag_detail', args=(self.pk,))

    class Meta:
        ordering = ['name']
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def get_article_count(self):
        return Article.objects.filter(tags__name=self.name).distinct().count()


# 友情链接
class Links(models.Model):
    name = models.CharField('链接名称', max_length=30, unique=True)
    link = models.URLField('链接地址')
    sequence = models.IntegerField('排序', unique=True)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)

    class Meta:
        ordering = ['sequence']
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 侧边栏,可以展示一些html内容
class SideBar(models.Model):
    name = models.CharField('标题', max_length=100)
    content = models.TextField("内容")
    sequence = models.IntegerField('排序', unique=True)
    is_enable = models.BooleanField('是否启用', default=True)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)

    class Meta:
        ordering = ['sequence']
        verbose_name = '侧边栏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 站点设置
class BlogSettings(models.Model):
    sitename = models.CharField("网站名称", max_length=200, null=False, blank=False, default='')
    site_description = models.TextField("网站描述", max_length=1000, null=False, blank=False, default='')
    site_seo_description = models.TextField("网站SEO描述", max_length=1000, null=False, blank=False, default='')
    site_keywords = models.TextField("网站关键字", max_length=1000, null=False, blank=False, default='')
    article_sub_length = models.IntegerField("文章摘要长度", default=300)
    sidebar_article_count = models.IntegerField("侧边栏文章数目", default=10)
    sidebar_comment_count = models.IntegerField("侧边栏评论数目", default=5)
    show_google_adsense = models.BooleanField('是否显示谷歌广告', default=False)
    google_adsense_codes = models.TextField('广告内容', max_length=2000, null=True, blank=True, default='')
    open_site_comment = models.BooleanField('是否打开网站评论功能', default=True)
    beiancode = models.CharField('备案号', max_length=2000, null=True, blank=True, default='')
    analyticscode = models.TextField("网站统计代码", max_length=1000, null=False, blank=False, default='')
    gongan_beiancode = models.TextField('公安备案号', max_length=2000, null=True, blank=True, default='')

    class Meta:
        verbose_name = '网站配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sitename


class Comment(models.Model):
    body = models.TextField('正文', max_length=300)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)
    author = models.ForeignKey(get_user_model(), verbose_name='作者', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name='文章', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', verbose_name="上级评论", blank=True, null=True, on_delete=models.CASCADE)
    is_enable = models.BooleanField('是否显示', default=True, blank=False, null=False)

    class Meta:
        ordering = ['created_time']
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        get_latest_by = 'created_time'

    def __str__(self):
        return self.body

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
