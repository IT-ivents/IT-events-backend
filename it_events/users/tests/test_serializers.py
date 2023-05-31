from djoser.serializers import TokenCreateSerializer
from rest_framework.test import APITestCase

from users.models import User
from users.serializers import UserCreateSerializer


class UserCreateSerializerTest(APITestCase):
    """ Test user serializer """

    def setUp(self) -> None:
        self.valid_data = {'username': 'new_user', 'password': '!@#QWE!@#', 'email': 'test_email@mail.su'}
        self.data_without_username = {'password': '!@#QWE!@#', 'email': 'test_email@mail.su'}
        self.data_without_email = {'username': 'new_user', 'password': '!@#QWE!@#'}
        self.data_with_wrong_email = {'username': 'new_user', 'password': '!@#QWE!@#', 'email': 'test_email'}
        self.data_without_password = {'username': 'new_user', 'email': 'test_email@mail.su'}
        self.valid_data_with_extra = {'username': 'new_user', 'password': '!@#QWE!@#', 'email': 'test_email@mail.su', 'first_name': 'Test_name'}
        self.serializer = UserCreateSerializer

    def test_create_user_serializer(self):
        """Проверка корректности работы сериализатора для создания пользователя"""
        serializer = self.serializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), 'Данные валидны но сериализатор их не принимает')
        serializer = self.serializer(data=self.data_without_username)
        self.assertFalse(serializer.is_valid(), 'Не передан username, но сериализатор это игнорирует')
        serializer = self.serializer(data=self.data_without_email)
        self.assertFalse(serializer.is_valid(), 'Не передан email, но сериализатор это игнорирует')
        serializer = self.serializer(data=self.data_with_wrong_email)
        self.assertFalse(serializer.is_valid(), 'Передан невалидный email, но сериализатор это игнорирует')
        serializer = self.serializer(data=self.data_without_password)
        self.assertFalse(serializer.is_valid(), 'Не передан password, но сериализатор это игнорирует')
        serializer = self.serializer(data=self.valid_data_with_extra)
        self.assertTrue(serializer.is_valid(), 'Сериализатор не игнорирует лишние переданные поля')


class UserLoginSerializerTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='test_username', email='test_email@mail.su', password='!@#QWE!@#')
        self.valid_data = {'password': '!@#QWE!@#', 'email': 'test_email@mail.su'}
        self.data_without_password = {'email': 'test_email@mail.su'}
        self.data_without_email = {'password': '!@#QWE!@#'}
        self.data_with_wrong_email = {'password': '!@#QWE!@#', 'email': 'test_email'}
        self.valid_data_with_extra = {'username': 'new_user', 'email': 'test_email@mail.su', 'password': '!@#QWE!@#'}
        self.serializer = TokenCreateSerializer

    def test_create_token_serializer(self):
        """Проверка корректности работы сериализатора для создания пользователя"""
        serializer = self.serializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), 'Данные валидны но сериализатор их не принимает')
        serializer = self.serializer(data=self.data_without_email)
        self.assertFalse(serializer.is_valid(), 'Не передан email, но сериализатор это игнорирует')
        serializer = self.serializer(data=self.data_with_wrong_email)
        self.assertFalse(serializer.is_valid(), 'Передан невалидный email, но сериализатор это игнорирует')
        serializer = self.serializer(data=self.data_without_password)
        self.assertFalse(serializer.is_valid(), 'Не передан password, но сериализатор это игнорирует')
        serializer = self.serializer(data=self.valid_data_with_extra)
        self.assertTrue(serializer.is_valid(), 'Сериализатор не игнорирует лишние переданные поля')