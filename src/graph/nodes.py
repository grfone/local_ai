from langchain_core.messages import AIMessage, SystemMessage

from src.models.state import AgentState
from src.predictor import Predictor


predictor = Predictor()

QUESTIONING_PROMPT = """
You are the questioning agent.

Your job is to understand what the user wants.

Review the entire conversation before asking a question.

Ask only for information that is still missing.
Do not ask for information the user already provided.

When you have enough information, create a clear final prompt
for another agent to execute the user's request.

Do not perform the user's task yourself.
"""


def questioning(state: AgentState) -> AgentState:
    messages = [
        SystemMessage(content=QUESTIONING_PROMPT),
        *state["messages"],
    ]

    response = predictor.predict(messages)

    return {
        "messages": [AIMessage(content=response)],
        "status": "questioning",
        "final_prompt": None,
    }