from django.contrib import admin
from users.models import Organisation, User, UserProfile, UserProfileEvent

admin.site.register(User)
admin.site.register(Organisation)
admin.site.register(UserProfileEvent)
admin.site.register(UserProfile)
