import re

import sqlglot
from sqlglot import exp

def extract_sql(response: str) -> str:
    """Extract SQL from Gemini's response."""
    
    match = re.search(
        r"```(?:sql)?\s*(.*?)```",
        response,
        re.IGNORECASE | re.DOTALL
    )
     
    if match:
        match.group(1).strip()
        
    return response.strip()

def validate_sql(sql: str) -> str:
    """Validate SQL and allow only safe read-only queries."""
    
    sql = extract_sql(sql)
    
    if not sql:
        raise ValueError("SQL query is empty.")

    try:
        statements = sqlglot.parse(sql, read="mysql")
    except sqlglot.errors.ParseError as error:
        raise ValueError(f"Invalid SQL syntax: {error}")
    
    # Remove empty statements.
    statements = [statement for statement in statements if statement]

    if len(statements) != 1:
        raise ValueError("Only one SQL statement is allowed.")

    statement = statements[0]

    # Allow only SELECT-based queries.
    if not isinstance(statement, exp.Query):
        raise ValueError("Only SELECT queries are allowed.")

    # Reject potentially unsafe SELECT operations.
    if statement.find(exp.Into):
        raise ValueError("SELECT INTO is not allowed.")

    if statement.find(exp.Lock):
        raise ValueError("Locking queries are not allowed.")

    return statement.sql(dialect="mysql")