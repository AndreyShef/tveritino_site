from django.contrib.sitemaps import Sitemap
from .models import Post


# Карта сайта
class PostSitemap(Sitemap):
    changefreq = 'weekly'  # Частота обновления страниц сата
    priority = 0.9  # Степень совпадения статей с тематикой сайта (max - 1)

    def items(self):
        """Возвращает QuerySet объектов, которые будут отображаться в карте сайта"""
        return Post.published.all()

    def lastmod(self, obj):
        """Принимает каждый объект из items() и возвращает время последней модификации статьи"""
        return obj.update
