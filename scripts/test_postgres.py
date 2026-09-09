from sqlalchemy import text

from etl.database.connection import engine


def main() -> None:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))

        # print(result.scalar())
        print(f"Hasil : ${result.scalar()}")


if __name__ == "__main__":
    main()
