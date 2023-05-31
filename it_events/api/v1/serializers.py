from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from events.models import City, Event, Format, Tags, Topic


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
    topic = TopicSerializer()
    format = FormatSerializer(many=True)
    # date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    # created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'url', 'image', 'program',
                  'organizer', 'partners', 'address', 'price', 'date_start',
                  'date_end', 'created_at', 'city', 'tags', 'topic', 'format',)


class EventWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = Base64ImageField()
    city = serializers.SlugRelatedField(
        slug_field='name', queryset=City.objects.all()
    )
    tags = serializers.SlugRelatedField(
        slug_field='slug', queryset=Tags.objects.all(), many=True
    )
    topic = serializers.SlugRelatedField(
        slug_field='slug', queryset=Topic.objects.all()
    )
    format = serializers.SlugRelatedField(
        slug_field='slug', queryset=Format.objects.all(), many=True
    )

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'url', 'image', 'program',
                  'organizer', 'partners', 'address', 'price', 'date_start',
                  'date_end', 'city', 'tags', 'topic', 'format',)
