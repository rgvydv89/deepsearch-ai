import os
import google.generativeai as genai
from dotenv import load_dotenv


class DecisionAgent:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def decide_tool(self, query, tools):
        print("[DecisionAgent] Deciding tool dynamically...")

        tool_descriptions = "\n".join(
            [f"{t['name']}: {t['description']}" for t in tools]
        )

        prompt = f"""
You are a tool selection agent.

AVAILABLE TOOLS:
{tool_descriptions}

USER QUERY:
{query}

RULES:
- Return ONLY the tool name
- No explanation
"""

        response = self.model.generate_content(prompt)

        try:
            tool_name = response.text.strip().lower()
        except:
            tool_name = "search"

        return tool_name