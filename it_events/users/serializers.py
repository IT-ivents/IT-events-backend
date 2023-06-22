from djoser.conf import settings
from djoser.serializers import UserCreateSerializer as DjoserUsCreateSerializer
from users.models import User, Organisation
from rest_framework import serializers


class UserCreateSerializer(DjoserUsCreateSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (settings.USER_ID_FIELD,
                                                'username',
                                                "password",)


class OrganisationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organisation
        fields = "__all__"
