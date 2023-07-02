from django.contrib import admin
from users.models import Organisation, User

admin.site.register(User)
admin.site.register(Organisation)
