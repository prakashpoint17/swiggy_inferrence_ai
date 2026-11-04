# For our Swiggy agent, the state will hold:
# Field	Purpose
# question -	User's natural-language question
# schema -	Database schema context
# sql -	Gemini-generated SQL
# results -	MySQL query results
# answer -	Final natural-language response
# error -	Error information

from typing import TypedDict, Any

class AgentStates(TypedDict):
    question: str
    schema: dict[str, Any]
    sql: str
    results: dict[str, Any]
    answer: str
    error: str
    