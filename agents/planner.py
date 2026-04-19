import json
import os
import re

import google.generativeai as genai
from dotenv import load_dotenv

from orchestrator.message import Message


class PlannerAgent:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    # -----------------------------------------
    # SAFE JSON EXTRACTION
    # -----------------------------------------
    def extract_json(self, text):
        try:
            match = re.search(r"\[.*\]", text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except:
            pass
        return None

    # -----------------------------------------
    # CREATE PLAN
    # -----------------------------------------
    def create_plan(self, query):
        prompt = f"""
You are a planning agent.

Break the user query into a short sequence of steps.

Rules:
- Maximum 3 steps
- Each step should be clear and actionable
- Focus on how to solve the query
- Use tools like "search" or "calculate" when needed

User Query:
{query}

Return ONLY a JSON list like:
["step 1", "step 2"]
"""

        response = self.model.generate_content(prompt)
        text = response.text.strip()

        plan = self.extract_json(text)

        if plan and isinstance(plan, list):
            return plan[:3]

        # fallback
        return [query]

    # -----------------------------------------
    # HANDLE
    # -----------------------------------------
    def handle(self, message):
        plan = self.create_plan(message.content)

        print("[PLANNER OUTPUT]:", plan)

        return Message(
            sender="Planner",
            receiver="Orchestrator",
            content=plan,
            msg_type="RESPONSE",
            status="SUCCESS",
            parent_id=message.id,
        )
