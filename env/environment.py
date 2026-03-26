from typing import Optional
import random
from .models import State

class CalmEnv:
    def __init__(self):
        self.state: Optional[State] = None
        self.last_action = None
        self.history = []
        self.personality = None

    def reset(self, task_type="easy"):
        self.personality = random.choice(["anxious", "calm", "energetic"])
        self.history = []
        self.last_action = None

        self.state = State(
            mood=random.randint(2, 5),
            stress=random.randint(5, 8),
            energy=random.randint(3, 6),
            step_count=0,
            task_type=task_type
        )
        return self.state

    def step(self, action):
        # ✅ FIX: ensure state is initialized
        if self.state is None:
            raise ValueError("Environment not initialized. Call reset() first.")

        old_state: State = self.state  # ✅ proper typing

        mood = old_state.mood
        stress = old_state.stress
        energy = old_state.energy

        # 🌍 Random events
        event = random.choice(["none", "bad_news", "good_news"])
        if event == "bad_news":
            stress += 2
            mood -= 1
        elif event == "good_news":
            mood += 2

        # 🎯 Actions
        if action.action_type == "meditate":
            stress -= 2
            mood += 1

        elif action.action_type == "exercise":
            stress -= 1
            mood += 2
            energy -= 1

        elif action.action_type == "journal":
            mood += 1

        elif action.action_type == "sleep":
            energy += 2
            stress -= 1

        elif action.action_type == "talk":
            mood += 2
            stress -= 1

        # 🧠 Personality
        if self.personality == "anxious":
            stress += 1
        elif self.personality == "energetic":
            energy += 1

        # 🔒 Clamp
        mood = max(0, min(10, mood))
        stress = max(0, min(10, stress))
        energy = max(0, min(10, energy))

        # 🔥 Reward
        reward = 0
        reward += (mood - old_state.mood) * 1.5
        reward += (old_state.stress - stress) * 2.0
        reward += (energy - old_state.energy) * 0.5

        # 🚫 Repeat penalty
        if action.action_type == self.last_action:
            reward -= 0.5

        # ⭐ WOW factor (memory)
        self.history.append(action.action_type)
        if self.history.count(action.action_type) > 3:
            reward -= 1.0

        # 🚫 High stress penalty
        if stress > 8:
            reward -= 1.0

        # 🎉 Bonus
        if mood >= 8 and stress <= 3:
            reward += 3.0

        self.last_action = action.action_type

        # ✅ Update state
        self.state = State(
            mood=mood,
            stress=stress,
            energy=energy,
            step_count=old_state.step_count + 1,
            task_type=old_state.task_type
        )

        done = self.state.step_count >= 10 or mood >= 8

        # 📊 Logging
        print(f"[STEP {self.state.step_count}] Action: {action.action_type}, Mood: {mood}, Stress: {stress}, Reward: {reward:.2f}")

        return self.state, reward, done