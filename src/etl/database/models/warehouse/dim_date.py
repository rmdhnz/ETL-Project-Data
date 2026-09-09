from datetime import date

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from etl.database.base import Base


class DimDate(Base):
    __tablename__ = "dim_date"
    __table_args__ = {"schema": "warehouse"}

    date_key: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    full_date: Mapped[date] = mapped_column(
        nullable=False,
        unique=True,
    )

    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    quarter: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    month: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    month_name: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    week: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    day: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    day_name: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    is_weekend: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )