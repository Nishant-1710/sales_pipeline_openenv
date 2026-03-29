from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from enum import Enum

class Action(str, Enum):
    DISCARD = "discard"
    NURTURE = "nurture"
    HOT_TRANSFER = "hot_transfer"

class LeadState(BaseModel):
    lead_id: str
    budget_score: float = Field(..., ge=0, le=1)
    sentiment_score: float = Field(..., ge=0, le=1)
    urgency_score: float = Field(..., ge=0, le=1)
    consultant_busy: bool
    steps_taken: int
    is_hot: bool = False

class StepResponse(BaseModel):
    observation: LeadState
    reward: float
    done: bool
    info: Dict