from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn

from env.environment import CalmIQEnv
from env.models import Action
from env.tasks import get_tasks, grade

app = FastAPI()
env = CalmIQEnv()

class ResetRequest(BaseModel):
    task: Optional[str] = "easy"

@app.post("/reset")
def reset(req: Optional[ResetRequest] = None):
    task = req.task if req and req.task else "easy"
    state = env.reset(task)
    return {"state": state}

@app.post("/step")
def step(action: Action):
    env.step(action)
    return {"state": env.state}

@app.get("/state")
def state():
    return {"state": env.state}

@app.get("/tasks")
def tasks():
    return {
        "tasks": get_tasks(),
        "action_schema": {
            "action_type": ["meditate", "exercise", "journal", "sleep", "talk"]
        }
    }

@app.get("/grader")
def grader():
    if env.state is None:
        return {"score": 0}
    return {"score": grade(env.state, env.state.task_type)}


# ✅ REQUIRED FOR OPENENV
def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


# ✅ REQUIRED ENTRY POINT
if __name__ == "__main__":
    main()