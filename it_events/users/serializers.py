from djoser.conf import settings
from djoser.serializers import UserCreateSerializer as DjoserUsCreateSerializer
from rest_framework import serializers
from users.models import Organization, User


class UserCreateSerializer(DjoserUsCreateSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (settings.USER_ID_FIELD,
                                                'username',
                                                "password",
                                                'organization')


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ('manager', 'name')
