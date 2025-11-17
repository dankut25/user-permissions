"""Содержание основной модели пользователя."""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .constants import USER_CONSTANTS, ROLE_GUEST, ROLES
from .utils import get_role_length
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Задание расширенной модели пользователя."""

    email = models.EmailField(
        _('Адрес электронной почты'),
        max_length=USER_CONSTANTS['email'],
        unique=True
    )
    first_name = models.CharField(
        _('Имя'), max_length=USER_CONSTANTS['names'], blank=True
    )
    last_name = models.CharField(
        _('Фамилия'), max_length=USER_CONSTANTS['names'], blank=True
    )
    sur_name = models.CharField(
        _('Отчество'), max_length=USER_CONSTANTS['names'], blank=True
    )
    password = models.CharField(
        _('Пароль'), max_length=USER_CONSTANTS['password']
    )
    last_login = models.DateTimeField(
        _('Дата последнего входа'), blank=True, null=True
    )
    is_staff = models.BooleanField(
        _('Статус персонала'),
        default=False,
        help_text=_(
            'Определяет, может ли пользователь войти на страничку '
            'администрирования.'
        ),
    )
    is_active = models.BooleanField(
        _('Активный аккаунт'),
        default=True,
        help_text=_(
            'Указывает на, что текущий аккаунт используется. '
            'Снимите флажок вместо полного удаления данных.'
        )
    )
    date_joined = models.DateTimeField(
        _('Дата регистрации'),
        default=timezone.now
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')

    def __str__(self) -> str:
        return self.email

    def get_full_name(self) -> str:
        """Возвращает first_name и last_name с пробелом между ними."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self) -> str:
        """Возвращает сокращенное имя пользователя."""
        return self.first_name

    def clean(self):
        """Нормализация поля email."""
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def is_admin(self):
        """Определение роли администратора в проекте."""
        return self.is_superuser and self.is_staff


class Roles(models.Model):
    """Задаем роли пользователей."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='roles',
        verbose_name='Пользователь',
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=get_role_length(ROLES),
        choices=ROLES,
        default=ROLE_GUEST,
    )

    class Meta:
        """Meta класс модели User."""

        ordering = ('role',)
        verbose_name = 'Роль в проекте'
        verbose_name_plural = 'Роли'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'role'],
                name='Такая роль у пользователя уже существует.'
            )
        ]
