from events.models import Event
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
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

class SubTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTopic
        fields = (
            'id', 'name', 'slug')
