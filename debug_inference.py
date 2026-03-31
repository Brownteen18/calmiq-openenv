import requests
import os
from env.models import State
from env.tasks import grade

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:7861")
ACTIONS = ["meditate", "exercise", "journal", "sleep", "talk"]

def test_task(task_name):
    print(f"\n=== Testing {task_name} task ===")
    requests.get(f"{API_BASE_URL}/reset", params={"task": task_name})

    final_state = None
    for i in range(10):
        action = {"action_type": ACTIONS[i % len(ACTIONS)]}
        res = requests.post(f"{API_BASE_URL}/step", json=action).json()
        state = res["state"]
        final_state = State(**state)
        print(f"Step {i+1}: mood={state['mood']}, stress={state['stress']}, energy={state['energy']}")

    # Call grade directly
    local_score = grade(final_state, task_name)
    print(f"Local grade() call: {local_score}")
    
    score_res = requests.get(f"{API_BASE_URL}/grader").json()
    print(f"Server /grader endpoint: {score_res['score']}")

if __name__ == "__main__":
    test_task("easy")
    test_task("medium")
    test_task("hard")
