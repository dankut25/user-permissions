from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.constants import USER_CONSTANTS
from users.models import Roles, User
from permissions.models import BusinessElements, Permissions


class UsersRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя через API."""

    password_confirm = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        max_length=USER_CONSTANTS['email'],
        required=True
    )

    class Meta:
        """Задание полей для сериализации данных."""

        model = User
        fields = [
            'email',
            'password',
            'password_confirm',
            'first_name',
            'last_name',
            'sur_name'
        ]

    def validate_email(self, value):
        """Метод проверки поля email на уникальность."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Указанный \'email\' принадлежит другому пользователю.'
            )
        return value

    def validate_password(self, value):
        """Валидация поля password."""
        if validate_password(value) is None:
            return value

    def validate(self, attrs):
        """Проверка совпадения паролей."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {'password_confirm': 'Указанные пароли не совпадают.'}
            )
        return attrs

    def create(self, validated_data):
        """Создание пользователя после валидации данных."""
        validated_data['password'] = make_password(validated_data['password'])
        user, _ = User.objects.get_or_create(**validated_data)
        roles, _ = Roles.objects.get_or_create(user=user)
        return user


class UsersLoginSerializer(serializers.ModelSerializer):
    """Сериализатор для выдачи токена пользователю через API."""

    email = serializers.EmailField(
        max_length=USER_CONSTANTS['email'],
        required=True
    )

    class Meta:
        """Задание полей для сериализации данных."""

        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        """Метод проверки поля email на уникальность."""
        if User.objects.filter(email=value, is_active=True).exists():
            return value

        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Указанный пользователь еще не зерегистрирован.'
            )
        if User.objects.filter(email=value, is_active=False).exists():
            raise serializers.ValidationError(
                'Данный аккаунт был удален.'
            )
        return value

    def validate(self, attrs):
        """Проверяем указнный пароль для входа."""
        user = User.objects.get(email=attrs['email'])
        if not check_password(attrs['password'], user.password):
            raise serializers.ValidationError(
                {'password': 'Указан неверный пароль.'}
            )
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    class Meta:
        """Meta-класс сериализатора."""

        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'sur_name'
        )

    def update(self, instance, validated_data):
        """Метод обновления данных пользователя.

        Обновляем пользовательские данные, убирая данные о email пользователя
        при PATCH запросе на энд-поинт /users/me/.
        """
        validated_data.pop('email', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class RolesSerializer(serializers.ModelSerializer):
    """Сериализатор модели Roles."""

    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        read_only=True,
        pk_field=serializers.IntegerField()
    )
    user = serializers.SlugRelatedField(
        slug_field='email', queryset=User.objects.all()
    )
    role_id = serializers.ReadOnlyField(source='id')

    class Meta:
        """Meta-класс сериализатора."""

        model = Roles
        fields = ('user_id', 'user', 'role_id', 'role')

    def validate_user(self, value):
        """Запрет на изменение удаленных аккаунтов."""
        if User.objects.filter(email=value, is_active=False).exists():
            raise serializers.ValidationError(
                'Данный аккаунт был удален.'
            )
        return value


class BusinessElementsSerializer(serializers.ModelSerializer):
    """Сериализатор модели BusinessElements."""

    class Meta:
        """Meta-класс сериализатора."""

        model = BusinessElements
        exclude = ('id',)


class PermissionsSerializer(serializers.ModelSerializer):
    """Сериализатор модели Permissions."""

    business_element = serializers.SlugRelatedField(
        slug_field='slug', queryset=BusinessElements.objects.all()
    )

    class Meta:
        """Meta-класс сериализатора."""

        model = Permissions
        fields = '__all__'
