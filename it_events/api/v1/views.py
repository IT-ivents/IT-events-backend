from api.v1.filters import EventFilterSet
from api.v1.permissions import IsAdminAuthorOrReadOnly
from api.v1.serializers import (EventReadSerializer, EventWriteSerializer,
                                TagSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from events.models import Event, Tags
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet


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


class EventSearchView(ModelViewSet):
    serializer_class = EventReadSerializer
    permission_classes = (IsAdminAuthorOrReadOnly,)
    http_method_names = ['get']

    def get_queryset(self):
        tag_name = self.request.GET.get('tag')
        if tag_name:
            return Event.objects.filter(tags__name__icontains=tag_name)
        else:
            return Event.objects.all()


class TagsViewSet(ModelViewSet):
    serializer_class = TagSerializer
    http_method_names = ['get']
    queryset = Tags.objects.all()
    # Нужно тестить когда будут ивенты
    # def get_queryset(self):
    #     queryset = Tags.objects.annotate(event_count=Count('event'))
    #     return queryset.order_by('-event_count')
