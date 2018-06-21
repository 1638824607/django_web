# -*- coding: utf-8 -*-
from django import template
from ..models import Article, Tag, Category
import requests
import mistune
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

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
    blogsetting = seo_processor(requests)

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
