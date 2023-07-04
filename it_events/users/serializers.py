from djoser.conf import settings
from djoser.serializers import UserCreateSerializer as DjoserUsCreateSerializer
from rest_framework import serializers
from users.models import Organisation, User, UserProfile, UserProfileEvent


class UserCreateSerializer(DjoserUsCreateSerializer):
    """Для регистрации пользователя."""
    organization_name = serializers.CharField()

    class Meta(DjoserUsCreateSerializer.Meta):
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (settings.USER_ID_FIELD,
                                                'username',
                                                "password",
                                                'organization_name')


class UserProfileSerializer(serializers.ModelSerializer):
    """Для Личного кабинета."""
    class Meta:
        model = UserProfile
        fields = (
            'user', 'email', 'profile_photo', 'organization_name', 'name')
        read_only_fields = ('user', 'organization_name')


class OrganisationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organisation
        fields = ('id', 'manager', 'name')


class UserProfileEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileEvent
        fields = ('id', 'user_profile', 'event')


class UserSerializer(UserCreateSerializer):
    """Используется для сериализации и десериализации данных пользователя."""

    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'password', 'first_name', 'last_name',
            'organization_name', 'profile'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        UserProfile.objects.create(user=user, email=user.email, **profile_data)
        return user
