from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        )
    first_name = models.CharField(
        'Имя',
        max_length=150
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150
    )

    def __str__(self):
        return self.username
