from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import AllDonationsDB, DonationCreate, DonationDB
from app.services.investment import allocate_donation_funds

DONATIONS_SUMMARY = "Список пожертвований"
CREATE_DONATION_SUMMARY = "Создать пожертвование"
USERS_DONATION_SUMMARY = "Список пожертвований пользователя"

router = APIRouter()


@router.get(
    "/",
    response_model=List[AllDonationsDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary=DONATIONS_SUMMARY,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Просмотр списка всех пожертвований. Только для суперюзеров."""
    return await donation_crud.get_all(session=session)


@router.post(
    "/",
    response_model=DonationDB,
    response_model_exclude_none=True,
    summary=CREATE_DONATION_SUMMARY,
)
async def create_donation(
    donation_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Создать пожертвование."""
    new_donation = await donation_crud.create(
        obj_in=donation_in, session=session, user=user, commit=False
    )
    not_fully_funded_projects = await charity_project_crud.get_not_closed(
        session=session
    )
    session.add_all(
        allocate_donation_funds(
            target=new_donation, sources=not_fully_funded_projects
        )
    )
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    "/my", response_model=List[DonationDB], summary=USERS_DONATION_SUMMARY
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Посмотреть список пожертвований текущего пользователя."""
    return await donation_crud.get_user_donations(user=user, session=session)
