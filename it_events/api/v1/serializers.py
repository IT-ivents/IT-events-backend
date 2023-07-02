from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from events.models import City, Event, Format, Tags, Topic
from rest_framework import serializers
from users.models import Organisation
from users.serializers import OrganisationSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = (
            'id', 'name', 'slug')


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = (
            'id', 'name')


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = (
            'id', 'name', 'slug')


class FormatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Format
        fields = (
            'id', 'name', 'slug')


class EventReadSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    tags = TagSerializer(many=True)
    topic = TopicSerializer(many=True)
    format = FormatSerializer(many=True)
    organizer = OrganisationSerializer()
    # date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    # created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'url', 'image', 'image_small',
                  'program', 'organizer', 'partners', 'address', 'price',
                  'date_start', 'date_end', 'created_at', 'city', 'tags',
                  'topic', 'format',)


class EventWriteUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    organizer = serializers.PrimaryKeyRelatedField(
        queryset=Organisation.objects.all()
    )
    image = Base64ImageField()
    image_small = Base64ImageField()
    city = serializers.SlugRelatedField(
        slug_field='name', queryset=City.objects.all()
    )
    tags = serializers.SlugRelatedField(
        slug_field='slug', queryset=Tags.objects.all(), many=True
    )
    topic = serializers.SlugRelatedField(
        slug_field='slug', queryset=Topic.objects.all(), many=True
    )
    format = serializers.SlugRelatedField(
        slug_field='slug', queryset=Format.objects.all(), many=True
    )

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'url', 'image', 'image_small',
                  'program', 'organizer', 'partners', 'address', 'price',
                  'date_start', 'date_end', 'city', 'tags', 'topic', 'format',)

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['organizer'] = user.organisation
        return super().create(validated_data)


class EventDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)

    def delete(self):
        event_id = self.validated_data['id']
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise serializers.ValidationError("Событие не найдено.")
        event.delete()
