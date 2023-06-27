from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users.models import User


class UserViewSetTest(APITestCase):
    """ Test module to users API """

    def setUp(self) -> None:
        self.user_create_data = {'username': 'new_user', 'password': '!@#QWE!@#', 'email': 'test_email@mail.su'}
        self.user_login_data = {'email': 'test_email@mail.su', 'password': '!@#QWE!@#'}

    def test_create_user(self):
        """Проверка доступности url для создания пользователя.
         Проверка того что пользователь создан"""
        users_count_before = User.objects.all().count()
        response = self.client.post(reverse('api:v1:users-list'), self.user_create_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), users_count_before + 1)

    def test_get_token(self):
        """Проверка доступности url для получния токена.
         Наличие токена в ответе."""
        self.client.post(reverse('api:v1:users-list'), self.user_create_data, format='json')
        response = self.client.post(reverse('api:v1:login'), self.user_login_data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "auth_token")

    def test_delete_token(self):
        """Проверка функционала удаления токена."""
        self.user = User.objects.create_user(**self.user_create_data)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.post(reverse('api:v1:logout'))
        self.client.credentials()
        response = self.client.get(reverse('api:v1:users-me'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserProfileURLTest(APITestCase):
    """ Test user profile API """

    def setUp(self):
        data = {'username': 'test_username', 'password': '!@#QWE!@#'}
        self.user = User.objects.create_user(**data)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_profile(self):
        """Доступ к профилю для авторизованного пользователя"""
        response = self.client.get(reverse('api:v1:users-me'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_user_not_authenticated(self):
        """Отсутствие доступа к профилю для неавторизованного пользователя"""
        self.client.credentials()
        response = self.client.get(reverse('api:v1:users-me'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)