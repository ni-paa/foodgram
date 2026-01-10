from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from users.constants import (MAX_LENGTH_USER_CHARFIELD, MAX_LENGTH_USER_EMAIL,
                             REDEX_USER_USERNAME,)
from users.validators import validate_username


class User(AbstractUser):
    """Класс кастомных пользователей."""

    email = models.EmailField(
        max_length=MAX_LENGTH_USER_EMAIL,
        verbose_name='Электронная почта',
        help_text='Обязательное поле',
        unique=True,
        blank=False,
        null=False,
    )
    username = models.CharField(
        max_length=MAX_LENGTH_USER_CHARFIELD,
        verbose_name='Никнейм',
        help_text='Обязательное поле',
        unique=True,
        blank=False,
        null=False,
        validators=[RegexValidator(regex=REDEX_USER_USERNAME,
                                   message='Неверный формат Никнейма.'),
                    validate_username])
    first_name = models.CharField(
        max_length=MAX_LENGTH_USER_CHARFIELD,
        verbose_name='Имя',
        help_text='Обязательное поле',
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH_USER_CHARFIELD,
        verbose_name='Фамилия',
        help_text='Обязательное поле',
        blank=False,
        null=False,
    )
    password = models.CharField(
        max_length=MAX_LENGTH_USER_CHARFIELD,
        verbose_name='Пароль',
        help_text='Обязательное поле',
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username', 'last_name',)
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='username_email_unique'
            ),
        )

    def __str__(self):
        return self.username


class Follower(models.Model):
    """Класс для подписки на автора."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Пользователь, который подписывается',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        help_text='Автор, на которого подписываются',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='user_author_unique'
            ),
        )

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'
