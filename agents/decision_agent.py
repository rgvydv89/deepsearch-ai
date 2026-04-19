import os

import google.generativeai as genai
from dotenv import load_dotenv


class DecisionAgent:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def decide_tool(self, step, tools):
        print("[DecisionAgent] Deciding tool dynamically...")

        step_lower = step.lower()

        # =========================================
        # 🔥 RULE-BASED GUARDRAILS (CRITICAL)
        # =========================================

        # ✅ math → calculator
        if any(op in step_lower for op in ["+", "-", "*", "/"]):
            return "calculator"

        if any(
            word in step_lower for word in ["calculate", "sum", "addition", "multiply", "divide"]
        ):
            return "calculator"

        # ✅ thinking steps → no tool
        if any(word in step_lower for word in ["identify", "understand", "analyze"]):
            return "none"

        # =========================================
        # 🤖 LLM FALLBACK (SMART PART)
        # =========================================
        try:
            tool_descriptions = "\n".join([f"{t['name']}: {t['description']}" for t in tools])

            prompt = f"""
You are a tool selection agent.

AVAILABLE TOOLS:
{tool_descriptions}

USER STEP:
{step}

RULES:
- Return ONLY ONE word
- Must be exactly one of: {", ".join([t['name'] for t in tools])}
- No explanation
"""

            response = self.model.generate_content(prompt)

            tool_name = response.text.strip().lower()

            # ✅ sanitize output
            valid_tools = [t["name"] for t in tools]

            if tool_name in valid_tools:
                return tool_name

        except Exception as e:
            print("[DecisionAgent] LLM failed:", str(e))

        # =========================================
        # 🔥 FINAL FALLBACK
        # =========================================
        return "search"
