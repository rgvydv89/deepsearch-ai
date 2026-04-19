import os

import google.generativeai as genai
from dotenv import load_dotenv

from orchestrator.message import Message


class ReasoningAgent:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    # -----------------------------------------
    # SAFE TEXT EXTRACTION
    # -----------------------------------------
    def extract_text(self, response):
        try:
            if response.candidates:
                return response.candidates[0].content.parts[0].text.strip()
        except Exception:
            pass
        return "No response generated"

    # -----------------------------------------
    # MAIN SUMMARIZATION LOGIC (GROUNDED)
    # -----------------------------------------
    def summarize(self, query, results, memory="", long_term=""):
        print("[ReasoningAgent] Processing...")

        # 🔥 DEBUG
        print("[DEBUG MEMORY]:", memory)

        # =========================================
        # MEMORY MODE
        # =========================================
        if any(word in query.lower() for word in ["before", "previous", "last", "earlier"]):
            if not memory:
                return "You haven't asked anything before in this session."

            lines = memory.split("\n")

            for line in reversed(lines):
                if line.lower().startswith("user:"):
                    return line.replace("User:", "").strip()

            return "I couldn't find your previous question."

        # =========================================
        # TOOL DATA PREPARATION
        # =========================================
        content_list = []

        for r in results[:5]:
            if isinstance(r, dict):
                content_list.append(r.get("content", ""))
            else:
                content_list.append(str(r))

        content = "\n".join(content_list)

        print("[DEBUG TOOL CONTENT]:", content)

        # 🔥 HANDLE EMPTY TOOL OUTPUT
        if not content.strip():
            return "No relevant data found from tools."

        # =========================================
        # GROUNDED PROMPT (CRITICAL FIX)
        # =========================================
        prompt = f"""
You are a strict AI system.

You MUST answer ONLY using the DATA provided below.
DO NOT use your own knowledge.
DO NOT add information not present in DATA.

USER QUERY:
{query}

DATA (from tools):
{content}

INSTRUCTIONS:
- Use ONLY the DATA above
- If DATA is insufficient, say "Insufficient data"
- Keep answer clear and concise
- Do NOT hallucinate

FINAL ANSWER:
"""

        response = self.model.generate_content(prompt)

        return self.extract_text(response)

    # -----------------------------------------
    # IMPROVE ANSWER (CRITIC LOOP)
    # -----------------------------------------
    def improve(self, query, answer, feedback):
        print("[ReasoningAgent] Improving answer...")

        prompt = f"""
Improve this answer based on feedback.

USER QUERY:
{query}

CURRENT ANSWER:
{answer}

FEEDBACK:
{feedback}

Return an improved answer.
"""

        response = self.model.generate_content(prompt)

        return self.extract_text(response)

    # -----------------------------------------
    # HANDLE (A2A ENTRY POINT)
    # -----------------------------------------
    def handle(self, message):
        query = message.content.get("query", "")
        results = message.content.get("results", [])
        memory = message.content.get("memory", "")
        long_term = message.content.get("long_term", "")

        final_answer = self.summarize(query, results, memory, long_term)

        return Message(
            sender="Reasoning",
            receiver="Critic",
            content={"final_answer": final_answer},
            msg_type="TASK",
            status="REQUEST",
            parent_id=message.id,
        )
