import google.generativeai as genai
import os
import re
import ast
from dotenv import load_dotenv


class PlannerAgent:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key="AIzaSyBbI_jI4_Xw3tvS9oWdK2f--At012t80YM")
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def create_plan(self, user_query: str):
        prompt = f"""
You are a planning agent.

STRICT RULES:
- Return ONLY a Python list of strings
- NO explanation
- NO markdown
- NO JSON blocks
- Each step must be short (max 8 words)

Example:
["AWS AI services", "Azure AI pricing", "GCP comparison"]

User Query:
{user_query}
"""

        response = self.model.generate_content(prompt)
        text = response.text.strip()

        print("[DEBUG] Raw Planner Output:", text)

        # 🔹 Remove markdown if present
        text = text.replace("```json", "").replace("```", "").strip()

        # 🔹 Try parsing as Python list safely
        try:
            plan = ast.literal_eval(text)
            if isinstance(plan, list):
                return [str(step) for step in plan if isinstance(step, str)]
        except Exception:
            pass

        # 🔹 Fallback: extract meaningful lines
        lines = re.findall(r"[A-Za-z0-9 ,\-]{3,}", text)

        cleaned_plan = []

        for line in lines:
            line = line.strip()

            # Skip unwanted noise
            if any(x in line.lower() for x in ["json", "step", "description"]):
                continue

            # Keep only short steps
            if len(line.split()) <= 10:
                cleaned_plan.append(line)

        # 🔹 Final fallback
        if not cleaned_plan:
            return [user_query]

        return cleaned_plan