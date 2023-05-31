from django.contrib import admin
from events.models import City, Event, Format, Tags, Topic

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """
    Админ-панель модели Направления
    """
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Event)
admin.site.register(City)
admin.site.register(Tags)
admin.site.register(Format)
