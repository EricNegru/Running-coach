"""One function per provider, both returning a validated Verdict.

The SDK imports live inside the functions so tests can import this module
without needing API keys or network access.
"""
import json
import os

from dotenv import load_dotenv

from offtrack.schemas import Verdict

load_dotenv()


def ask_gemini(system: str, user: str, model: str | None = None) -> Verdict:
    from google import genai
    from google.genai import types

    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"],
        http_options=types.HttpOptions(timeout=60000),
        )
    response = client.models.generate_content(
        model=model or os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
        contents=user,
        config=types.GenerateContentConfig(
            system_instruction=system,
            response_mime_type="application/json",
            response_json_schema=Verdict.model_json_schema(),  # constrains output to the schema
            temperature=0,
        ),
    )
    return Verdict.model_validate_json(response.text)


def ask_groq(system: str, user: str, model: str | None = None) -> Verdict:
    from openai import OpenAI  # Groq's API is OpenAI-compatible

    client = OpenAI(
        api_key=os.environ["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1",
    )
    response = client.chat.completions.create(
        model=model or os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "verdict",
                "strict": True,  # strict mode is supported on the gpt-oss models
                "schema": Verdict.model_json_schema(),
            },
        },
        temperature=0,
    )
    return Verdict.model_validate(json.loads(response.choices[0].message.content))


PROVIDERS = {"gemini": ask_gemini, "groq": ask_groq}


def ask(provider: str, system: str, user: str) -> Verdict:
    return PROVIDERS[provider](system, user)
