
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def get_client():
    api_key = (
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
    )

    if not api_key:
        raise RuntimeError(
            "Gemini API key missing. Add GEMINI_API_KEY to .env."
        )

    return genai.Client(api_key=api_key)


def generate_plan(name, age, goal, level, days):
    client = get_client()

    prompt = f"""
You are FitBuddy AI, a responsible fitness assistant.

Create a personalized {days}-day workout plan.

Name: {name}
Age: {age}
Goal: {goal}
Experience: {level}

For each day include:
1. Warm-up
2. Main exercises with sets and repetitions
3. Cool-down
4. Rest or recovery advice

Include beginner-friendly alternatives where appropriate.
Avoid extreme exercise, dangerous advice, and unrealistic promises.
Use clear headings and simple language.
For younger users, prioritize age-appropriate activity and recovery.
"""

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=prompt
    )

    if not response.text:
        raise RuntimeError("AI returned an empty workout plan.")

    return response.text.strip()


def generate_nutrition_tip(goal):
    client = get_client()

    prompt = f"""
Give one practical, balanced nutrition and recovery tip
for someone whose fitness goal is: {goal}.

Use simple language. Do not recommend restrictive diets,
supplements, or skipping meals.
"""

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=prompt
    )

    if not response.text:
        raise RuntimeError("AI returned an empty nutrition tip.")

    return response.text.strip()
