import re
import asyncio

from agents.decision_agent import DecisionAgent
from agents.planner import PlannerAgent
from agents.reasoning_agent import ReasoningAgent
from agents.executor import ExecutorAgent
from agents.critic_agent import CriticAgent, parse_critic_response
from agents.quality_agent import QualityAgent

from memory.session_memory import SessionMemory
from memory.vector_store import VectorStore

from orchestrator.state import AgentState
from orchestrator.message import Message

from mcp.server import MCPServer
from mcp.client import MCPClient

from tools.utils import deduplicate_results


class Orchestrator:
    def __init__(self):
        self.mcp_server = MCPServer()
        self.mcp_client = MCPClient(self.mcp_server)

        self.decision_agent = DecisionAgent()
        self.executor = ExecutorAgent(self.mcp_client, self.decision_agent)
        self.planner = PlannerAgent()
        self.reasoning_agent = ReasoningAgent()
        self.critic = CriticAgent()
        self.quality_agent = QualityAgent()

        self.session_memory = SessionMemory()
        self.vector_store = VectorStore()

    def is_math_query(self, query):
        pattern = r'^\s*\d+(\s*[\+\-\*/]\s*\d+)+\s*$'
        return re.match(pattern, query)

    async def run(self, user_query: str):
        state = AgentState(user_query)

        # ALWAYS DEFINE QUALITY
        quality = None

        # =========================================
        # FAST PATH (Math)
        # =========================================
        if self.is_math_query(user_query):
            print("[FAST PATH] Math detected")

            response = self.mcp_client.call(
                "calculator",
                {"expression": user_query}
            )

            results = response.get("results", [])
            result = results[0].get("content", "") if results else ""

            quality = self.quality_agent.evaluate(
                user_query,
                str(result),
                steps_count=1,
                tool_calls=1
            )

            return {
                "final_answer": str(result),
                "score": 10,
                "feedback": "Direct calculation",
                "quality": quality
            }

        # =========================================
        # 🧠 MEMORY
        # =========================================
        session_context = self.session_memory.get_context()

        long_term_results = self.vector_store.search(user_query)
        long_term_context = "\n".join(
            [item for sublist in long_term_results for item in sublist]
        )

        # =========================================
        # 🔥 MCP FLOW
        # =========================================
        print("[Node] Orchestrator → Planner")

        planner_msg = Message(
            sender="Orchestrator",
            receiver="Planner",
            content=user_query
        )

        planner_response = self.planner.handle(planner_msg)

        steps = planner_response.content or [user_query]

        print("[Node] Planner → Executor")

        executor_msg = Message(
            sender="Planner",
            receiver="Executor",
            content=steps
        )

        executor_response = await self.executor.handle(executor_msg)

        results = executor_response.content.get("results", [])
        results = deduplicate_results(results)

        print("[DEBUG] Total results:", len(results))

        # =========================================
        # 🧠 REASONING
        # =========================================
        reasoning_msg = Message(
            sender="Executor",
            receiver="Reasoning",
            content={
                "query": user_query,
                "results": results,
                "memory": session_context,
                "long_term": long_term_context
            }
        )

        reasoning_response = self.reasoning_agent.handle(reasoning_msg)
        state.final_answer = reasoning_response.content.get("final_answer", "")

        # =========================================
        # 🔁 CRITIC LOOP
        # =========================================
        for i in range(3):
            print(f"[Critic Loop] Iteration {i+1}")

            critic_response = self.critic.review(user_query, state.final_answer)
            score, feedback = parse_critic_response(critic_response)

            state.score = score
            state.feedback = feedback

            if score >= 7:
                break

            state.final_answer = self.reasoning_agent.improve(
                user_query,
                state.final_answer,
                feedback
            )

        # =========================================
        # 📊 QUALITY AGENT
        # =========================================
        print("[QualityAgent] Evaluating response...")

        metrics = self.executor.get_metrics()

        quality = self.quality_agent.evaluate(
            user_query,
            state.final_answer,
            metrics.get("steps", 0),
            metrics.get("tool_calls", 0)
        )

        # =========================================
        # 🧠 STORE MEMORY
        # =========================================
        self.session_memory.add(user_query, state.final_answer)
        self.vector_store.add(user_query, str(state.final_answer))

        return {
            "final_answer": state.final_answer,
            "score": state.score,
            "feedback": state.feedback,
            "quality": quality
        }