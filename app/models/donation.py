from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import CharityProjectDonationCommon


class Donation(CharityProjectDonationCommon):
    """Модель пожертвования."""

    CLASS_REPR = 'от {user} {comment:.30}'

    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        """Возвращает строковое представление объекта."""
        base_repr = super().__repr__()
        class_repr = self.CLASS_REPR.format(
            user=self.user_id, comment=self.comment
        )
        return f'{base_repr} {class_repr}'
