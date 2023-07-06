from django_filters import rest_framework as filters
from events.models import Format, Tags, Topic


class EventFilterSet(filters.FilterSet):
    price__lte = filters.NumberFilter(field_name='price', lookup_expr='lte')
    price__gte = filters.NumberFilter(field_name='price', lookup_expr='gte')
    date__gte = filters.DateTimeFilter(
        field_name='date_end', lookup_expr='gte'
    )
    date__lte = filters.DateTimeFilter(
        field_name='date_start', lookup_expr='lte'
    )
    tag = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tags.objects.all())
    formats = filters.ModelMultipleChoiceFilter(
        field_name='format__slug',
        to_field_name='slug',
        queryset=Format.objects.all())
    topic = filters.ModelMultipleChoiceFilter(
        field_name='topic__slug',
        to_field_name='slug',
        queryset=Topic.objects.all())
    # city = filters.ModelMultipleChoiceFilter(
    #     field_name='city__name',
    #     to_field_name='name',
    #     queryset=City.objects.all())
