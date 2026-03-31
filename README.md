---
title: CalmIQ OpenEnv
emoji: "🧠"
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
---

# 🧠 CalmIQ OpenEnv

CalmIQ OpenEnv is a **real-world simulation environment** designed to model emotional well-being and decision-making.
It enables AI agents to learn how to balance **mood, stress, and energy** through realistic actions and trade-offs.

---

## 🚀 Features

* 🎯 Multi-task environment (Easy → Medium → Hard)
* ⚖️ Realistic trade-offs between actions
* 📊 Reward shaping with partial progress signals
* 🔄 Stateful simulation (step-by-step transitions)
* 🌐 Fully deployed REST API (FastAPI + Docker)
* 🧪 Baseline agent for reproducible evaluation

---

## 🧩 Tasks

| Task   | Objective                                                |
| ------ | -------------------------------------------------------- |
| Easy   | Increase mood to ≥ 6                                     |
| Medium | Reduce stress below 4                                    |
| Hard   | Achieve mood > 7 AND stress < 3 while maintaining energy |

---

## 🎮 Action Space

Agents can perform the following actions:

* **meditate** → Improves mood, reduces stress, costs energy
* **exercise** → Boosts mood significantly, reduces stress, high energy cost
* **journal** → Small mood boost, reduces stress
* **sleep** → Restores energy, slightly reduces stress
* **talk** → Improves mood, reduces energy

---

## 📊 Observation Space

Each step returns the current state:

* `mood` (0–10) → Emotional state
* `stress` (0–10) → Stress level
* `energy` (0–10) → Available energy
* `step_count` → Current timestep
* `task_type` → Active task

---

## 🏆 Reward Function

The reward is designed to guide agents toward balanced behavior:

* ✅ Higher mood → positive reward
* ✅ Lower stress → positive reward
* ✅ Higher energy → small positive reward
* ⚠️ Step penalty to discourage long sequences
* 🔥 Fatigue penalty when energy is low
* 🚫 Anti-over-optimization penalty for unrealistic perfect states

---

## 🔌 API Endpoints

| Endpoint    | Description           |
| ----------- | --------------------- |
| `/reset`    | Reset environment     |
| `/step`     | Perform an action     |
| `/state`    | Get current state     |
| `/tasks`    | List tasks and schema |
| `/grader`   | Get final score       |
| `/baseline` | Run baseline agent    |
| `/docs`     | Swagger UI            |

---

## 🧪 Example Usage

```bash
curl -X POST "http://localhost:7860/step" \
-H "Content-Type: application/json" \
-d '{"action_type": "meditate"}'
```

---

## 🏗️ Project Structure

```
calmiq-openenv/
├── app.py
├── env/
│   ├── environment.py
│   ├── models.py
│   └── tasks.py
├── inference.py
├── openenv.yaml
├── Dockerfile
└── README.md
```

---

## ⚙️ Setup (Local)

```bash
pip install -r requirements.txt
python -m uvicorn app:app --reload --port 7860
```

---

## 🐳 Run with Docker

```bash
docker build -t calmiq .
docker run -p 7860:7860 calmiq
```

---

## 🎯 Design Philosophy

CalmIQ models **real-world human decision-making**, where:

* Improving one factor (e.g., mood) may reduce another (energy)
* Perfect optimization is penalized
* Agents must learn **balanced strategies**

---

## 🏁 Conclusion

CalmIQ OpenEnv is not a toy environment — it is a **behavioral simulation platform** that challenges AI agents to make **realistic, multi-objective decisions** under constraints.

---

## 👤 Author

Built for OpenEnv Hackathon 🚀
