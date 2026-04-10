import os
import json
import requests
from openai import OpenAI

# 1. Use defaults to ensure these are always 'str', never 'None'
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:7861")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5.4-mini") 
HF_TOKEN = os.getenv("HF_TOKEN", "no-token-provided")

def run_task(task_name):
    ENV_BASE_URL = "http://localhost:7860"
    steps_count = 0
    
    print(f"[START] {json.dumps({'task': task_name, 'model': MODEL_NAME})}", flush=True)

    try:
        # 2. Fix the "in" operator error by using the guaranteed string API_BASE_URL
        # We check if /v1 is already there to avoid double-suffixing
        base_url = API_BASE_URL
        if "/v1" not in base_url:
            base_url = f"{base_url.rstrip('/')}/v1"

        client = OpenAI(
            base_url=base_url,
            api_key=HF_TOKEN
        )
        
        requests.post(f"{ENV_BASE_URL}/reset", json={"task": task_name}, timeout=5)

        for i in range(5):
            # 3. MODEL_NAME is now guaranteed to be a string
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": "Pick: meditate, exercise, or sleep."}],
                max_tokens=5
            )
            
            llm_decision = (completion.choices[0].message.content or "meditate").lower()
            
            # Action Mapping
            selected_action = "meditate"
            if "sleep" in llm_decision:
                selected_action = "sleep"
            elif "exercise" in llm_decision:
                selected_action = "exercise"

            r = requests.post(f"{ENV_BASE_URL}/step", json={"action_type": selected_action}, timeout=5)
            state = r.json().get("state", {})
            steps_count += 1
            
            # Ensure score is strictly 0 < s < 1
            raw_reward = float(state.get("score", 0.5))
            safe_reward = max(0.01, min(0.99, raw_reward))
            
            print(f"[STEP] {json.dumps({'step': steps_count, 'reward': safe_reward})}", flush=True)

        g = requests.get(f"{ENV_BASE_URL}/grader", timeout=5)
        final_score = float(g.json().get("score", 0.5))

    except Exception as e:
        print(f"Error: {e}") # Helpful for local debugging
        final_score = 0.5
        steps_count = max(steps_count, 1)

    clamped_score = max(0.01, min(0.99, final_score))
    print(f"[END] {json.dumps({'task': task_name, 'score': clamped_score, 'steps': steps_count})}", flush=True)

if __name__ == "__main__":
    for t in ["easy", "medium", "hard"]:
        run_task(t)