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


class Subscribe(models.Model):
    """Модель подписки."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed_author',
        verbose_name='Автор'
    )
    created = models.DateField(
        'Дата подписки',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        models.UniqueConstraint(
            fields=['user', 'author'],
            name='unique_subscribe'
        )

    def __str__(self):
        return f'Пользователь {self.user} подписан на автора {self.author}'
