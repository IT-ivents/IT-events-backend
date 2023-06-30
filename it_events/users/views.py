from djoser.views import UserViewSet as DjoserViewSet
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from .models import Organization, User
from .permissions import IsManagerOrReadOnly
from .serializers import OrganizationSerializer


class UserViewSet(DjoserViewSet):
    pass


class OrganizationViewsSet(ModelViewSet):
    permission_classes = (IsManagerOrReadOnly,)
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def perform_create(self, serializer):
        user = self.request.user
        user.role = User.MANAGER
        user.save(update_fields=['role'])
        serializer.save(manager=user)

    def perform_destroy(self, instance):
        user = self.request.user
        user.role = User.USER
        user.save(update_fields=['role'])
        instance.delete()
