from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
from env.environment import CalmIQEnv
from env.models import Action
from env.tasks import get_tasks, grade

app = FastAPI()
env = CalmIQEnv()

class ResetRequest(BaseModel):
    task: Optional[str] = "easy"

@app.post("/reset")
def reset(req: Optional[ResetRequest] = None, task: str = Query(default="easy")):
    # ✅ handle both body + query
    task_type = req.task if req and req.task else task
    state = env.reset(task_type)
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

@app.get("/baseline")
def baseline():
    import subprocess
    result = subprocess.check_output(["python", "baseline/run.py"])
    return {"result": result.decode()}

@app.get("/")
def home():
    return {
        "message": "CalmIQ OpenEnv is running 🚀",
        "endpoints": ["/reset", "/step", "/tasks", "/grader", "/docs"]
    }