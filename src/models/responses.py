from pydantic import BaseModel
from typing import Literal


class QuestioningResponse(BaseModel):
    status: Literal[
        "needs_clarification",
        "ready",
    ]

    question: str | None = None
    final_prompt: str | None = None