from pprint import pprint

from app.tools.sql_executor import execute_sql


query = """
SELECT
    r.RestaurantID,
    r.RestaurantName,
    COUNT(o.OrderID) AS OrderCount
FROM restaurants r
JOIN orders o
    ON r.RestaurantID = o.RestaurantID
GROUP BY r.RestaurantID, r.RestaurantName
ORDER BY OrderCount DESC
LIMIT 5;
"""

try:
    result = execute_sql(query)

    print("\n========== QUERY RESULTS ==========\n")
    print("Columns:", result["columns"])
    print("Total rows:", result["row_count"])

    pprint(result["rows"])

except Exception as error:
    print("Execution failed:", error)