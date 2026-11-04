import json

from app.llm.gemini_client import ask_gemini
from app.database.schema import get_database_schema

schema = get_database_schema()

schema_context = json.dumps(schema, indent=2)

system_message = f"""
    You are an expert MySQL database analyst.

    You are working with a MySQL 8 database named SwiggyDB_new.

    Here is the actual database schema:

    {schema_context}

    Instructions:
    1. Generate a valid MySQL 8 SELECT query.
    2. Use only tables and columns present in the schema.
    3. Use correct JOIN conditions based on foreign keys.
    4. Return only the SQL query.
    5. Do not generate INSERT, UPDATE, DELETE or DROP statements.
    """

prompt = f"""

    {system_message}

    User question:
    give Mysql query for the following question:
    Which five restaurants have received the highest number of orders?
    """

try:
    sql = ask_gemini(prompt)
    print(f"Generated SQL Query:\n {sql}")
    
except Exception as e:
    print("Error generating SQL query:", str(e))