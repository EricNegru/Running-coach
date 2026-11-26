"""Tonight's goal: run one scenario through one model and see a valid answer.

Usage:
    python first_call.py            # uses Gemini
    python first_call.py groq       # uses Groq
"""
import sys

from offtrack.data import load_plan, load_scenarios
from offtrack.llm import ask
from offtrack.prompts import build_prompt_v1


def main() -> None:
    provider = sys.argv[1] if len(sys.argv) > 1 else "gemini"
    scenario = load_scenarios()[0]
    plan = load_plan(scenario.plan)
    system, user = build_prompt_v1(plan, scenario)

    print("=== PROMPT SENT ===")
    print(user)
    print(f"\n=== {provider.upper()} ANSWER ===")
    verdict = ask(provider, system, user)
    print(verdict.model_dump_json(indent=2))

    print("\n=== EXPECTED ===")
    print(scenario.expected.model_dump_json(indent=2))
    match = verdict.on_track == scenario.expected.on_track
    print(f"\non_track matches expected: {match}")


if __name__ == "__main__":
    main()
