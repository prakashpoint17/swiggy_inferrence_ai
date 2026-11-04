from app.agents.graph import agent


initial_state = {
    "question": "Which five restaurants have the highest orders?",
    "schema": {},
    "sql": "",
    "results": {},
    "answer": "",
    "error": ""
}


print("\n========== SWIGGY INSIGHT AI ==========\n")

result = agent.invoke(initial_state)


if result.get("error"):

    print("\n========== AGENT ERROR ==========\n")
    print(result["error"])

else:

    print("\n========== GENERATED SQL ==========\n")
    print(result["sql"])

    print("\n========== MYSQL RESULTS ==========\n")
    print(result["results"]["rows"])

    print("\n========== AI BUSINESS ANSWER ==========\n")
    print(result["answer"])