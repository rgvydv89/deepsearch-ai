import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio

from evaluation.pairwise_evaluator import PairwiseEvaluator
from evaluation.test_queries import TEST_QUERIES
from orchestrator.workflow import Orchestrator


# -----------------------------------------
# SAFE ANSWER FETCH
# -----------------------------------------
async def get_answer(system, query):
    try:
        response = await system.run(query)
        return response.get("final_answer", "")
    except Exception as e:
        return f"Error: {str(e)}"


# -----------------------------------------
# MAIN RUNNER
# -----------------------------------------
async def main():
    evaluator = PairwiseEvaluator()

    # 🔥 STEP 4 (IMPORTANT)
    # A = baseline
    system_a = Orchestrator()

    # B = modified system (example: disable critic)
    system_b = Orchestrator()
    # system_b.critic = None   # 👉 makes systems different

    results = {"A": 0, "B": 0, "tie": 0}

    print("\n🚀 Running Pairwise Evaluation...\n")

    for i, query in enumerate(TEST_QUERIES, 1):
        print("\n==============================")
        print(f"Query {i}: {query}")

        # Get answers
        answer_a = await get_answer(system_a, query)
        answer_b = await get_answer(system_b, query)

        print("\n🅰️ Answer A:\n", answer_a)
        print("\n🅱️ Answer B:\n", answer_b)

        # Compare
        result = evaluator.compare(query, answer_a, answer_b)

        winner = result.get("winner", "tie")
        results[winner] += 1

        print("\n🏆 Winner:", winner)
        print("📝 Reason:", result.get("rationale"))

    print("\n==============================")
    print("📊 FINAL RESULTS")
    print(results)


# -----------------------------------------
# ENTRY POINT
# -----------------------------------------
if __name__ == "__main__":
    asyncio.run(main())
