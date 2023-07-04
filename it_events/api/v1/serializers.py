from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from events.models import City, Event, Format, Tags, Topic
from rest_framework import serializers


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
        read_only=True, default=serializers.CurrentUserDefault())
    image = Base64ImageField()
    image_small = Base64ImageField()
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(), many=True
    )
    topic = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(), many=True
    )
    format = serializers.PrimaryKeyRelatedField(
        queryset=Format.objects.all(), many=True
    )

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'url', 'image', 'image_small',
                  'program', 'organizer', 'partners', 'address', 'price',
                  'date_start', 'date_end', 'city', 'tags', 'topic', 'format',
                  )

    @transaction.atomic
    def create(self, validated_data):
        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.url = validated_data.get('url', instance.url)
        instance.image = validated_data.get('image', instance.image)
        instance.image_small = validated_data.get('image_small',
                                                  instance.image_small)
        instance.program = validated_data.get('program', instance.program)
        instance.partners = validated_data.get('partners', instance.partners)
        instance.address = validated_data.get('address', instance.address)
        instance.date_start = validated_data.get('date_start',
                                                 instance.date_start)
        instance.date_end = validated_data.get('date_end', instance.date_end)
        instance.city = validated_data.get('city', instance.city)
        tags = validated_data.pop('tags')
        if tags:
            instance.tags.set(tags)
        topic = validated_data.pop('topic')
        if topic:
            instance.topic.set(topic)
        format = validated_data.pop('format')
        if format:
            instance.format.set(format)
        instance.save()
        return instance


class EventDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    def delete(self):
        event_id = self.validated_data['id']
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise serializers.ValidationError("Событие не найдено.")
        event.delete()
