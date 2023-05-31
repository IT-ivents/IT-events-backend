from api.v1.filters import EventFilterSet
from api.v1.permissions import IsAdminAuthorOrReadOnly
from api.v1.serializers import (EventReadSerializer, EventWriteSerializer,
                                TagSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from events.models import Event, Favourite, Tags
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class EventsViewSet(ModelViewSet):
    permission_classes = (IsAdminAuthorOrReadOnly,)
    queryset = Event.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = EventFilterSet
    search_fields = ['city__name']
    http_method_names = ['get', 'patch', 'delete', 'post']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return EventReadSerializer
        return EventWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=["get"],
            permission_classes=[IsAuthenticated])
    def favorites(self, request: Request):
        """Маршрутизатор для вывода списка ивентов
        находящихся в Избранном пользователя"""
        queryset = Event.objects.filter(favourite__user=request.user)
        serializer = EventReadSerializer(data=queryset, many=True)
        serializer.is_valid()
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


class TagsViewSet(ModelViewSet):
    serializer_class = TagSerializer
    http_method_names = ['get']
    queryset = Tags.objects.all()
    # Нужно тестить когда будут ивенты
    # def get_queryset(self):
    #     queryset = Tags.objects.annotate(event_count=Count('event'))
    #     return queryset.order_by('-event_count')
