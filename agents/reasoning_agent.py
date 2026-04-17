import os
import google.generativeai as genai
from dotenv import load_dotenv
from orchestrator.message import Message


class ReasoningAgent:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def extract_text(self, response):
        try:
            if response.candidates:
                return response.candidates[0].content.parts[0].text.strip()
        except:
            pass
        return "No response generated"

    def summarize(self, query, results, memory="", long_term=""):
        print("[ReasoningAgent] Processing...")

        # 🔥 MEMORY MODE
        if "before" in query.lower() or "previous" in query.lower():
            lines = memory.split("\n")
            for line in reversed(lines):
                if line.lower().startswith("user:"):
                    return line.replace("User:", "").strip()
            return "No previous question found"

        content = "\n".join(
            [r.get("content", "") for r in results[:5]]
        )

        prompt = f"""
USER QUERY: {query}
MEMORY: {memory}
DATA: {content}

Answer clearly in short.
"""

        response = self.model.generate_content(prompt)

        return self.extract_text(response)

    def improve(self, query, answer, feedback):
        prompt = f"""
Improve this answer:

Q: {query}
A: {answer}
Feedback: {feedback}
"""

        response = self.model.generate_content(prompt)
        return self.extract_text(response)

    def handle(self, message):
        query = message.content.get("query", "")
        results = message.content.get("results", [])
        memory = message.content.get("memory", "")
        long_term = message.content.get("long_term", "")

        answer = self.summarize(query, results, memory, long_term)

        return Message(
            sender="Reasoning",
            receiver="Critic",
            content={"final_answer": answer}
        )