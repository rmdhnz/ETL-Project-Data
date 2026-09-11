from etl.database.models.source import (
    Category,
    Customer,
    Order,
    OrderItem,
    Payment,
    Product,
)

# from etl.database.session import SessionLocal
from etl.database.connection import SessionLocal
from sqlalchemy import func, select
from sqlalchemy.orm import Session


def total_data(session: Session) -> dict[str, int]:
    tables = (Category, Customer, Order, OrderItem, Payment, Product)

    return {
        table.__tablename__: session.scalar(select(func.count()).select_from(table))
        or 0
        for table in tables
    }


def main() -> None:
    with SessionLocal() as session:
        for table_name, row_count in total_data(session).items():
            print(f"{table_name}: {row_count}")


if __name__ == "__main__":
    main()
