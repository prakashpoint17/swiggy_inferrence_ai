#first node retrieves the actual database schema.

import json
from app.database.schema import get_database_schema
from app.llm.gemini_client import ask_gemini
from app.tools.sql_validator import validate_sql


def retrieve_schema(state):
    """Retrieve the actual database schema and store it in the state."""
    print("\n[AGENT] Retrieving database schema...")
    
    schema = get_database_schema()
    
    print(f"[AGENT] Retrieved {len(schema)} tables.")
    
    return {
        "schema": schema
    }
    
def generate_sql(state):
    """Generate SQL query using Gemini LLM based on the question and schema."""
    
    print("\n[AGENT] Generating SQL using Gemini...")
    
    question = state["question"]
    schema = state["schema"]
    
    schema_context = json.dumps(schema, indent=2)
    
    prompt = f"""
            You are an expert MySQL 8 database analyst.

            Database: SwiggyDB_new

            ACTUAL DATABASE SCHEMA:
            {schema_context}

            USER QUESTION:
            {question}

            INSTRUCTIONS:
            1. Generate a valid MySQL 8 SELECT query.
            2. Use only tables and columns in the provided schema.
            3. Use correct JOIN conditions based on foreign keys.
            4. Use meaningful column aliases.
            5. Do not generate INSERT, UPDATE, DELETE, DROP or other
            data modification statements.
            6. Return only the SQL query.
            7. Do not include explanations or Markdown code fences.
            """

    sql = ask_gemini(prompt)

    print("[AGENT] SQL generated successfully.")

    return {
        "sql": sql
    }
    
def validate_generated_sql(state):
    """Validate the generated SQL query for safety and correctness."""
    
    print("\n[AGENT] Validating generated SQL...")
    
    sql = state["sql"]
    
    try:
        safe_sql = validate_sql(sql)
        
        return {
                "sql": safe_sql,
                "error": ""
            }
    
    except ValueError as error:

        print("[AGENT] SQL validation failed:", error)

        return {
            "error": str(error)
        }

from app.tools.sql_executor import execute_sql


def execute_generated_sql(state):

    print("\n[AGENT] Executing SQL in MySQL...")

    if state.get("error"):
        print("[AGENT] Execution skipped due to validation error.")
        return {}

    try:
        results = execute_sql(state["sql"])

        print(
            f"[AGENT] Query executed successfully. "
            f"{results['row_count']} rows retrieved."
        )

        return {
            "results": results,
            "error": ""
        }

    except Exception as error:

        print("[AGENT] SQL execution failed:", error)

        return {
            "error": str(error)
        }
        
def generate_answer(state):
    
    print("\n[AGENT] Generating final answer...")

    question = state["question"]
    results = state["results"]

    prompt = f"""
        You are Swiggy Insight AI, an intelligent business analytics assistant.

        USER QUESTION:
        {question}

        DATABASE QUERY RESULTS:
        {results}

        INSTRUCTIONS:
        1. Answer the user's question using only the provided results.
        2. it should be structured and formatted for clarity and readability.
        3. Present numerical information accurately.
        4. Use a clear, professional and concise explanation.
        5. Use a numbered list or table when appropriate.
        6. Do not invent information.
        7. If no records are found, clearly mention that.
        8. not only straight answers also add interpretation a lively chat like response, insights, trends, and recommendations based on the results.

        Generate the final answer.
        """

    answer = ask_gemini(prompt)

    print("[AGENT] Final answer generated.")

    return {
        "answer": answer
    }
    
def route_after_validation(state):
    
    if state.get("error"):
        return "end"
    
    return "execute_sql"

def route_after_execution(state):
    
    if state.get("error"):
        return "end"

    return "generate_answer"