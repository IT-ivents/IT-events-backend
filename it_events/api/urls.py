from django.urls import include, path
from rest_framework import routers
from .views import EventsViewSet

app_name = "api"

router = routers.DefaultRouter()

router.register('events', EventsViewSet, basename='events')

urlpatterns = [
    path('v1/', include('api.v1.urls', namespace='v1')),
    path('', include(router.urls)),
]
