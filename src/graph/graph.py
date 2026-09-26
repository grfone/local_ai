# src/graph/graph.py

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from src.graph.nodes import questioning
from src.models.context import AgentContext
from src.models.state import AgentState


CHECKPOINT_DB = ".data/checkpoints.sqlite"


def create_graph(
    checkpointer,
):
    builder = StateGraph(
        AgentState,
        context_schema=AgentContext,
    )

    builder.add_node(
        "questioning",
        questioning,
    )

    builder.add_edge(
        START,
        "questioning",
    )

    builder.add_edge(
        "questioning",
        END,
    )

    return builder.compile(
        checkpointer=checkpointer,
    )


_checkpoint_context = SqliteSaver.from_conn_string(
    CHECKPOINT_DB,
)

checkpointer = _checkpoint_context.__enter__()

graph = create_graph(
    checkpointer,
)