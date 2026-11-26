"""Data shapes for plans, runs, scenarios and the model's answer.

Pydantic checks every file you load and every answer the model returns,
so bad data fails loudly instead of silently skewing your results.
"""
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

RunType = Literal["easy", "long", "tempo", "intervals", "recovery"]

# The kinds of problem the model can flag. "none" means on track.
Issue = Literal[
    "none",
    "missed_runs",
    "too_fast",
    "distance_jump",
    "pain_or_injury",
    "other",
]


class PlannedRun(BaseModel):
    day: str  # "Mon", "Tue", ...
    type: RunType
    distance_km: float = Field(gt=0)
    target_pace: str  # "mm:ss" per km, e.g. "6:30"


class PlanWeek(BaseModel):
    week: int = Field(ge=1)
    runs: list[PlannedRun]


class TrainingPlan(BaseModel):
    name: str
    goal: str
    weeks: list[PlanWeek]


class CompletedRun(BaseModel):
    """One run the runner actually did (roughly what Strava would give you)."""
    week: int = Field(ge=1)
    day: str
    distance_km: float = Field(gt=0)
    duration: str  # "hh:mm:ss" or "mm:ss"
    avg_hr: Optional[int] = None
    note: Optional[str] = None  # the runner's own comment, e.g. "left knee sore"


class Expected(BaseModel):
    on_track: bool
    issue: Issue
    why: str  # your reasoning as the "coach" - useful when you score the advice


class Scenario(BaseModel):
    id: str
    plan: str  # file name in data/plans/, e.g. "beginner_10k.json"
    current_week: int = Field(ge=1)
    today: str  # day of the week "now", so runs later this week aren't counted as missed
    recent_runs: list[CompletedRun]
    expected: Expected


class Verdict(BaseModel):
    """What the LLM must return. extra="forbid" keeps the JSON schema strict."""
    model_config = ConfigDict(extra="forbid")

    on_track: bool
    issue: Issue
    reason: str = Field(description="One or two sentences citing the runner's data.")
    advice: str = Field(description="Specific, safe next step for this week.")
