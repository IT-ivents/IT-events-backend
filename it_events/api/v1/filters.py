from django_filters import rest_framework as filters

from events.models import Event, Format, Tags


class EventFilterSet(filters.FilterSet):
    price__lte = filters.NumberFilter(field_name='price', lookup_expr='lte')
    price__gte = filters.NumberFilter(field_name='price', lookup_expr='gte')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tags.objects.all())
    formats = filters.ModelMultipleChoiceFilter(
        field_name='format__slug',
        to_field_name='slug',
        queryset=Format.objects.all())
    topic = filters.CharFilter(field_name='topic__slug')

    class Meta:
        model = Event
        fields = ('tags', 'formats', 'topic', 'price')
