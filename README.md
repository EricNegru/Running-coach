# Off-track coach

An LLM that reads a runner's training plan and recent runs, decides whether
they're off track, and suggests what to do next, plus an evaluation of how
good and how safe that advice is.

> Work in progress: results table, prompt comparison and "what I'd improve" to come.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then paste in your API keys
```

## Run

```bash
python first_call.py             # one scenario through Gemini
python first_call.py groq        # same scenario through Groq
pytest                           # tests (no API calls)
```

## Layout

```
data/plans/          mock training plans (JSON)
data/scenarios/      test cases: plan + recent runs + expected answer
offtrack/schemas.py  Pydantic models for plans, runs and the model's answer
offtrack/data.py     loading + pace/distance helpers
offtrack/prompts.py  prompt versions (v1 baseline, v2 to come)
offtrack/llm.py      Gemini and Groq calls returning a validated Verdict
tests/               pytest tests for the non-LLM code
```
