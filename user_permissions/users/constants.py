"""Константы для Users."""
ROLE_GUEST = 'guest'
ROLE_USER: str = 'user'
ROLE_MANAGER: str = 'manager'
ROLE_ADMIN: str = 'admin'
ROLES = [
    (ROLE_GUEST, 'Гость'),
    (ROLE_USER, 'Активный пользователь'),
    (ROLE_MANAGER, 'Менеджер'),
    (ROLE_ADMIN, 'Администратор'),
]
USER_CONSTANTS = {
    "password": 128,
    "names": 150,
    "email": 254
}
APP_NAME = 'users'
MODEL_NAME = 'Roles'
USER_LOGIN_REGISTER_DELETE = ['POST']
USER_UPDATE_METHODS_LIST = ['GET', 'PATCH']
USER_ROLES_METHODS = ['get', 'post', 'patch', 'delete']
