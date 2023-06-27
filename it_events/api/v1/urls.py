from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet

from .views import (CityViewSet, EventsViewSet, TagsViewSet, TopicsViewSet,
                    cookies_view, privacy_view)

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('events', EventsViewSet, basename='events')
router.register('tags', TagsViewSet, basename='tags')
router.register('sities', CityViewSet, basename='sities')
router.register('topics', TopicsViewSet, basename='topics')

app_name = "v1"

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
    path('cookies/', cookies_view, name='cookies'),
    path('privacy/', privacy_view, name='privacy'),
]
