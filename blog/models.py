from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# Создание своего менеджера модели взамен objects
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'В разработке'),
        ('published', 'Опубликовано'),
    )
    title = models.CharField(max_length=200, verbose_name='Название статьи')
    slug = models.SlugField(max_length=200, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts',
                               verbose_name='Автор')
    body = models.TextField(verbose_name='Поле для статьи')
    publish = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')
    objects = models.Manager()  # Менеджер по умолчанию
    published = PublishedManager()  # Мой новый менеджер
    tags = TaggableManager(verbose_name="Тэги")  # Для тэгов статей

    def get_absolute_url(self):
        """Для получения ссылок на статью"""
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day,
                                                 self.slug])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


# Модель комментария
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Статья')
    name = models.CharField(max_length=80, verbose_name='Имя')
    email = models.EmailField()
    body = models.TextField(verbose_name='Комментарий')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    active = models.BooleanField(default=True)

    def __str__(self):
        return 'Комментарий {} к статье {}'.format(self.name, self.post)

    class Meta:
        ordering = ('created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
