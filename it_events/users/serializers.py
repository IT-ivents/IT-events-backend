from djoser.conf import settings
from djoser.serializers import UserCreateSerializer as DjoserUsCreateSerializer
from rest_framework import serializers
from users.models import Organisation, User


class UserCreateSerializer(DjoserUsCreateSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (settings.USER_ID_FIELD,
                                                'username',
                                                "password",)


class OrganisationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organisation
        fields = ('manager', 'name')
