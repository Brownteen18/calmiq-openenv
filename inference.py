import os
import uvicorn

from server.app import app

if __name__ == "__main__":
    port = int(os.getenv("PORT", "7860"))
    uvicorn.run("server.app:app", host="0.0.0.0", port=port)
<<<<<<< HEAD
import requests
import os
from openai import OpenAI

try:
    client = OpenAI()
except Exception as e:
    print(f"Failed to initialize OpenAI client: {e}")
    client = None

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:7861")
MODEL_NAME = os.getenv("MODEL_NAME", "dummy")
HF_TOKEN = os.getenv("HF_TOKEN", "dummy")

ACTIONS = ["meditate", "exercise", "journal", "sleep", "talk"]


def run_task(task_name):
    # Reset environment
    try:
        requests.post(
            f"{API_BASE_URL}/reset",
            json={"task": task_name}
        )
    except Exception as e:
        print(f"Error resetting env for task {task_name}: {e}")
        return 0.0

    total_reward = 0

    for _ in range(10):
        action = {"action_type": ACTIONS[_ % len(ACTIONS)]}
        try:
            response = requests.post(f"{API_BASE_URL}/step", json=action)
            response.raise_for_status()
            res = response.json()

            total_reward += res.get("reward", 0)

            if res.get("done", False):
                break
        except Exception as e:
            print(f"Error during step: {e}")
            break

    # Get score from grader
    try:
        response = requests.get(f"{API_BASE_URL}/grader")
        response.raise_for_status()
        score = response.json().get("score", 0.0)
    except Exception as e:
        print(f"Error getting score: {e}")
        score = 0.0
        
    return score


if __name__ == "__main__":
    tasks = ["easy", "medium", "hard"]

    for t in tasks:
        score = run_task(t)
        print(f"Task: {t} -> Score: {score:.2f}")
=======
import os
import uvicorn

from server.app import app

if __name__ == "__main__":
    port = int(os.getenv("PORT", "7860"))
    uvicorn.run("server.app:app", host="0.0.0.0", port=port)

>>>>>>> d57d56c (Fix HF entrypoint by running uvicorn from inference launcher.)
