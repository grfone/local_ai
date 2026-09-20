from langgraph.graph import StateGraph, START, END

from src.models.state import AgentState
from src.graph.nodes import questioning


builder = StateGraph(AgentState)

# States
builder.add_node("questioning", questioning)

# Connections
builder.add_edge(START, "questioning")
builder.add_edge("questioning", END)

graph = builder.compile()