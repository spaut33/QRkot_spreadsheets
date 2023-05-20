from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_before_delete,
    check_before_update,
    check_name_duplicate,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import allocate_donation_funds

ALL_PROJECTS_SUMMARY = "Список всех проектов"
CREATE_PROJECT_SUMMARY = "Создать проект"
DELETE_PROJECT_SUMMARY = "Удалить проект"
UPDATE_PROJECT_SUMMARY = "Редактировать проект"

router = APIRouter()


@router.get(
    "/",
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
    summary=ALL_PROJECTS_SUMMARY,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
) -> List[CharityProjectDB]:
    """Просмотр списка всех благотворительных проектов."""
    return await charity_project_crud.get_all(session=session)


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary=CREATE_PROJECT_SUMMARY,
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Создает благотворительный проект. Только для суперюзеров."""
    await check_name_duplicate(
        charity_project_name=charity_project.name, session=session
    )
    new_charity_project = await charity_project_crud.create(
        obj_in=charity_project, session=session, commit=False
    )
    session.add_all(
        allocate_donation_funds(
            target=new_charity_project,
            sources=await donation_crud.get_not_closed(session=session),
        )
    )
    await session.commit()
    await session.refresh(new_charity_project)
    return new_charity_project


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary=DELETE_PROJECT_SUMMARY,
)
async def delete_charity_project(
    project_id: int, session: AsyncSession = Depends(get_async_session)
) -> CharityProjectDB:
    """Удаляет благотворительный проект. Только для суперюзеров."""
    charity_project = await check_before_delete(
        charity_project_id=project_id, session=session
    )
    return await charity_project_crud.remove(
        db_obj=charity_project, session=session
    )


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary=UPDATE_PROJECT_SUMMARY,
)
async def update_charity_project(
    project_id: int,
    charity_project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Редактирует благотворительный проект. Только для суперюзеров."""
    charity_project_db = await check_before_update(
        charity_project_id=project_id,
        session=session,
        charity_project_in=charity_project_in,
    )
    return await charity_project_crud.update(
        db_obj=charity_project_db, session=session, obj_in=charity_project_in
    )
