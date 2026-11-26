"""Tests for everything that doesn't need an LLM. Fast, free, run in CI."""
import pytest
from pydantic import ValidationError

from offtrack.data import (
    load_plan,
    load_scenarios,
    run_pace,
    seconds_to_pace,
    time_to_seconds,
    weekly_distance,
)
from offtrack.schemas import CompletedRun, Verdict


def test_time_to_seconds():
    assert time_to_seconds("6:30") == 390
    assert time_to_seconds("1:02:15") == 3735


def test_time_to_seconds_rejects_bad_input():
    with pytest.raises(ValueError):
        time_to_seconds("630")


def test_seconds_to_pace_pads_seconds():
    assert seconds_to_pace(365) == "6:05"


def test_run_pace():
    run = CompletedRun(week=1, day="Tue", distance_km=5, duration="35:00")
    assert run_pace(run) == "7:00"


def test_weekly_distance_only_counts_that_week():
    runs = [
        CompletedRun(week=1, day="Tue", distance_km=3, duration="21:00"),
        CompletedRun(week=2, day="Tue", distance_km=4, duration="28:00"),
        CompletedRun(week=2, day="Sun", distance_km=6.5, duration="48:00"),
    ]
    assert weekly_distance(runs, 2) == 10.5


def test_every_scenario_loads_and_points_to_a_real_plan():
    scenarios = load_scenarios()
    assert scenarios, "no scenarios found"
    ids = [s.id for s in scenarios]
    assert len(ids) == len(set(ids)), "duplicate scenario ids"
    for s in scenarios:
        plan = load_plan(s.plan)
        assert s.current_week <= len(plan.weeks)


def test_verdict_rejects_unknown_issue():
    with pytest.raises(ValidationError):
        Verdict(on_track=False, issue="tired", reason="x", advice="y")


def test_verdict_rejects_extra_fields():
    with pytest.raises(ValidationError):
        Verdict.model_validate(
            {"on_track": True, "issue": "none", "reason": "x", "advice": "y", "mood": "happy"}
        )
