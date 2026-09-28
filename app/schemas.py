from pydantic import BaseModel, Field
from typing import Optional


class UserInput(BaseModel):
    username: str = Field(..., min_length=2, max_length=100)
    user_id: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., ge=10, le=100)
    weight: float = Field(..., gt=20, le=300)
    goal: str = Field(..., min_length=2, max_length=200)
    intensity: str = Field(default="moderate", max_length=50)


class FeedbackInput(BaseModel):
    user_id: str = Field(..., min_length=2, max_length=50)
    feedback: str = Field(..., min_length=2, max_length=2000)


class WorkoutResponse(BaseModel):
    success: bool
    user_id: str
    workout_plan: Optional[str] = None
    nutrition_tip: Optional[str] = None


class FeedbackResponse(BaseModel):
    success: bool
    user_id: str
    updated_plan: Optional[str] = None