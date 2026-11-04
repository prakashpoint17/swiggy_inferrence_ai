from app.agents.nodes import retrieve_schema

initial_state = {
    "question": "Which five restaurants have the highest orders?",
    "schema": {},
    "sql": "",
    "results": {},
    "answer": "",
    "error": ""
}

updated_state = retrieve_schema(initial_state)

print("\n========== AGENT STATE TEST ==========")

print("Question:", initial_state["question"])
print("Schema tables:", list(updated_state["schema"].keys()))
print("Total tables:", len(updated_state["schema"]))