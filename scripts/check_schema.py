from sqlalchemy import inspect
from etl.database.connection import engine


def main():
    inspector = inspect(engine)
    print("\n=== SOURCE TABLES ===")
    for table in inspector.get_table_names(schema="source"):
        print(f" -{table}")

    print("\n=== WAREHOUSE TABLES ===")
    for table in inspector.get_table_names(schema="warehouse"):
        print(f"  - {table}")

if __name__ == '__main__' : 
  main()