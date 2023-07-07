from django.contrib import admin
from users.models import Organisation, User, UserEvent

admin.site.register(User)
admin.site.register(Organisation)
admin.site.register(UserEvent)

