from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from events.models import City, Event, Tags, Topic
from mixer.backend.django import mixer

User = get_user_model()


class EventURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.event = mixer.blend(Event)
        self.tag = mixer.blend(Tags)
        self.city = mixer.blend(City)
        self.topic = mixer.blend(Topic)

    def test_all_user_all_page(self):
        response = self.guest_client.get(reverse('api:v1:events-list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.guest_client.get(reverse('api:v1:events-detail', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.guest_client.get(reverse('api:v1:tags-list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.guest_client.get(reverse('api:v1:sities-list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.guest_client.get(reverse('api:v1:topics-list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_404_url(self):
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
