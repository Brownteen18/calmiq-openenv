from env.models import State, Action, StepResponse
from env.tasks import grade
import random


class CalmIQEnv:
    def __init__(self):
        self.state: State | None = None

    def reset(self, task: str = "easy"):
        self.state = State(
            mood=random.randint(2, 5),
            stress=random.randint(5, 8),
            energy=random.randint(3, 6),
            step_count=0,
            task_type=task
        )
        return self.state

    def step(self, action: Action):
        if self.state is None:
            raise ValueError("Call reset() before step().")

        self.state.step_count += 1

        # 🎯 ACTION EFFECTS WITH TRADE-OFFS
        if action.action_type == "meditate":
            self.state.mood += 0
            self.state.stress -= 2
            self.state.energy -= 1

        elif action.action_type == "exercise":
            self.state.mood += 1
            self.state.stress -= 1
            self.state.energy -= 2

        elif action.action_type == "journal":
            self.state.mood += 0
            self.state.stress -= 1

        elif action.action_type == "sleep":
            self.state.energy += 3
            self.state.stress -= 1

        elif action.action_type == "talk":
            self.state.mood += 1
            self.state.energy -= 1

        # 🔥 FATIGUE PENALTY (REALISM)
        if self.state.energy <= 1:
            self.state.mood -= 1  # burnout effect

        # 🔒 CLAMP VALUES
        self.state.mood = max(0, min(self.state.mood, 10))
        self.state.stress = max(0, min(self.state.stress, 10))
        self.state.energy = max(0, min(self.state.energy, 10))

        # 🎯 BASE REWARD
        reward = 0
        reward += self.state.mood * 0.2
        reward += (10 - self.state.stress) * 0.2
        reward += self.state.energy * 0.1

        # ⚠️ STEP PENALTY
        reward -= 0.3

        # 🔥 ANTI-OVER-OPTIMIZATION PENALTY
        if self.state.mood == 10 and self.state.stress == 0:
            reward -= 2.0
            done = True

        # 🎯 TASK SCORE
        score = grade(self.state, self.state.task_type)

        done = False
        if score >= 1.0 or self.state.step_count >= 6:
            done = True

        # 🚀 WOW DEBUG LOG
        print(
            f"[STEP {self.state.step_count}] Action: {action.action_type}, "
            f"Mood: {self.state.mood}, Stress: {self.state.stress}, "
            f"Energy: {self.state.energy}, Reward: {reward:.2f}"
        )

        return StepResponse(
            state=self.state,
            reward=reward,
            done=done
        )

    def get_state(self):
        return self.state