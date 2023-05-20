from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate

PROJECT_NOT_FOUND = (
    'Проекта с указанным id <{charity_project_id}> не существует!'
)
PROJECT_NAME_DUPLICATED = 'Проект с таким именем уже существует!'
ALREADY_INVESTED_ERROR = (
    'В проект были внесены средства, не подлежит удалению!'
)
CLOSED_PROJECT_ERROR = 'Закрытый проект нельзя редактировать!'


async def check_exists(
    charity_project_id: int, session: AsyncSession
) -> CharityProject:
    """Проверка наличия проекта в базе."""
    charity_project = await charity_project_crud.get(
        obj_id=charity_project_id, session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail=PROJECT_NOT_FOUND.format(
                charity_project_id=charity_project_id
            ),
        )
    return charity_project


async def check_name_duplicate(
    charity_project_name: str, session: AsyncSession
) -> None:
    """Проверка имени проекта на уникальность."""
    charity_project = await charity_project_crud.get_charity_project_by_name(
        charity_project_name=charity_project_name, session=session
    )
    if charity_project is not None:
        raise HTTPException(status_code=400, detail=PROJECT_NAME_DUPLICATED)


async def check_before_delete(
    charity_project_id: int, session: AsyncSession
) -> CharityProject:
    """Проверка перед удалением на наличие вложенных средств."""
    charity_project = await check_exists(
        charity_project_id=charity_project_id, session=session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(status_code=400, detail=ALREADY_INVESTED_ERROR)
    return charity_project


async def check_before_update(
    charity_project_id: int,
    charity_project_in: CharityProjectUpdate,
    session: AsyncSession,
) -> CharityProject:
    """Проверка перед обновлением на наличие вложенных средств и закрытый"""
    charity_project = await check_exists(
        charity_project_id=charity_project_id, session=session
    )
    if charity_project.close_date is not None:
        raise HTTPException(status_code=400, detail=CLOSED_PROJECT_ERROR)
    full_amount_update_value = charity_project_in.full_amount
    if (
        full_amount_update_value and
        charity_project.invested_amount > full_amount_update_value
    ):
        raise HTTPException(
            status_code=422,
            detail='нельзя установить требуемую сумму меньше уже вложенной.',
        )
    await check_name_duplicate(
        charity_project_name=charity_project_in.name, session=session
    )
    return charity_project
