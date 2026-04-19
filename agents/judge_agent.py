import json
import os
import re

import google.generativeai as genai
from dotenv import load_dotenv


class JudgeAgent:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def extract_json(self, text):
        try:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except:
            pass
        return None

    def evaluate_trace(self, query, trace):
        prompt = f"""
You are an expert evaluator of AI agent systems.

Your task is to evaluate the AGENT PROCESS (not just the answer).

User Query:
{query}

Execution Trace:
{trace}

Answer the following:

1. Plan Quality:
Was the plan logical and appropriate?

2. Tool Usage:
Were the correct tools selected and used properly?

3. Context Handling:
Was memory/context used effectively?

Return ONLY JSON:

{{
  "plan_quality": number (1-10),
  "tool_usage": number (1-10),
  "context_handling": number (1-10),
  "overall_score": number (1-10),
  "issues": "what went wrong (if anything)"
}}
"""

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()

            result = self.extract_json(text)

            if result:
                return result
            else:
                return {"overall_score": 0, "issues": "Invalid JSON", "raw": text}

        except Exception as e:
            return {"overall_score": 0, "issues": str(e)}
