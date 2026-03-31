import requests
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:7860")
MODEL_NAME = os.getenv("MODEL_NAME", "dummy")
HF_TOKEN = os.getenv("HF_TOKEN", "dummy")

ACTIONS = ["meditate", "exercise", "journal", "sleep", "talk"]


def run_task(task_name):
    # Reset environment
    requests.get(f"{API_BASE_URL}/reset")

    total_reward = 0

    for _ in range(10):
        action = {"action_type": ACTIONS[_ % len(ACTIONS)]}
        res = requests.post(f"{API_BASE_URL}/step", json=action).json()

        total_reward += res["reward"]

        if res["done"]:
            break

    # Get score from grader
    score = requests.get(f"{API_BASE_URL}/grader").json()["score"]
    return score


if __name__ == "__main__":
    tasks = ["easy", "medium", "hard"]

    for t in tasks:
        score = run_task(t)
        print(f"Task: {t} → Score: {score:.2f}")