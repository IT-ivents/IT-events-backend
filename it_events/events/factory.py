import random
from datetime import timedelta

import factory
import pytz
from faker import Faker
from users.models import User

from .models import City, Event, Format, Tags, Topic

fake_ru = Faker('ru_RU')

cities = list(City.objects.all())
tags_ids = list(Tags.objects.all().values_list('id', flat=True))
topics = list(Topic.objects.all())
formats_ids = list(Format.objects.all().values_list('id', flat=True))


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    author = User.objects.all().first()
    title = factory.LazyAttribute(lambda _: fake_ru.text(max_nb_chars=100))
    description = factory.LazyAttribute(
        lambda _: fake_ru.text(max_nb_chars=500))
    url = factory.LazyAttribute(lambda _: fake_ru.url())
    image = factory.django.ImageField(color='gray')
    program = factory.LazyAttribute(lambda _: fake_ru.text(max_nb_chars=1000))
    organizer = factory.LazyAttribute(lambda _: fake_ru.company())
    partners = factory.LazyAttribute(
        lambda _: ', '.join(fake_ru.company()
                            for _ in range(random.randint(2, 5))))
    address = factory.LazyAttribute(lambda o: fake_ru.address())
    price = factory.LazyAttribute(lambda _: fake_ru.random_number(digits=6))
    city = random.choice(cities)
    topic = random.choice(topics)

    @factory.post_generation
    def format(self, create, extracted, **kwargs):
        if not create:
            return

        self.format.set(random.choices(formats_ids, k=1))

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        tags_list = random.choices(tags_ids, k=3)
        self.tags.set(tags_list)

    @factory.lazy_attribute
    def date_start(self):
        timezone = pytz.timezone('Europe/Moscow')
        return timezone.localize(fake_ru.date_time_this_year())

    @factory.lazy_attribute
    def date_end(self):
        return self.date_start + timedelta(hours=random.randint(1, 48))
