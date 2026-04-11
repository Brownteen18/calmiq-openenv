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
It was developed as a submission for the **Meta PyTorch Hackathon x Scaler School of Technology**.

It enables AI agents to learn how to balance **mood, stress, and energy** through realistic actions and trade-offs.

---

## 🚀 Features

* 🎯 Multi-task environment (Easy → Medium → Hard)
* ⚖️ Realistic trade-offs between actions
* 📊 Reward shaping with partial progress signals
* 🔄 Stateful simulation (step-by-step transitions)
* 🌐 Fully deployed REST API (FastAPI + Docker)
* 🤖 **LiteLLM Proxy Integration** specifically designed for hackathon AST & traffic validations
* ✨ **Hackathon Evaluator Ready** with strictly bounded grader scores and proxy tracking

---

## 🧩 Tasks

| Task   | Objective                                                | Grader Scoring |
| ------ | -------------------------------------------------------- | -------------- |
| Easy   | Increase mood to ≥ 6                                     | (0.01 - 0.99)  |
| Medium | Reduce stress below 4                                    | (0.01 - 0.99)  |
| Hard   | Achieve mood > 7 AND stress < 3 while maintaining energy | (0.01 - 0.99)  |

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

## 🔌 API Endpoints

| Endpoint    | Description           |
| ----------- | --------------------- |
| `/reset`    | Reset environment     |
| `/step`     | Perform an action     |
| `/v1/chat/completions`| Intercepts & handles LLM interactions through Proxy |
| `/grader`   | Get final score       |
| `/docs`     | Swagger UI            |

---

## 🏗️ Project Structure

```
calmiq-openenv/
├── server/
│   └── app.py       # Core FastAPI application & Endpoints
├── env/
│   ├── environment.py
│   ├── models.py
│   └── tasks.py     # Task definitions and strict bounded grader logic
├── inference.py     # Main Entrypoint with Grader Stdout hooks & LLM Proxy registration
├── openenv.yaml
├── Dockerfile
└── README.md
```

---

## ⚙️ Setup (Local)

To run locally and connect to your own proxy:
```bash
pip install -r requirements.txt
export API_KEY="your-proxy-key"
export API_BASE_URL="your-proxy-endpoint" 
python inference.py
```

---

## 🐳 Run with Docker

```bash
docker build -t calmiq .
docker run -p 7860:7860 -e API_KEY="dummy" -e API_BASE_URL="dummy" calmiq
```

---

## 🏁 Conclusion

CalmIQ OpenEnv is a **behavioral simulation platform** that evaluates proxy-integrated agent decision-making under strict multi-objective constraints.

---

## 👤 Author

Built for **Meta PyTorch Hackathon x Scaler School of Technology** 🚀
