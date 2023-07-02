from django.contrib import admin
from django.utils.html import format_html
from events.models import City, Event, Format, Tags, Topic


@admin.register(Event)
class PostAdmin(admin.ModelAdmin):
    """
    Админ-панель модели Событие
    """
    def url_link(self, obj):
        return format_html(
            f'<a href="{obj.url}" target="_blank">{obj.url}</a>')

    list_display = ['title', 'author', 'city', 'url_link',
                    'date_start', 'created_at']
    list_filter = ['format', 'price', 'date_start', 'created_at']
    search_fields = ['title', 'organizer', 'city__name',
                     'topic__name', 'tags__name']
    raw_id_fields = ['author', 'city', 'topic']
    date_hierarchy = 'date_start'
    ordering = ['-created_at']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """
    Админ-панель модели Направление
    """
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    """
    Админ-панель модели Тег
    """
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    """
    Админ-панель модели Формат
    """
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(City)
