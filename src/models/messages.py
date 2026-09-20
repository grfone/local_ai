from pydantic import BaseModel, Field
from typing import Literal


MessageRole = Literal["system", "user", "assistant"]


class Message(BaseModel):
    role: MessageRole
    content: str