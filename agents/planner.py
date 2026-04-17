from orchestrator.message import Message
import google.generativeai as genai
import os
from dotenv import load_dotenv
import ast


class PlannerAgent:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def create_plan(self, query):
        prompt = f"""
Return MAX 3 search queries.

Query: {query}
"""

        response = self.model.generate_content(prompt)
        text = response.text.strip()

        try:
            plan = ast.literal_eval(text)
            if isinstance(plan, list) and plan:
                return plan[:3]
        except:
            pass

        return [query]

    def handle(self, message):
        plan = self.create_plan(message.content)

        return Message(
            sender="Planner",
            receiver="Executor",
            content=plan
        )