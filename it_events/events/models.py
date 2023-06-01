from django.db import models
from users.models import User


class Event(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='events', verbose_name='Автор публикации')
    title = models.CharField(
        "Название мероприятия", max_length=200, db_index=True)
    description = models.TextField(
        "Описание мероприятия", max_length=1000)
    url = models.URLField(
        "Сайт мероприятия", max_length=200, unique=True)
    image = models.ImageField(
        verbose_name='Афиша мероприятия', upload_to='events/image',
        help_text='Загрузите фотографию')
    program = models.TextField(
        "Программа мероприятия", max_length=3000)
    organizer = models.CharField(
        "Организатор", max_length=100)
    partners = models.CharField(
        "Партнеры", max_length=200, blank=True)
    address = models.CharField(
        "Адрес", max_length=200, blank=True)
    price = models.DecimalField(
        "Цена", max_digits=8, decimal_places=2)
    date_start = models.DateTimeField(
        "Дата и время начала")
    date_end = models.DateTimeField(
        "Дата и время окончания")
    created_at = models.DateTimeField(
        "Дата создания записи", auto_now_add=True)
    city = models.ForeignKey(
        'City', on_delete=models.SET_NULL,
        verbose_name="Город проведения", blank=True, null=True)
    tags = models.ManyToManyField(
        'Tags', verbose_name="Теги")
    topic = models.ForeignKey(
        'Topic', on_delete=models.CASCADE, verbose_name="Направление")
    format = models.ManyToManyField(
        'Format', verbose_name="Формат")

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class City(models.Model):
    name = models.CharField(
        'Город проведения', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(
        'Тэг', max_length=200)
    slug = models.SlugField(
        'слаг', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['name']

    def __str__(self):
        return self.name


class Format(models.Model):
    name = models.CharField(
        'Формат', max_length=200, unique=True)
    slug = models.SlugField(
        'слаг', max_length=100, unique=True)

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
        'слаг', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Топик'
        verbose_name_plural = 'Топики'
        ordering = ['name']

    def __str__(self):
        return self.name


class Favourite(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE,
                              verbose_name='Ивент')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ['id']

    def __str__(self):
        return f'Favourite(user={self.user}, event={self.event}'
