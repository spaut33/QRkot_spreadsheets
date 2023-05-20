from fastapi import APIRouter, HTTPException

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

USER_DELETION_ERROR = 'Удаление пользователей запрещено!'

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['Auth'],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['Auth'],
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['Users'],
)


@router.delete('/users/{id}', tags=['Users'], deprecated=True)
def delete_user(user_id: str) -> HTTPException:
    """Не используйте удаление, деактивируйте пользователей."""
    raise HTTPException(status_code=405, detail=USER_DELETION_ERROR)
