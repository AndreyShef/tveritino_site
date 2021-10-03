from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


# Добавление RSS для статей
class LatestPostsFeed(Feed):
    title = 'Мой блог'
    link = '/blog/'
    description = 'Новая статья в моём блоге.'

    def items(self):
        """Получает объекты, которые будут включены в рассылку"""
        return Post.published.all()[:3]  # берём последние 3 статьи

    def item_title(self, item):
        """Получает title для каждого результата из item()"""
        return item.title

    def item_description(self, item):
        """Получает description для каждого результата из item()"""
        return truncatewords(item.body, 30)
