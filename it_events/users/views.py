from djoser.views import UserViewSet as DjoserViewSet
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from api.v1.permissions import IsAdminAuthorOrReadOnly

from .models import Organisation, User
from .permissions import IsManagerOrReadOnly
from .serializers import OrganisationSerializer, UserCreateSerializer


class UserViewSet(DjoserViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (IsAdminAuthorOrReadOnly,)


class OrganisationViewsSet(ModelViewSet):
    permission_classes = (IsManagerOrReadOnly,)
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def perform_create(self, serializer):
        user = self.request.user
        user.role = User.MANAGER
        user.organization_name = serializer.validated_data['name']
        user.save(update_fields=['role', 'organization_name'])
        serializer.save(manager=user)

    def perform_destroy(self, instance):
        user = self.request.user
        user.role = User.USER
        user.organization_name = ""
        user.save(update_fields=['role', 'organization_name'])
        instance.delete()
