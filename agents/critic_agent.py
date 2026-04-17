import os
import google.generativeai as genai
from dotenv import load_dotenv

class CriticAgent:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def review(self, query, answer):
        print("[CriticAgent] Reviewing answer...")

        prompt = f"""
You are a strict AI critic.

USER QUERY:
{query}

ANSWER:
{answer}

TASK:
- Identify issues in the answer
- Check if it fully answers the question
- Check clarity, correctness, completeness

Return:
- score (0 to 10)
- feedback (what to improve)

Format:
Score: <number>
Feedback: <text>
"""

        response = self.model.generate_content(prompt)
        return response.text
    

def parse_critic_response(text):
    score = 5
    feedback = text

    try:
        lines = text.split("\n")
        for line in lines:
            if "Score" in line:
                score = int(line.split(":")[1].strip())
            if "Feedback" in line:
                feedback = line.split(":", 1)[1].strip()
    except:
        pass

    return score, feedback