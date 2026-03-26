from pydantic import BaseModel
from typing import Literal

class State(BaseModel):
    mood: int
    stress: int
    energy: int
    step_count: int
    task_type: str

class Action(BaseModel):
    action_type: Literal["meditate", "exercise", "journal", "sleep", "talk"]

class StepResponse(BaseModel):
    state: State
    reward: float
    done: bool