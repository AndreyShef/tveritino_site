import markdown
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from ..models import Post

register = template.Library()


# Тэг для показа количества статей
@register.simple_tag
def total_posts():
    return Post.published.count()


# Тэг для добавления последних статей
@register.inclusion_tag('blog/post/latest_posts.html')  # Инклюзивный тэг с указанием шаблона для формирования HTML
def show_latest_posts(count=5):  # указываем количество показываемых статей
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# Тэг для отображения статей с наибольшим ко-вом комментариев
@register.simple_tag
def get_most_commented_posts(count=3):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


# Фильтр для заполнения тела статьи с помощью форматирования Markdown
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
