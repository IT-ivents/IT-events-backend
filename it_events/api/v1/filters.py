from django.db.models import Q
from django_filters import rest_framework as filters
from events.models import Event, Format, Tags, Topic


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
    city = filters.CharFilter(
        field_name='city__name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Event
        fields = []

    q = filters.CharFilter(
        method='filter_by_search',
        label='Search',
    )

    def filter_by_search(self, queryset, name, value):
        queryset = queryset.filter(
            Q(title__icontains=value)
            | Q(url__icontains=value)
            | Q(program__icontains=value)
            | Q(tags__name__icontains=value)
            | Q(topic__name__icontains=value)
            | Q(city__icontains=value)
            | Q(format__name__icontains=value)
        )
        if not queryset.exists():
            Event.objects.none()
        return queryset
