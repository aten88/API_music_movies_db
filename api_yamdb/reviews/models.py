from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''Переопределенная модель пользователя.
    Добавлены поля bio и confirmation code,
    изменено поле email как обязательное.
    Сделано поле выбора для выбора роли пользователя.
    '''

    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    email = models.EmailField(
        max_length=150,
        unique=True,
        blank=False,
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=40, blank=True, verbose_name='Имя')
    last_name = models.CharField(
        max_length=40, blank=True, verbose_name='Фамилия'
    )
    password = models.CharField(max_length=128, blank=True, null=True)
    bio = models.TextField(
        max_length=280,
        blank=True,
        verbose_name='О себе'
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Роль пользователя'
    )
    confirmation_code = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Код подтверждения'
    )

    def __str__(self):
        return self.username
