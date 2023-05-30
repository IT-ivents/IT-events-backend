from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
class Event(models.Model):
    pass


class City(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='events', verbose_name='Автор публикации')
    name = models.CharField(
        'Город проведения', max_length=200, unique=True)



class Tags(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='events', verbose_name='Автор публикации')
    name = models.CharField(
        'Тэг', max_length=200)
    slug = models.SlugField(
        'Ссылка', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['-id']

    def __str__(self):
        return self.name

class Format(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='events', verbose_name='Автор публикации')
    name = models.CharField(
        'Формат', max_length=200, unique=True)
    slug = models.SlugField(
        'Ссылка', max_length=100, unique=True)


class Topic(models.Model):
    """Направление(Дизайн, Разработка)"""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='events', verbose_name='Автор публикации')
    name = models.CharField(
        'Направление', max_length=200, unique=True)
    slug = models.SlugField(
        'Ссылка', max_length=100, unique=True)


class SubTopic(models.Model):
    """Под направление(Backend, Frontend)"""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='events', verbose_name='Автор публикации')
    name = models.CharField(
        'Направление', max_length=200, unique=True)
    slug = models.SlugField(
        'Ссылка', max_length=100, unique=True)
