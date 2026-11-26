"""Loading data files and small helpers that don't need an LLM (easy to test)."""
import json
from pathlib import Path

from offtrack.schemas import CompletedRun, Scenario, TrainingPlan

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_plan(filename: str) -> TrainingPlan:
    path = DATA_DIR / "plans" / filename
    return TrainingPlan.model_validate(json.loads(path.read_text()))


def load_scenarios(filename: str = "scenarios.json") -> list[Scenario]:
    path = DATA_DIR / "scenarios" / filename
    return [Scenario.model_validate(s) for s in json.loads(path.read_text())]


def time_to_seconds(text: str) -> int:
    """'6:30' -> 390, '1:02:15' -> 3735."""
    parts = [int(p) for p in text.split(":")]
    if len(parts) == 2:
        minutes, seconds = parts
        return minutes * 60 + seconds
    if len(parts) == 3:
        hours, minutes, seconds = parts
        return hours * 3600 + minutes * 60 + seconds
    raise ValueError(f"Expected mm:ss or hh:mm:ss, got {text!r}")


def seconds_to_pace(seconds: float) -> str:
    """390 -> '6:30'."""
    seconds = round(seconds)
    return f"{seconds // 60}:{seconds % 60:02d}"


def run_pace(run: CompletedRun) -> str:
    """Average pace of a completed run, as 'mm:ss' per km."""
    return seconds_to_pace(time_to_seconds(run.duration) / run.distance_km)


def weekly_distance(runs: list[CompletedRun], week: int) -> float:
    return round(sum(r.distance_km for r in runs if r.week == week), 2)
