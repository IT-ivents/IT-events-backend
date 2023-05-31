from django.contrib import admin

from events.models import City, Event, Format, Tags, Topic

admin.site.register(Event)
admin.site.register(City)
admin.site.register(Tags)
admin.site.register(Topic)
admin.site.register(Format)
