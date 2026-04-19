import json
import os
import re

import google.generativeai as genai
from dotenv import load_dotenv


class PairwiseEvaluator:
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
    # MAIN COMPARISON
    # -----------------------------------------
    def compare(self, query, answer_a, answer_b):
        prompt = f"""
You are an expert evaluator.

Your job is to compare two answers and decide which is better.

Evaluate based on:
- Correctness
- Helpfulness
- Clarity
- Tone

User Query:
{query}

Answer A:
{answer_a}

Answer B:
{answer_b}

Instructions:
1. Compare both answers carefully
2. Explain which is better and why
3. Return ONLY JSON:

{{
  "winner": "A" or "B" or "tie",
  "rationale": "short explanation"
}}
"""

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()

            result = self.extract_json(text)

            if result:
                return result
            else:
                return {"winner": "tie", "rationale": "Invalid JSON", "raw_output": text}

        except Exception as e:
            return {"winner": "tie", "rationale": f"Evaluation failed: {str(e)}"}
