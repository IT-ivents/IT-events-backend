from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from users.models import Organisation, UserEvent

User = get_user_model()


class UserSerializer(UserSerializer):
    organization_name = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'organization_name',
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    organization_name = serializers.CharField(required=True)

    # class Meta(UserCreateSerializer.Meta):
    #     fields = ('username', 'password', 'email', 'organization_name',)
    class Meta(UserCreateSerializer.Meta):
        fields = UserCreateSerializer.Meta.fields + ('organization_name',)

    def perform_create(self, serializer):
        organization_name = self.validated_data.pop('organization_name')
        user = super().perform_create(serializer)
        Organisation.objects.create(name=organization_name, manager=user)
        return user


class OrganisationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organisation
        fields = ('id', 'manager', 'name')


class UserEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvent
        fields = ('id', 'user', 'event')
