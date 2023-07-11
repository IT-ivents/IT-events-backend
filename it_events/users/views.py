from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Organisation
from .permissions import IsManagerOrReadOnly
from .serializers import (OrganisationSerializer, UserProfileSerializer,
                          UserSerializer)

User = get_user_model()


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'], url_path='profile')
    def get_profile(self, request, id=None):
        user = self.get_object()
        profile = user.profile
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='profile')
    def update_profile(self, request, id=None):
        user = self.get_object()
        profile = user.profile
        serializer = UserProfileSerializer(
            profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='profile')
    def delete_profile(self, request, id=None):
        user = self.get_object()
        user.profile.delete()
        return Response({'message': 'Профиль удален'},
                        status=status.HTTP_204_NO_CONTENT)


class OrganisationViewsSet(ModelViewSet):
    permission_classes = (IsManagerOrReadOnly,)
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def perform_create(self, serializer):
        user = self.request.user
        user.role = User.ADMIN
        user.organization_name = serializer.validated_data['name']
        user.save(update_fields=['role', 'organization_name'])
        serializer.save(manager=user)

    def perform_destroy(self, instance):
        user = self.request.user
        user.role = User.USER
        user.organization_name = ""
        user.save(update_fields=['role', 'organization_name'])
        instance.delete()
