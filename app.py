from fastapi import FastAPI
from env.environment import CalmEnv
from env.models import Action
from env.tasks import get_tasks, grade

app = FastAPI()
env = CalmEnv()
current_task = "easy"

@app.post("/reset")
def reset(task: str = "easy"):
    global current_task
    current_task = task
    state = env.reset(task)
    return {"state": state}

@app.post("/step")
def step(action: Action):
    state, reward, done = env.step(action)
    return {"state": state, "reward": reward, "done": done}

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
    return {"score": grade(env.state, current_task)}

@app.get("/baseline")
def baseline():
    import subprocess
    result = subprocess.check_output(["python", "baseline/run.py"])
    return {"result": result.decode()}