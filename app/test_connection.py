from sqlalchemy import inspect
from app.database.connection import engine

try:
    inspector = inspect(engine)

    print("MySQL connected successfully!")

    print("\nAvailable tables:")

    for table in inspector.get_table_names():
        print("-", table)

except Exception as error:
    print("Connection failed:", error)