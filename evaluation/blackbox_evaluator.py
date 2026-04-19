import json
import os
import re

import google.generativeai as genai
from dotenv import load_dotenv


class BlackBoxEvaluator:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    # -----------------------------------------
    # SAFE JSON EXTRACTION
    # -----------------------------------------
    def extract_json(self, text):
        try:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except Exception:
            pass
        return None

    # -----------------------------------------
    # MAIN EVALUATION
    # -----------------------------------------
    def evaluate(self, query, answer):
        prompt = f"""
You are an AI evaluator.

Evaluate the following response:

User Query:
{query}

AI Answer:
{answer}

Instructions:
- Check if the answer is correct, relevant, and helpful
- Score from 1 to 10
- Decide if it is a success or failure

Return ONLY valid JSON:

{{
  "success": true/false,
  "score": number,
  "reason": "short explanation"
}}
"""

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()

            # 🔥 SAFE PARSING
            result = self.extract_json(text)

            if result:
                return result
            else:
                return {
                    "success": False,
                    "score": 0,
                    "reason": "Invalid JSON from evaluator",
                    "raw_output": text,
                }

        except Exception as e:
            return {
                "success": False,
                "score": 0,
                "reason": f"Evaluation failed: {str(e)}",
                "raw_output": "",
            }
