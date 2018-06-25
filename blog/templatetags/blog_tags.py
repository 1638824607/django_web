# -*- coding: utf-8 -*-
from django import template
from ..models import Article, Tag, Category, SideBar, Links, Comment
import mistune
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
import request
from django.urls import reverse

from pygments import highlight
from pygments.lexers import get_lexer_by_name

register = template.Library()


@register.simple_tag
def get_recent_articles(num=5):
    return Article.objects.all().order_by('-created_time')[:num]


# 获取分类列表
@register.simple_tag
def get_category_list(category_id=None):
    return Category.objects.filter(parent_category_id=category_id)


# 加载文章详情 isindex 列表页或详情页两种显示方式
@register.inclusion_tag('blog/tags/article_info.html')
def load_article_detail(article, isindex, user):

    from blog.context_processors import seo_processor
    blogsetting = seo_processor(request)

    return {
        'article': article,
        'isindex': isindex,
        'user': user,
        'open_site_comment': blogsetting['OPEN_SITE_COMMENT'],
    }


# 获得文章面包屑
# @register.inclusion_tag('blog/tags/breadcrumb.html')
# def load_breadcrumb(article):
    # names = article.get_category_tree()
    # from DjangoBlog.utils import get_blog_setting
    # blogsetting = get_blog_setting()
    # site = Site.objects.get_current().domain
    # names.append((blogsetting.sitename, site))
    # names = names[::-1]
    #
    # return {
    #     'names': names,
    #     'title': article.title
    # }

@register.filter
def markdown_detail(value):
    renderer = BlogMarkDownRenderer(inlinestyles=False)

    mdp = mistune.Markdown(escape=True, renderer=renderer)
    return mark_safe(mdp(value))


# 字符串截取
@register.filter(is_safe=True)
@stringfilter
def truncatechars_content(content):
    from django.template.defaultfilters import truncatechars_html
    from blog.context_processors import seo_processor
    blogsetting = seo_processor(request)
    return truncatechars_html(content, blogsetting['ARTICLE_SUB_LENGTH'])



class BlogMarkDownRenderer(mistune.Renderer):
    def block_code(self, text, lang=None):
        inlinestyles = self.options.get('inlinestyles')
        linenos = self.options.get('linenos')
        return block_code(text, lang, inlinestyles, linenos)


def block_code(text, lang, inlinestyles=False, linenos=False):
    if not lang:
        text = text.strip()
        return u'<pre><code>%s</code></pre>\n' % mistune.escape(text)

    try:
        lexer = get_lexer_by_name(lang, stripall=True)
        from pygments.formatters import html
        formatter = html.HtmlFormatter(
            noclasses=inlinestyles, linenos=linenos
        )
        code = highlight(text, lexer, formatter)
        if linenos:
            return '<div class="highlight">%s</div>\n' % code
        return code
    except:
        return '<pre class="%s"><code>%s</code></pre>\n' % (
            lang, mistune.escape(text)
        )


# 获得文章meta底部信息
@register.inclusion_tag('blog/tags/article_meta_info.html')
def load_article_metas(article, user):
    return {
        'article': article,
        'user': user
    }


# 格式化时间
@register.simple_tag
def datetimeformat(data):
    try:
        return data.strftime('%Y-%m-%d')
    except:
        return ""


# 加载侧边栏
@register.inclusion_tag('blog/tags/sidebar.html')
def load_sidebar(user):
    from blog.context_processors import seo_processor
    blogsetting = seo_processor(request)
    recent_articles = Article.objects.filter(status='p')[:blogsetting['SIDEBAE_ARTICLE_COUNT']]
    sidebar_categorys = Category.objects.all()
    extra_sidebars = SideBar.objects.filter(is_enable=True).order_by('sequence')
    most_read_articles = Article.objects.filter(status='p').order_by('-views')[:blogsetting['SIDEBAE_ARTICLE_COUNT']]
    dates = Article.objects.datetimes('created_time', 'month', order='DESC')
    links = Links.objects.all()
    commment_list = Comment.objects.filter(is_enable=True).order_by('-id')[:blogsetting['SIDEBAR_COMMENT_COUNT']]
    # show_adsense = settings.SHOW_GOOGLE_ADSENSE
    # 标签云 计算字体大小
    # 根据总数计算出平均值 大小为 (数目/平均值)*步长
    increment = 5
    tags = Tag.objects.all()
    sidebar_tags = None
    if tags and len(tags) > 0:
        s = list(map(lambda t: (t, t.get_article_count()), tags))
        count = sum(map(lambda t: t[1], s))
        dd = 1 if count == 0 else count / len(tags)
        sidebar_tags = list(map(lambda x: (x[0], x[1], (x[1] / dd) * increment + 10), s))

    return {
        'recent_articles': recent_articles,
        'sidebar_categorys': sidebar_categorys,
        'most_read_articles': most_read_articles,
        'article_dates': dates,
        'sidabar_links': links,
        'sidebar_comments': commment_list,
        'user': user,
        'show_google_adsense': False,
        'google_adsense_codes': '',
        'open_site_comment': True,
        'sidebar_tags': sidebar_tags,
        'extra_sidebars': extra_sidebars
    }


@register.inclusion_tag('blog/tags/article_pagination.html')
def load_pagination_info(page_obj, page_type, tag_name):
    previous_url = ''
    next_url = ''
    # 首页
    if page_type == '':
        if page_obj.has_next():
            next_number = page_obj.next_page_number()
            next_url = reverse('blog:index_page', kwargs={'page': next_number})
        if page_obj.has_previous():
            previous_number = page_obj.previous_page_number()
            previous_url = reverse('blog:index_page', kwargs={'page': previous_number})
    # 标签
    if page_type == '分类标签归档':
        tag = get_object_or_404(Tag, name=tag_name)
        if page_obj.has_next():
            next_number = page_obj.next_page_number()
            next_url = reverse('blog:tag_detail_page', kwargs={'page': next_number, 'tag_id': tag.pk})
        if page_obj.has_previous():
            previous_number = page_obj.previous_page_number()
            previous_url = reverse('blog:tag_detail_page', kwargs={'page': previous_number, 'tag_id': tag.pk})
    # 作者
    if page_type == '作者文章归档':
        if page_obj.has_next():
            next_number = page_obj.next_page_number()
            next_url = reverse('blog:author_detail_page', kwargs={'page': next_number, 'author_name': tag_name})
        if page_obj.has_previous():
            previous_number = page_obj.previous_page_number()
            previous_url = reverse('blog:author_detail_page', kwargs={'page': previous_number, 'author_name': tag_name})
    # 分类
    if page_type == '分类目录归档':
        category = get_object_or_404(Category, name=tag_name)
        if page_obj.has_next():
            next_number = page_obj.next_page_number()
            next_url = reverse('blog:category_detail_page',
                               kwargs={'page': next_number, 'category_id': category.pk})
        if page_obj.has_previous():
            previous_number = page_obj.previous_page_number()
            previous_url = reverse('blog:category_detail_page',
                                   kwargs={'page': previous_number, 'category_id': category.pk})

    return {
        'previous_url': previous_url,
        'next_url': next_url,
        'page_obj': page_obj
    }
