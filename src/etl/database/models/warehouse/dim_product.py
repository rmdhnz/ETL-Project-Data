from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from etl.database.base import Base


class DimProduct(Base):
    __tablename__ = "dim_product"
    __table_args__ = {"schema": "warehouse"}

    product_key: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    product_id: Mapped[int] = mapped_column(
        nullable=False,
        unique=True,
        index=True,
    )

    sku: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    product_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    category_key: Mapped[int] = mapped_column(
        ForeignKey("warehouse.dim_category.category_key"),
        nullable=False,
        index=True,
    )

    current_price: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )