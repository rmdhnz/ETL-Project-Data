from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from etl.database.base import Base


class DimCategory(Base):
    __tablename__ = "dim_category"
    __table_args__ = {"schema": "warehouse"}

    category_key: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    category_id: Mapped[int] = mapped_column(
        nullable=False,
        unique=True,
        index=True,
    )

    category_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )