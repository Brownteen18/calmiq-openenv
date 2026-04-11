def get_tasks():
    return [
        {"name": "easy", "goal": "increase mood to 6+"},
        {"name": "medium", "goal": "reduce stress below 4 while maintaining energy"},
        {"name": "hard", "goal": "optimize mood > 8, stress < 2, and energy > 7"}
    ]


def grade(state, task):
    score = 0

    # 🟢 EASY TASK - achievable but requires some effort
    if task == "easy":
        # need mood at least 7 for perfect
        if state.mood >= 7:
            score = min((state.mood - 6) / 3, 1.0)
        else:
            score = max(0, (state.mood - 4) / 3)

    # 🟡 MEDIUM TASK - requires balance with trade-offs
    elif task == "medium":
        # stress must be low AND energy must be high
        # but improving one often hurts the other
        if state.stress > 5:
            score = 0
        elif state.energy < 4:
            score = 0
        else:
            # partial credit for reducing stress but losing energy
            stress_reduction = max(0, (8 - state.stress) / 8)
            energy_maintained = max(0, (state.energy - 2) / 8)
            score = min(stress_reduction * 0.6 + energy_maintained * 0.4, 1.0)

    # 🔴 HARD TASK - nearly impossible
    elif task == "hard":
        score = 0

        # ALL conditions must be met and tightly
        mood_ok = state.mood >= 9
        stress_ok = state.stress <= 1
        energy_ok = state.energy >= 8

        if mood_ok and stress_ok and energy_ok:
            score = 1.0
        elif mood_ok and stress_ok and energy_ok >= 7:
            score = 0.7
        elif (mood_ok or stress_ok) and energy_ok:
            score = 0.4
        elif mood_ok or stress_ok:
            score = 0.2
        else:
            score = 0

    return min(max(score, 0.01), 0.99)