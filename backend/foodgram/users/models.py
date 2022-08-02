from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""
    GUEST = 'guest'
    AUTH_USER = 'auth_user'
    ADMIN = 'admin'

    ROLES = (
        (GUEST, 'guest'),
        (AUTH_USER, 'auth_user'),
        (ADMIN, 'admin'),
    )

    login = models.CharField(
        verbose_name='Логин',
        max_length=200,
        help_text='Введите логин',
        blank=False,
        unique=True,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=128,
        help_text='Введите пароль',
        blank=True,
        null=True,
        default='',
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        help_text='Введите адрес электронной почты',
        blank=False,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Имя',
        max_length=50,
        help_text='Введите имя',
        blank=False,
        null=False,
    )
    surname = models.CharField(
        verbose_name='Фамилия',
        max_length=50,
        help_text='Введите фамилию',
        blank=False,
        null=False,
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        help_text='Введите роль пользователя',
        max_length=16,
        choices=ROLES,
        default='gues',
        blank=False,
        null=False,
    )

    @property
    def is_guest(self):
        return self.role == self.GUEST

    @property
    def is_auth_user(self):
        return self.role == self.AUTH_USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.name, self.login, self.surname
