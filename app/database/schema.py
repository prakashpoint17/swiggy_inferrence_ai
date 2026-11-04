
from sqlalchemy import inspect

from app.database.connection import engine


def get_database_schema():

    inspector = inspect(engine)

    schema = {}

    tables = inspector.get_table_names()

    for table in tables:

        columns = inspector.get_columns(table)
        primary_key = inspector.get_pk_constraint(table)
        foreign_keys = inspector.get_foreign_keys(table)
        indexes = inspector.get_indexes(table)

        schema[table] = {
            "columns": [
                {
                    "name": column["name"],
                    "type": str(column["type"]),
                    "nullable": column["nullable"],
                }
                for column in columns
            ],

            "primary_key": primary_key.get(
                "constrained_columns", []
            ),

            "foreign_keys": [
                {
                    "columns": fk["constrained_columns"],
                    "references_table": fk["referred_table"],
                    "references_columns": fk["referred_columns"],
                }
                for fk in foreign_keys
            ],

            "indexes": [
                index["name"]
                for index in indexes
            ],
        }

    return schema


def print_database_schema():

    schema = get_database_schema()

    print("\n========== DATABASE SCHEMA ==========\n")

    for table, details in schema.items():

        print(f"\nTABLE: {table}")

        print("COLUMNS:")

        for column in details["columns"]:
            print(
                f"  {column['name']} "
                f"| {column['type']} "
                f"| Nullable: {column['nullable']}"
            )

        print("PRIMARY KEY:", details["primary_key"])

        print("FOREIGN KEYS:")

        for fk in details["foreign_keys"]:
            print(
                f"  {fk['columns']} -> "
                f"{fk['references_table']}."
                f"{fk['references_columns']}"
            )

        print("INDEXES:", details["indexes"])

    print("\n========== SCHEMA EXTRACTION COMPLETE ==========")


if __name__ == "__main__":
    print_database_schema()
