import asyncio

from evaluation.test_queries import TEST_QUERIES
from orchestrator.workflow import Orchestrator


async def main():
    agent = Orchestrator()

    scores = []

    for query in TEST_QUERIES:
        response = await agent.run(query)

        eval_score = response.get("evaluation", {}).get("score", 0)
        scores.append(eval_score)

    avg_score = sum(scores) / len(scores) if scores else 0

    print("Average Score:", avg_score)

    if avg_score < 7:
        raise Exception("❌ Quality check failed")

    print("✅ Passed quality gate")


if __name__ == "__main__":
    asyncio.run(main())
