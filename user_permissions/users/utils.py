"""Вспомогательные функции проекта."""


def get_role_length(roles: list[tuple]) -> int:
    """Определение максимальной длины поля role модели Users.

    Принимает на вход список кортежей ('role', 'description').
    'role', 'description' - текстовые поля.
    Возвращает максимальную длину среди всех полей 'role'.
    """
    return max(len(role) for role, _ in roles)
