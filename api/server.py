import traceback

from fastapi import FastAPI

from orchestrator.workflow import Orchestrator

app = FastAPI()

agent = Orchestrator()


@app.get("/query")
async def query(q: str):
    try:
        response = await agent.run(q)

        return {
            "query": q,
            "final_answer": response.get("final_answer", ""),
            "trace": response.get("trace", {}),
            "metrics": response.get("metrics", {}),
        }

    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}
