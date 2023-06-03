from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from events.models import Event


def search_events(query: str):
    """Осуществляет поиск объектов Event наиболее подходящих
     под запрос пользователя и возвращает их.
     query - запрос пользователя в поисковой строке
     """
    print(query)
    search_vector = SearchVector(
        'title', 'description', 'program', 'organizer', 'partners', 'address',
        'city__name', 'tags__name', 'topic__name'
    )
    formatted_words = " | ".join([f"'{word}'" for word in set(query.split())])
    search_query = SearchQuery(formatted_words, search_type='raw')
    return Event.objects.annotate(
        rank=SearchRank(search_vector, search_query)
    ).filter(rank__gte=0.01).distinct('id', 'rank').order_by('-rank')