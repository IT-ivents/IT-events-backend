from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from users.models import Organisation, UserProfile, UserProfileEvent

User = get_user_model()


class UserSerializer(UserSerializer):
    organization_name = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'organization_name',
        )


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя."""

    class Meta:
        model = UserProfile
        fields = ('user', 'email', 'profile_photo',
                  'organization_name', 'name',)
        read_only_fields = ('user', 'organization_name')


class CustomUserCreateSerializer(UserCreateSerializer):
    organization_name = serializers.CharField()

    class Meta(UserCreateSerializer.Meta):
        fields = ('username', 'password', 'email',
                  'first_name', 'last_name', 'organization_name')


class OrganisationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organisation
        fields = ('id', 'manager', 'name')


class UserProfileEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileEvent
        fields = ('id', 'user_profile', 'event')
