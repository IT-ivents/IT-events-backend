from djoser.views import UserViewSet as DjoserViewSet
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from .models import Organisation, User
from .permissions import IsManagerOrReadOnly
from .serializers import OrganisationSerializer


class UserViewSet(DjoserViewSet):
    pass


class OrganisationViewsSet(ModelViewSet):
    permission_classes = (IsManagerOrReadOnly,)
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
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
