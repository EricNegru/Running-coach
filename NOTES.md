## Finding 1: model counts future runs as missed
- Scenario: s01_on_track
- Model/prompt:openai/gpt-oss-20b/ v1
- What it said:
  ```json
  { "on_track": false,
  "issue": "other",
  "reason": "Completed 7.0 km of 13.0 km planned for week 3; Sun run still pending.",
  "advice": "Run the scheduled 6.0 km long run today (Sun) at the target pace of 7:30/km. If you feel fatigued, consider a slightly slower pace or split the run into two segments with a short walk break."
  }
  ```
- Why it's wrong: The model does not take into account runs that have not happened yet and gives a final verdict before the week ends. Another error was that its advice says "today (Sun)", but the prompt itself says today is Friday.
- Hypothesis for v2: In v2 I will specifically mention how runs planned for later in the week should be treated, because so far they counted as missing.