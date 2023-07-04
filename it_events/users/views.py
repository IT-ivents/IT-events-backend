from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Organisation
from .permissions import IsManagerOrReadOnly
from .serializers import OrganisationSerializer, UserProfileSerializer

User = get_user_model()


class UserViewSet(UserViewSet):
    queryset = User.objects.all()

    @action(detail=False, methods=['patch'])
    def update_profile(self, request, *args, **kwargs):
        user = self.request.user
        profile_data = request.data.get('profile', {})
        profile_serializer = UserProfileSerializer(
            user.profile, data=profile_data, partial=True)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(
                {'message': 'Profile updated'}, status=status.HTTP_200_OK)
        return Response(
            profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def delete_profile(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()
        return Response(
            {'message': 'Profile deleted'}, status=status.HTTP_204_NO_CONTENT)


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
