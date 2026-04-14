import os
import google.generativeai as genai
from dotenv import load_dotenv


class DecisionAgent:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        # Use stable model
        self.model = genai.GenerativeModel("gemini-1.0-pro")

    def decide(self, step: str, context: str = ""):
        print(f"[DecisionAgent] Deciding for: {step}")

        # 🔥 Rule-based shortcut (fast + reliable)
        if len(context) < 50:
            return "search"

        prompt = f"""
Decide the best action for the given step.

Step: {step}
Context: {context}

Options:
- search
- skip
- summarize

Rules:
- Return ONLY one word
- No explanation

Answer:
"""

        try:
            response = self.model.generate_content(prompt)
            decision = response.text.strip().lower()

            if "search" in decision:
                return "search"
            elif "summarize" in decision:
                return "summarize"
            elif "skip" in decision:
                return "skip"
            else:
                return "search"  # 🔥 safe fallback

        except Exception as e:
            print("[DecisionAgent] Error:", e)
            return "search"  # fallback