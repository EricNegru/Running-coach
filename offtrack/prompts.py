"""Prompt versions. Keep each version as its own function so you can compare them."""
from offtrack.data import run_pace, weekly_distance
from offtrack.schemas import Scenario, TrainingPlan

SYSTEM_V1 = (
    "You are a running coach. Decide whether the runner is on track with their "
    "training plan. Respond in JSON with the fields on_track, issue, reason and advice."
)


def format_plan_weeks(plan: TrainingPlan, weeks: list[int]) -> str:
    lines = []
    for w in plan.weeks:
        if w.week in weeks:
            runs = ", ".join(
                f"{r.day} {r.type} {r.distance_km} km @ {r.target_pace}/km" for r in w.runs
            )
            lines.append(f"Week {w.week}: {runs}")
    return "\n".join(lines)


def format_runs(scenario: Scenario) -> str:
    lines = []
    for r in scenario.recent_runs:
        line = f"Week {r.week} {r.day}: {r.distance_km} km in {r.duration} ({run_pace(r)}/km)"
        if r.avg_hr:
            line += f", avg HR {r.avg_hr}"
        if r.note:
            line += f', note: "{r.note}"'
        lines.append(line)
    return "\n".join(lines) or "No runs logged."


def build_prompt_v1(plan: TrainingPlan, scenario: Scenario) -> tuple[str, str]:
    """Returns (system, user). v1 is deliberately plain - your baseline."""
    weeks = sorted({r.week for r in scenario.recent_runs} | {scenario.current_week})
    totals = ", ".join(
        f"week {w}: {weekly_distance(scenario.recent_runs, w)} km" for w in weeks
    )
    user = (
        f"Plan: {plan.name} (goal: {plan.goal})\n\n"
        f"Planned runs:\n{format_plan_weeks(plan, weeks)}\n\n"
        f"Completed runs:\n{format_runs(scenario)}\n\n"
        f"Completed distance by week: {totals}\n"
        f"Today is {scenario.today} of week {scenario.current_week}. "
        f"Runs planned for later this week have not happened yet."
    )
    return SYSTEM_V1, user


# Later today/tomorrow: add build_prompt_v2 (e.g. explicit coaching rules,
# safety instructions for pain, a worked example) and compare it with v1.
