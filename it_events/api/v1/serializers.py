from django.contrib.auth import get_user_model
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from events.models import City, Event, Format, Tags, Topic
from rest_framework import serializers
from users.models import Organisation
from users.serializers import OrganisationSerializer

User = get_user_model()


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
    tags = TagSerializer(many=True)
    topic = TopicSerializer(many=True)
    format = FormatSerializer(many=True)
    organizer = OrganisationSerializer()

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'url', 'image', 'image_small',
                  'program', 'organizer', 'partners', 'address', 'price',
                  'date_start', 'date_end', 'created_at', 'city', 'tags',
                  'topic', 'format',)


class EventWriteUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    image = Base64ImageField()
    image_small = Base64ImageField()
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
                  'author', 'date_start', 'date_end', 'city', 'tags', 'topic',
                  'format',)
        read_only_fields = ('organizer',)

    def create(self, validated_data):
        author = self.context['request'].user
        try:
            organizer = Organisation.objects.get(manager=author)
        except Organisation.DoesNotExist:
            raise serializers.ValidationError(
                "Организация автора события не найдена")
        validated_data['organizer'] = organizer

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
        instance.price = validated_data.get('price', instance.price)
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

    def validate(self, data):
        formats_val = data.get('format')
        offline = 'offline'
        online = 'online'
        if offline in str(formats_val) and (
                data.get('city') is None or data.get('address') is None):
            raise serializers.ValidationError(
                'Добавьте город и адрес.'
            )
        elif online in str(formats_val) and (
                data.get('city') is not None or
                data.get('address') is not None) and (
                offline not in str(formats_val)):
            raise serializers.ValidationError(
                'город и адрес не нужны'
            )
        else:
            return data




class EventDeleteSerializer(serializers.Serializer):
    event_ids = serializers.ListField(child=serializers.IntegerField())
