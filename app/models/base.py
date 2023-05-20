from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, CheckConstraint

from app.core import constants
from app.core.db import Base


class CharityProjectDonationCommon(Base):
    """Базовый класс для моделей благотворительных проектов и пожертвований."""

    __abstract__ = True

    CLASS_REPR = (
        '{class_name} Инвестиций {full_amount} собрано '
        '{invested_amount} Собрана вся сумма: {fully_invested} Создан: '
        '{create_date} Закрыт: {close_date}'
    )

    full_amount = Column(Integer)
    invested_amount = Column(
        Integer, default=constants.DEFAULT_INVESTED_AMOUNT
    )
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    __table_args__ = (
        CheckConstraint('full_amount > 0', name='check_full_amount_positive'),
        CheckConstraint(
            'invested_amount <= full_amount',
            name='check_invested_amount_not_exceed_full_amount',
        ),
    )

    def __repr__(self):
        return self.CLASS_REPR.format(
            class_name=type(self),
            full_amount=self.full_amount,
            invested_amount=self.invested_amount,
            fully_invested=self.fully_invested,
            create_date=self.create_date,
            close_date=self.close_date,
        )
