"""Тесты приложения api."""
from http import HTTPStatus

from django.test import Client, TestCase


class FoodgramAPITestCase(TestCase):
    """Класс тестирования api foodgram."""

    def setUp(self):
        """Создаёт атрибут класса guest_client."""
        self.guest_client = Client()

    def test_recipes_list(self):
        """Проверка доступности списка рецептов."""
        response = self.guest_client.get('/api/recipes/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_task_creation(self):
        """Проверка доступности списка юзеров."""
        response = self.guest_client.get('/api/users/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
