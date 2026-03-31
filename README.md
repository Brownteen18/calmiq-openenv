---
title: CalmIQ OpenEnv
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
---

# CalmIQ OpenEnv

CalmIQ OpenEnv is a real-world simulation environment for emotional well-being optimization.

## Features
- Multi-task environment (easy, medium, hard)
- Reward shaping with trade-offs
- REST API for agent interaction

## Endpoints
- /reset
- /step
- /tasks
- /grader
- /docs

## Action Space
- meditate
- exercise
- journal
- sleep
- talk

## State Variables
- mood (0–10)
- stress (0–10)
- energy (0–10)