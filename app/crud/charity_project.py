from typing import Any, Dict, List

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    """CRUD для работы с благотворительными проектами."""

    async def get_charity_project_by_name(
        self, charity_project_name: str, session: AsyncSession
    ) -> CharityProject:
        """Получение благотворительного проекта по его названию."""
        charity_project = await session.execute(
            select(self.model).where(self.model.name == charity_project_name)
        )
        return charity_project.scalars().first()

    async def get_fully_invested_projects(
        self, session: AsyncSession
    ) -> List[Dict[str, str]]:
        """Получение списка проектов."""
        projects = await session.execute(
            select([CharityProject]).where(CharityProject.fully_invested == 1)
        )
        return projects.scalars().all()

    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> List[Dict[str, Any]]:
        """Получение списка проектов, отсортированных по скорости завершения"""
        projects = await session.execute(
            select([CharityProject])
            .where(CharityProject.fully_invested == 1)
            .order_by(
                func.julianday(CharityProject.close_date) -
                func.julianday(CharityProject.create_date)
            )
        )
        projects = projects.scalars().all()
        return [
            {
                'name': project.name,
                'duration': project.close_date - project.create_date,
                'description': project.description,
            }
            for project in projects
        ]


charity_project_crud = CRUDCharityProject(CharityProject)
