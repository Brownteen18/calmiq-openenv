import requests

URL = "http://127.0.0.1:7860"

def smart_action(state):
    if state["stress"] > 6:
        return "meditate"
    elif state["energy"] < 3:
        return "sleep"
    elif state["mood"] < 5:
        return "talk"
    else:
        return "exercise"

def run(task):
    res = requests.post(f"{URL}/reset?task={task}")
    state = res.json()["state"]

    for _ in range(10):
        action = {"action_type": smart_action(state)}
        res = requests.post(f"{URL}/step", json=action)
        state = res.json()["state"]

    score = requests.get(f"{URL}/grader").json()["score"]
    print(f"Task: {task} → Score: {score:.2f}")

if __name__ == "__main__":
    for task in ["easy", "medium", "hard"]:
        run(task)