"""Управление созданием пользователя."""
from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from users.constants import APP_NAME, MODEL_NAME


class UserManager(BaseUserManager):
    """Менеджер модели пользователя, где email - это идентификатор."""

    def create_user(self, email: str, password=None, **extra_fields):
        """Создает и сохраняет пользователя с заданным email и паролем."""
        if not email:
            raise ValueError(_('Поле Email обязательное.'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        roles = apps.get_model(APP_NAME, MODEL_NAME)
        roles.objects.create(user=user)
        return user

    def create_superuser(self, email: str, password=None, **extra_fields):
        """Создает и сохраняет суперпользователя с заданным email и паролем."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)
