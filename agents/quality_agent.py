# import os
# import json
# import re
# import time
# import google.generativeai as genai
# from dotenv import load_dotenv


# class QualityAgent:
#     def __init__(self):
#         load_dotenv()
#         genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#         self.model = genai.GenerativeModel("gemini-2.5-flash")

#     import re

# def extract_json(self, text):
#     try:
#         match = re.search(r"\{.*\}", text, re.DOTALL)
#         if match:
#             return json.loads(match.group())
#     except:
#         pass
#     return None

#     def call_llm(self, prompt, retries=2):
#         for _ in range(retries):
#             try:
#                 response = self.model.generate_content(prompt)

#                 if response.candidates:
#                     text = response.candidates[0].content.parts[0].text.strip()
#                     print("🔍 LLM OUTPUT:", text)

#                     parsed = self.extract_json(text)
#                     if parsed:
#                         return parsed

#             except Exception as e:
#                 print("[QualityAgent] Retry error:", e)

#             time.sleep(1)

#         return None

#     def rule_based_scores(self, answer, steps, tool_calls):
#         return {
#             "effectiveness": 10 if answer else 3,
#             "efficiency": max(1, 10 - (steps + tool_calls)),
#             "robustness": 8 if answer else 3,
#             "safety": 10
#         }

#     def evaluate(self, query, answer, steps_count=0, tool_calls=0):
#         print("[QualityAgent] Evaluating response...")

#         score = 8

#         if not answer or "error" in answer.lower():
#             score = 2

#         elif len(answer.split()) < 5:
#             score = 5

#         return {
#             "score": score,
#             "reason": "Basic quality evaluation"
#         }

#         prompt = f"""
# Return ONLY JSON.

# Query: {query}
# Answer: {answer}

# Rules:
# - Excellent → score ≥ 8
# - Average → 5–7
# - Poor → ≤ 4

# Return:
# {{
#  "effectiveness": number,
#  "efficiency": number,
#  "robustness": number,
#  "safety": number,
#  "final_score": number,
#  "confidence": number between 0 and 1,
#  "feedback": "short"
# }}
# """

#         llm = self.call_llm(prompt)

#         if not llm:
#             return {
#                 **base,
#                 "final_score": sum(base.values()) // 4,
#                 "confidence": 0.5,
#                 "feedback": "Fallback evaluation"
#             }

#         return {
#             "effectiveness": llm.get("effectiveness", base["effectiveness"]),
#             "efficiency": llm.get("efficiency", base["efficiency"]),
#             "robustness": llm.get("robustness", base["robustness"]),
#             "safety": llm.get("safety", base["safety"]),
#             "final_score": llm.get("final_score", 5),
#             "confidence": llm.get("confidence", 0.7),
#             "feedback": llm.get("feedback", "")
#         }


class QualityAgent:
    def __init__(self):
        pass

    def evaluate(self, query, answer, steps_count=0, tool_calls=0):
        print("[QualityAgent] Evaluating response...")

        # 🔹 Basic scoring logic
        if not answer or "error" in answer.lower():
            score = 2
            reason = "Invalid or error response"

        elif len(answer.split()) < 5:
            score = 5
            reason = "Too short answer"

        else:
            score = 8
            reason = "Good response"

        return {"score": score, "reason": reason}
