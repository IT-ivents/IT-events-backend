from api.v1.filters import EventFilterSet
from api.v1.permissions import IsAdminAuthorOrReadOnly
from api.v1.serializers import (CitySerializer, EventDeleteSerializer,
                                EventReadSerializer,
                                EventWriteUpdateSerializer, TagSerializer,
                                TopicSerializer)
from api.v1.utils import search_events
from django.db.models import Count
from django.http import FileResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from events.models import City, Event, Favourite, Tags, Topic
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.models import Organisation


class EventsViewSet(ModelViewSet):
    permission_classes = (IsAdminAuthorOrReadOnly,)
    serializer_class = EventWriteUpdateSerializer
    # pagination_class = PageLimitPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilterSet
    http_method_names = ['get', 'post']

    def get_queryset(self):
        query = self.request.query_params.get('search', '')
        return Event.objects.all() if not query else search_events(query)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EventReadSerializer
        return EventWriteUpdateSerializer

    def perform_create(self, serializer):
        author = self.request.user
        try:
            organizer = Organisation.objects.get(manager=author)
        except Organisation.DoesNotExist:
            raise Exception("Организация автора события не найдена")
        serializer.save(organizer=organizer)

    @action(detail=False, methods=["get"])
    def popular(self, request):
        current_datetime = timezone.now()
        active_events = Event.objects.filter(date_end__gt=current_datetime)
        sorted_events = active_events.annotate(
            tag_count=Count('tags')).order_by('-tag_count')
        serializer = EventWriteUpdateSerializer(sorted_events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"],
            permission_classes=[IsAuthenticated])
    def favorites(self, request: Request):
        """Маршрутизатор для вывода списка ивентов
        находящихся в Избранном пользователя"""
        queryset = Event.objects.filter(favourite__user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = EventReadSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = EventReadSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"],
            permission_classes=[IsAuthenticated])
    def toggle_favorite(self, request: Request, pk: int):
        """Маршрутизатор для добавления и удаления ивентов
        из Избранного пользователя"""
        event = self.get_object()
        favorite = Favourite.objects.filter(user=request.user,
                                            event=event).first()

        if favorite:
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        Favourite.objects.create(user=request.user, event=event)
        return Response(status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UsersEventsViewSet(ModelViewSet):
    permission_classes = (IsAdminAuthorOrReadOnly,)
    serializer_class = EventWriteUpdateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilterSet
    http_method_names = ['get', 'patch', 'delete']

    def get_queryset(self):
        return self.request.user.events.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EventReadSerializer
        if self.request.method == 'DELETE':
            return EventDeleteSerializer
        return EventWriteUpdateSerializer
    
    def destroy(self, request, *args, **kwargs):
        # Логика удаления событий
        event_ids = request.data.get('event_ids', [])
        events = Event.objects.filter(id__in=event_ids)
        events.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagsViewSet(ModelViewSet):
    serializer_class = TagSerializer
    http_method_names = ['get']
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = Tags.objects.annotate(event_count=Count('event'))
        return queryset.order_by('-event_count')


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    http_method_names = ['get']
    filter_backends = [SearchFilter]
    search_fields = ['name']


class TopicsViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    http_method_names = ['get']
    filter_backends = [SearchFilter]
    search_fields = ['name']


def cookies_view(request):
    file_path = "cookies.pdf"
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')


def privacy_view(request):
    file_path = "privacy.pdf"
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
