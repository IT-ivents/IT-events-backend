from djoser.views import UserViewSet as DjoserViewSet
from rest_framework.viewsets import ModelViewSet
from .models import Organisation
from rest_framework.filters import SearchFilter

from .serializers import OrganisationSerializer


class UserViewSet(DjoserViewSet):
    pass


class OrganisationViewsSet(ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
