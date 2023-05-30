from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from api.v1.filters import EventFilterSet
from api.v1.permissions import IsAdminAuthorOrReadOnly
from api.v1.serializers import EventReadSerializer, EventWriteSerializer
from events.models import Event


class EventsViewSet(ModelViewSet):
    permission_classes = (IsAdminAuthorOrReadOnly,)
    queryset = Event.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = EventFilterSet
    search_fields = ['city__name']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return EventReadSerializer
        return EventWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
