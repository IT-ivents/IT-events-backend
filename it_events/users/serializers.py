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
    profile = UserProfileSerializer()

    class Meta(UserCreateSerializer.Meta):
        fields = UserCreateSerializer.Meta.fields + ('profile',)

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = super().create(validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        return user


class OrganisationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organisation
        fields = ('id', 'manager', 'name')


class UserProfileEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileEvent
        fields = ('id', 'user_profile', 'event')
