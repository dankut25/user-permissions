"""Модели приложения permissions."""
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import PERMISSIONS_CONSTANTS
from users.constants import ROLES
from users.utils import get_role_length



class BusinessElements(models.Model):
    """Задаем список приложений, к которым будем регулировать доступ."""

    name = models.CharField(
        verbose_name='Название приложения',
        max_length=PERMISSIONS_CONSTANTS['names'],
    )
    slug = models.CharField(
        verbose_name='Короткое имя',
        max_length=PERMISSIONS_CONSTANTS['names'],
        unique=True,
    )

    class Meta:
        """Meta класс модели BusinessElements."""

        ordering = ('name',)
        verbose_name = 'Приложение'
        verbose_name_plural = 'Приложения'

    def __str__(self):
        return self.name


class Permissions(models.Model):
    """Описание прав доступа для приложений и ролей пользователя."""

    business_element = models.ForeignKey(
        BusinessElements, on_delete=models.CASCADE, verbose_name='приложение',
        related_name='business_app', blank=True, null=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=get_role_length(ROLES),
        choices=ROLES
    )
    get_list_permission = models.BooleanField(
        _('Получение списка объектов'), default=False,
    )
    create_obj_permission = models.BooleanField(
        _('Создание объекта'), default=False,
    )
    get_obj_permission = models.BooleanField(
        _('Получение объекта'), default=False,
    )
    update_obj_permission = models.BooleanField(
        _('Обновление объекта'), default=False,
    )
    partial_update_obj_permission = models.BooleanField(
        _('Частичное обновление объекта'), default=False,
    )
    delete_obj_permission = models.BooleanField(
        _('Удаление объекта'), default=False,
    )
    owner_permission = models.BooleanField(
        _('Имеет ли автор отдельный доступ к созданному объекту'),
        default=False
    )

    class Meta:
        """Meta класс модели Permissions."""

        ordering = ('business_element__slug',)
        verbose_name = 'Разрешения'
        verbose_name_plural = 'Разрешения'
        constraints = [
            models.UniqueConstraint(
                fields=['business_element', 'role'],
                name='Права для приложения с такой ролью пользователя '
                'уже заданы.'
            )
        ]
