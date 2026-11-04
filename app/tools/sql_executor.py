from sqlalchemy import text

from app.database.connection import engine
from app.tools.sql_validator import validate_sql

def execute_sql(sql: str):
    """Validate and execute a read-only SQL query."""
    
    safe_sql = validate_sql(sql)
    
    with engine.connect() as connection:
        result = connection.execute(text(safe_sql))
        rows = result.fetchall()
        columns = list(result.keys())
        
    return {
        "columns": columns,
        "rows": [dict(zip(columns, row)) for row in rows],
        "row_count": len(rows)
    }
    
    