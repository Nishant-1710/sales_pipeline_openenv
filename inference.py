import os
from env import SalesPipelineEnv
from models import Action

def run_baseline():
    env = SalesPipelineEnv()
    tasks = ["easy", "medium", "hard"]
    
    print("--- STARTING OPENENV BASELINE EVALUATION ---")
    for task in tasks:
        state = env.reset(task_difficulty=task)
        total_reward = 0
        done = False
        
        while not done:
            # Heuristic 'Closer' Logic
            if state.budget_score > 0.7 and state.sentiment_score > 0.6 and not state.consultant_busy:
                action = Action.HOT_TRANSFER
            elif state.budget_score > 0.6 and state.sentiment_score <= 0.6:
                action = Action.NURTURE
            else:
                action = Action.DISCARD
            
            resp = env.step(action)
            state = resp.observation
            total_reward += resp.reward
            done = resp.done
            
        print(f"Task: {task.upper()} | Score: {total_reward:.2f} | Success: {total_reward > 0}")

if __name__ == "__main__":
    run_baseline()