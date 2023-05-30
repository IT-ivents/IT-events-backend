from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
class Event(models.Model):
    pass


class City(models.Model):
    name = models.CharField(
        'Город проведения', max_length=200, unique=True)

    class Meta:
        ordering = ['name']

class Tags(models.Model):
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
    name = models.CharField(
        'Формат', max_length=200, unique=True)
    slug = models.SlugField(
        'Ссылка', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Формат'
        verbose_name_plural = 'Форматы'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Topic(models.Model):
    """Направление(Дизайн, Разработка)"""
    name = models.CharField(
        'Направление', max_length=200, unique=True)
    slug = models.SlugField(
        'Ссылка', max_length=100, unique=True)


class SubTopic(models.Model):
    """Под направление(Backend, Frontend)"""
    name = models.CharField(
        'Направление', max_length=200, unique=True)
    slug = models.SlugField(
        'Ссылка', max_length=100, unique=True)
