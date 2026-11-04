from app.tools.sql_validator import validate_sql


test_queries = [
    {
        "name": "Valid SELECT",
        "sql": "SELECT * FROM customers",
        "expected": "PASS"
    },
    {
        "name": "Valid JOIN",
        "sql": """
            SELECT r.RestaurantName, COUNT(o.OrderID)
            FROM restaurants r
            JOIN orders o
            ON r.RestaurantID = o.RestaurantID
            GROUP BY r.RestaurantName
        """,
        "expected": "PASS"
    },
    {
        "name": "Valid CTE",
        "sql": """
            WITH customer_orders AS (
                SELECT CustomerID, COUNT(*) AS total
                FROM orders
                GROUP BY CustomerID
            )
            SELECT * FROM customer_orders
        """,
        "expected": "PASS"
    },
    {
        "name": "Unsafe DELETE",
        "sql": "DELETE FROM customers",
        "expected": "BLOCK"
    },
    {
        "name": "Unsafe DROP",
        "sql": "DROP TABLE customers",
        "expected": "BLOCK"
    },
    {
        "name": "Multiple statements",
        "sql": "SELECT * FROM customers; DELETE FROM customers;",
        "expected": "BLOCK"
    }
]


for test in test_queries:

    print(f"\nTest: {test['name']}")

    try:
        result = validate_sql(test["sql"])

        print("Status: PASS")
        print("Validated SQL:", result)

        if test["expected"] == "BLOCK":
            print("ERROR: Unsafe query was accepted!")

    except ValueError as error:

        print("Status: BLOCKED")
        print("Reason:", error)

        if test["expected"] == "PASS":
            print("ERROR: Valid query was rejected!")