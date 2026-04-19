import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class AutoMetrics:
    def __init__(self, embedder):
        """
        embedder → your embedding model
        Example: sentence-transformers
        """
        self.embedder = embedder

    # -----------------------------------------
    # EMBEDDING SIMILARITY
    # -----------------------------------------
    def similarity(self, text1, text2):
        vec1 = self.embedder.encode([text1])
        vec2 = self.embedder.encode([text2])

        score = cosine_similarity(vec1, vec2)[0][0]

        return float(round(score, 3))

    # -----------------------------------------
    # SINGLE EVALUATION
    # -----------------------------------------
    def evaluate(self, expected, generated):
        if not generated:
            return 0.0

        return self.similarity(expected, generated)

    # -----------------------------------------
    # BATCH EVALUATION
    # -----------------------------------------
    def evaluate_batch(self, dataset, system):
        results = []

        for item in dataset:
            query = item["query"]
            expected = item["expected"]

            print(f"\n🔍 Query: {query}")

            try:
                response = system.run_sync(query)
                generated = response.get("final_answer", "")
            except Exception as e:
                print("❌ Error:", e)
                generated = ""

            score = self.evaluate(expected, generated)

            print(f"Score: {score}")
            print(f"Answer: {generated[:100]}...")

            results.append(score)

        avg_score = sum(results) / len(results) if results else 0

        return {"scores": results, "average_score": round(avg_score, 3)}
