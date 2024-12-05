from django.contrib.auth.models import AbstractUser
from django.db import models

from api.constants import MAX_LENGTH_EMAIL, MAX_LENGTH_NAME


class User(AbstractUser):
    """Модель пользователя."""
    email = models.EmailField(
        'email',
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=MAX_LENGTH_NAME,
        unique=True,
        )
    first_name = models.CharField(
        'Имя',
        max_length=MAX_LENGTH_NAME
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=MAX_LENGTH_NAME
    )
    avatar = models.ImageField(
        upload_to='users/',
        null=True,
        default=None
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

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
