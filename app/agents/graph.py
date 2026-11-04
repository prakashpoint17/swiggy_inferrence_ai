from langgraph.graph import StateGraph, START, END

from app.agents.state import AgentStates
from app.agents.nodes import (retrieve_schema,
                              generate_sql,
                              validate_generated_sql,
                              execute_generated_sql,
                              generate_answer,
                              route_after_validation,
                              route_after_execution)

# Create the graph
builder = StateGraph(AgentStates)

# Register the node
builder.add_node("retrieve_schema", retrieve_schema)
builder.add_node("generate_sql", generate_sql)
builder.add_node("validate_sql", validate_generated_sql)
builder.add_node("execute_sql", execute_generated_sql)
builder.add_node("generate_answer", generate_answer)


# Define execution flow
builder.add_edge(START, "retrieve_schema")
builder.add_edge("retrieve_schema", "generate_sql")
builder.add_edge("generate_sql", "validate_sql")

# Conditional routing after validation
builder.add_conditional_edges(
    "validate_sql",
    route_after_validation,
    {
        "execute_sql": "execute_sql",
        "end": END
    }
)


# Conditional routing after execution
builder.add_conditional_edges(
    "execute_sql",
    route_after_execution,
    {
        "generate_answer": "generate_answer",
        "end": END
    }
)


builder.add_edge("generate_answer", END)

# Compile the graph
agent = builder.compile()