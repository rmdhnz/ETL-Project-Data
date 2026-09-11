from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from etl.database.base import Base


class FactSales(Base):
    __tablename__ = "fact_sales"
    __table_args__ = {"schema": "warehouse"}

    sales_key: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    date_key: Mapped[int] = mapped_column(
        ForeignKey("warehouse.dim_date.date_key"),
        nullable=False,
        index=True,
    )

    customer_key: Mapped[int] = mapped_column(
        ForeignKey("warehouse.dim_customer.customer_key"),
        nullable=False,
        index=True,
    )

    product_key: Mapped[int] = mapped_column(
        ForeignKey("warehouse.dim_product.product_key"),
        nullable=False,
        index=True,
    )

    order_id: Mapped[int] = mapped_column(
        nullable=False,
        index=True,
    )

    order_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
        default=0,
    )

    sales_amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )
