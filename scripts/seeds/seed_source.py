from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from random import randint

from faker import Faker
from sqlalchemy import select
from sqlalchemy.orm import Session

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


# ============================================================
# CONFIGURATION
# ============================================================

SEED = 42

CATEGORY_COUNT = 20
CUSTOMER_COUNT = 1_000
PRODUCT_COUNT = 500
ORDER_COUNT = 5_000

MIN_ITEMS_PER_ORDER = 1
MAX_ITEMS_PER_ORDER = 5

BATCH_SIZE = 500


# ============================================================
# RANDOM / FAKER
# ============================================================

fake = Faker("id_ID")
fake.seed_instance(SEED)

random.seed(SEED)


# ============================================================
# CONSTANT DATA
# ============================================================

CATEGORY_NAMES = [
    "Electronics",
    "Clothing",
    "Books",
    "Home & Kitchen",
    "Sports",
    "Beauty",
    "Toys",
    "Automotive",
    "Groceries",
    "Health",
    "Office Supplies",
    "Shoes",
    "Accessories",
    "Pet Supplies",
    "Garden",
    "Furniture",
    "Jewelry",
    "Music",
    "Gaming",
    "Travel",
]

ORDER_STATUSES = [
    "pending",
    "paid",
    "processing",
    "shipped",
    "completed",
    "cancelled",
]

ORDER_STATUS_WEIGHTS = [
    8,
    10,
    10,
    15,
    50,
    7,
]

PAYMENT_METHODS = [
    "qris",
    "bank_transfer",
    "credit_card",
    "debit_card",
    "e_wallet",
]

PAYMENT_METHOD_WEIGHTS = [
    30,
    25,
    15,
    10,
    20,
]

PAYMENT_STATUSES = [
    "paid",
    "pending",
    "failed",
    "refunded",
]


# ============================================================
# HELPERS
# ============================================================


def random_datetime(start: datetime, end: datetime) -> datetime:
    """Return a random datetime between start and end."""

    delta = end - start

    random_seconds = randint(
        0,
        int(delta.total_seconds()),
    )

    return start + timedelta(seconds=random_seconds)


def weighted_choice(values: list[str], weights: list[int]) -> str:
    """Choose a value based on predefined weights."""

    return random.choices(
        values,
        weights=weights,
        k=1,
    )[0]


# ============================================================
# CATEGORY SEED
# ============================================================


def seed_categories(session: Session) -> list[Category]:
    print("Seeding categories...")

    existing_categories = session.scalars(select(Category)).all()

    if existing_categories:
        print(f"  Categories already exist: {len(existing_categories)}")

        return existing_categories

    categories: list[Category] = []

    for name in CATEGORY_NAMES[:CATEGORY_COUNT]:
        category = Category(
            name=name,
            description=f"Products in {name} category.",
        )

        categories.append(category)

    session.add_all(categories)
    session.flush()

    print(f"  Created: {len(categories)} categories")

    return categories


# ============================================================
# CUSTOMER SEED
# ============================================================


def seed_customers(session: Session) -> list[Customer]:
    print("Seeding customers...")

    existing_customers = session.scalars(select(Customer)).all()

    if existing_customers:
        print(f"  Customers already exist: {len(existing_customers)}")

        return existing_customers

    customers: list[Customer] = []

    for index in range(1, CUSTOMER_COUNT + 1):
        first_name = fake.first_name()
        last_name = fake.last_name()

        full_name = f"{first_name} {last_name}"

        customer = Customer(
            customer_code=f"CUST-{index:06d}",
            name=full_name,
            email=f"customer{index:06d}@example.com",
            phone=fake.phone_number(),
        )

        customers.append(customer)

        if len(customers) >= BATCH_SIZE:
            session.add_all(customers)
            session.flush()

            customers.clear()

    if customers:
        session.add_all(customers)
        session.flush()

    result = session.scalars(select(Customer).order_by(Customer.id)).all()

    print(f"  Created: {len(result)} customers")

    return result


# ============================================================
# PRODUCT SEED
# ============================================================


def seed_products(
    session: Session,
    categories: list[Category],
) -> list[Product]:
    print("Seeding products...")

    existing_products = session.scalars(select(Product)).all()

    if existing_products:
        print(f"  Products already exist: {len(existing_products)}")

        return existing_products

    products: list[Product] = []

    for index in range(1, PRODUCT_COUNT + 1):
        category = random.choice(categories)

        price = Decimal(randint(50_000, 5_000_000)).quantize(Decimal("0.01"))

        product = Product(
            category_id=category.id,
            sku=f"SKU-{index:06d}",
            name=f"{fake.word().title()} {category.name} Product {index}",
            description=fake.text(max_nb_chars=200),
            price=price,
            stock_quantity=randint(0, 500),
            is_active=random.random() < 0.95,
        )

        products.append(product)

        if len(products) >= BATCH_SIZE:
            session.add_all(products)
            session.flush()

            products.clear()

    if products:
        session.add_all(products)
        session.flush()

    result = session.scalars(select(Product).order_by(Product.id)).all()

    print(f"  Created: {len(result)} products")

    return result


# ============================================================
# ORDER SEED
# ============================================================


def seed_orders(
    session: Session,
    customers: list[Customer],
) -> list[Order]:
    print("Seeding orders...")

    existing_orders = session.scalars(select(Order)).all()

    if existing_orders:
        print(f"  Orders already exist: {len(existing_orders)}")

        return existing_orders

    orders: list[Order] = []

    start_date = datetime(
        2025,
        1,
        1,
        tzinfo=timezone.utc,
    )

    end_date = datetime(
        2026,
        9,
        1,
        tzinfo=timezone.utc,
    )

    for index in range(1, ORDER_COUNT + 1):
        order_date = random_datetime(
            start_date,
            end_date,
        )

        status = weighted_choice(
            ORDER_STATUSES,
            ORDER_STATUS_WEIGHTS,
        )

        order = Order(
            order_number=f"ORD-{index:08d}",
            customer_id=random.choice(customers).id,
            status=status,
            order_date=order_date,
            total_amount=Decimal("0.00"),
        )

        orders.append(order)

        if len(orders) >= BATCH_SIZE:
            session.add_all(orders)
            session.flush()

            orders.clear()

    if orders:
        session.add_all(orders)
        session.flush()

    result = session.scalars(select(Order).order_by(Order.id)).all()

    print(f"  Created: {len(result)} orders")

    return result


# ============================================================
# ORDER ITEM SEED
# ============================================================


def seed_order_items(
    session: Session,
    orders: list[Order],
    products: list[Product],
) -> None:
    print("Seeding order items...")

    existing_items = session.scalar(select(OrderItem.id).limit(1))

    if existing_items is not None:
        print("  Order items already exist.")

        return

    order_items: list[OrderItem] = []

    for order in orders:
        item_count = randint(
            MIN_ITEMS_PER_ORDER,
            MAX_ITEMS_PER_ORDER,
        )

        selected_products = random.sample(
            products,
            item_count,
        )

        total_amount = Decimal("0.00")

        for product in selected_products:
            quantity = randint(1, 5)

            unit_price = product.price

            subtotal = (unit_price * quantity).quantize(Decimal("0.01"))

            total_amount += subtotal

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=unit_price,
                subtotal=subtotal,
            )

            order_items.append(order_item)

        order.total_amount = total_amount

        if len(order_items) >= BATCH_SIZE:
            session.add_all(order_items)
            session.flush()

            order_items.clear()

    if order_items:
        session.add_all(order_items)
        session.flush()

    print("  Order items created.")


# ============================================================
# PAYMENT SEED
# ============================================================


def seed_payments(
    session: Session,
    orders: list[Order],
) -> None:
    print("Seeding payments...")

    existing_payments = session.scalar(select(Payment.id).limit(1))

    if existing_payments is not None:
        print("  Payments already exist.")

        return

    payments: list[Payment] = []

    for order in orders:
        payment_status = "paid"

        if order.status == "cancelled":
            payment_status = random.choice(["failed", "refunded"])

        elif order.status == "pending":
            payment_status = "pending"

        elif order.status in {
            "paid",
            "processing",
            "shipped",
            "completed",
        }:
            payment_status = "paid"

        paid_at = None

        if payment_status in {
            "paid",
            "refunded",
        }:
            paid_at = order.order_date + timedelta(minutes=randint(5, 180))

        payment = Payment(
            order_id=order.id,
            payment_method=weighted_choice(
                PAYMENT_METHODS,
                PAYMENT_METHOD_WEIGHTS,
            ),
            payment_status=payment_status,
            amount=order.total_amount,
            paid_at=paid_at,
        )

        payments.append(payment)

        if len(payments) >= BATCH_SIZE:
            session.add_all(payments)
            session.flush()

            payments.clear()

    if payments:
        session.add_all(payments)
        session.flush()

    print(f"  Created: {len(orders)} payments")


# ============================================================
# MAIN
# ============================================================


def main() -> None:
    print("=" * 60)
    print("SOURCE DATABASE SEED")
    print("=" * 60)

    with SessionLocal() as session:
        try:
            categories = seed_categories(session)

            customers = seed_customers(session)

            products = seed_products(
                session,
                categories,
            )

            orders = seed_orders(
                session,
                customers,
            )

            seed_order_items(
                session,
                orders,
                products,
            )

            seed_payments(
                session,
                orders,
            )

            session.commit()

            print()
            print("=" * 60)
            print("SEED COMPLETED SUCCESSFULLY")
            print("=" * 60)

        except Exception:
            session.rollback()

            print()
            print("SEED FAILED. Transaction rolled back.")

            raise


if __name__ == "__main__":
    main()
