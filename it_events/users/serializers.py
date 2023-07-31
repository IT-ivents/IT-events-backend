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
    organization_name = serializers.CharField()

    class Meta:
        model = UserProfile
        fields = ('user', 'email', 'profile_photo',
                  'organization_name', 'name',)
        read_only_fields = ('user', 'organization_name')


class CustomUserCreateSerializer(UserCreateSerializer):
    organization_name = serializers.CharField(required=True)

    class Meta(UserCreateSerializer.Meta):
        fields = ('username', 'password', 'email',
                  'first_name', 'last_name', 'organization_name',)


    def create(self, validated_data):
        organization_name = validated_data.pop('organization_name')
        user = super().create(validated_data)
        Organisation.objects.create(name=organization_name, manager=user)
        profile_data = {
            'user': user,
            'email': user.email,
            'organization_name': organization_name,
            'name': f"{user.first_name} {user.last_name}"
        }
        UserProfile.objects.create(**profile_data)
        user.profile.organization_name = organization_name
        user.profile.save()
        return user


class OrganisationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organisation
        fields = ('id', 'manager', 'name')


class UserProfileEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileEvent
        fields = ('id', 'user_profile', 'event')
