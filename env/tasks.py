def get_tasks():
    return [
        {"name": "easy", "goal": "increase mood to 6+"},
        {"name": "medium", "goal": "reduce stress below 4"},
        {"name": "hard", "goal": "balance mood>7 and stress<3"}
    ]

def grade(state, task):
    score = 0

    if task == "easy":
        score += min(state.mood / 6, 1.0)

    elif task == "medium":
        score += max(0, (8 - state.stress) / 5)
        score += min(state.energy / 10, 0.3)

    elif task == "hard":
        if state.mood > 7:
            score += 0.4
        if state.stress < 3:
            score += 0.4
        if state.energy > 5:
            score += 0.2

    return min(score, 1.0)