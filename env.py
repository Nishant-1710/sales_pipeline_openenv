import numpy as np
from models import Action, LeadState, StepResponse

class SalesPipelineEnv:
    def __init__(self):
        self.max_steps = 15
        self.reset()

    def reset(self, task_difficulty="random"):
        self.current_step = 0
        # Scenario Generation
        if task_difficulty == "easy":
            self.internal_state = {"budget": 0.9, "sentiment": 0.8, "urgency": 0.9, "busy": False}
        elif task_difficulty == "medium":
            self.internal_state = {"budget": 0.8, "sentiment": 0.2, "urgency": 0.4, "busy": False}
        else: # Hard/Random
            self.internal_state = {
                "budget": np.random.beta(2, 5), # Real-world distribution: few high-budget leads
                "sentiment": np.random.uniform(0.1, 0.6),
                "urgency": np.random.uniform(0.1, 0.9),
                "busy": np.random.choice([True, False], p=[0.3, 0.7])
            }
        return self.get_state()

    def get_state(self) -> LeadState:
        return LeadState(
            lead_id=f"L-{''.join(str(np.random.randint(0,9)) for _ in range(5))}",
            budget_score=self.internal_state["budget"],
            sentiment_score=self.internal_state["sentiment"],
            urgency_score=self.internal_state["urgency"],
            consultant_busy=self.internal_state["busy"],
            steps_taken=self.current_step
        )

    def step(self, action: Action) -> StepResponse:
        self.current_step += 1
        reward = 0.0
        done = False
        info = {"msg": ""}

        # 1. Logic: Lead Decay (Real-world urgency drops over time)
        self.internal_state["urgency"] *= 0.95

        # 2. Action Handling
        if action == Action.HOT_TRANSFER:
            if self.internal_state["busy"]:
                reward = -2.0 # SEVERE PENALTY: Wasted consultant's focus
                info["msg"] = "Critical Failure: Consultant was in a meeting."
                done = True
            elif self.internal_state["budget"] > 0.7 and self.internal_state["sentiment"] > 0.6:
                reward = 5.0 # BIG WIN: Closed a qualified lead
                info["msg"] = "Sale Closed: High-value lead transferred."
                done = True
            else:
                reward = -1.5 # PENALTY: Transferred a 'junk' lead
                info["msg"] = "Failure: Consultant rejected the low-quality lead."
                done = True

        elif action == Action.NURTURE:
            # Partial Progress Signal (Requirement for Meta)
            if self.internal_state["sentiment"] < 0.8:
                self.internal_state["sentiment"] += 0.15
                reward = 0.5 
                info["msg"] = "Progress: Sentiment improved."
            else:
                reward = -0.1 # Waste of time nurturing someone already ready
                info["msg"] = "Inefficient: Lead was already ready for transfer."

        elif action == Action.DISCARD:
            if self.internal_state["budget"] < 0.3:
                reward = 1.0 # GOOD CALL: Filtered out junk
                done = True
            else:
                reward = -3.0 # BAD CALL: Discarded a potential whale
                done = True

        if self.current_step >= self.max_steps:
            done = True
            if reward == 0: reward = -0.5 # Penalty for indecision

        return StepResponse(observation=self.get_state(), reward=reward, done=done, info=info)