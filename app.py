from fastapi import FastAPI
from pydantic import BaseModel

# ✅ correct imports
from env.environment import CalmIQEnv
from env.models import Action
from env.tasks import get_tasks, grade

app = FastAPI()
env = CalmIQEnv()

# ✅ Request model (THIS FIXES 422)
class ResetRequest(BaseModel):
    task: str = "easy"

# ✅ Correct POST endpoint
@app.post("/reset")
def reset(req: ResetRequest):
    state = env.reset(req.task)
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