from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема с базовыми полями модели пользователя (кроме пароля):
    id, email, is_active, is_superuser, is_verified."""


class UserCreate(schemas.BaseUserCreate):
    """Схема для создания пользователя; в неё обязательно должны быть переданы
    email и password. Любые другие поля, передаваемые в запросе на создание
    пользователя, будут проигнорированы."""


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для обновления объекта пользователя; содержит все базовые поля
    модели пользователя (в том числе и пароль). Все поля опциональны.
    Если запрос передаёт обычный пользователь (а не суперюзер), то поля
    is_active, is_superuser, is_verified исключаются из набора данных:
    эти три поля может изменить только суперюзер."""
