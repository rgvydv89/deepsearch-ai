import os
import google.generativeai as genai


class EvaluatorAgent:
    def __init__(self):
        genai.configure(api_key="")
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def evaluate(self, query, answer):
        print("[Evaluator] Scoring response...")

        prompt = f"""
        You are an expert evaluator.

        Evaluate the quality of the answer based on:
        - Relevance to the query
        - Completeness
        - Clarity
        - Accuracy

        Query:
        {query}

        Answer:
        {answer}

        Give output strictly in this format:
        Score: <number between 1-10>
        Feedback: <short explanation>
        """

        response = self.model.generate_content(prompt)
        text = response.text

        # Simple parsing
        score = 5
        if "Score:" in text:
            try:
                score = float(text.split("Score:")[1].split("\n")[0].strip())
            except:
                pass

        return {
            "score": score,
            "feedback": text
        }

