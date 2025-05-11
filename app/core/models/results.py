from datetime import date

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Date, Integer, UniqueConstraint

from .base import Base

class Results(Base):
    __tablename__ = 'results'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    competition: Mapped[int] = mapped_column(Integer, nullable=False)
    home_team: Mapped[str] = mapped_column(String(50), nullable=False)
    away_team: Mapped[str] = mapped_column(String(50), nullable=False)
    score_home: Mapped[int] = mapped_column(Integer, nullable=False)
    score_away: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)

    __table_args__ = (
        UniqueConstraint('home_team', 'away_team', 'date', name='uq_home_away_date'),
    )