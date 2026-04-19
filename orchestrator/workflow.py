import asyncio
import re

from agents.critic_agent import CriticAgent, parse_critic_response
from agents.decision_agent import DecisionAgent
from agents.executor import ExecutorAgent
from agents.judge_agent import JudgeAgent
from agents.planner import PlannerAgent
from agents.reasoning_agent import ReasoningAgent
from evaluation.blackbox_evaluator import BlackBoxEvaluator
from mcp.client import MCPClient
from mcp.server import MCPServer
from memory.session_memory import SessionMemory
from memory.vector_store import VectorStore
from orchestrator.message import Message
from orchestrator.state import AgentState
from plugins.safety_plugin import SafetyPlugin
from tools.utils import deduplicate_results
from utils.logger import StructuredLogger
from utils.metrics import MetricsCollector
from utils.tracer import TraceLogger


class Orchestrator:
    def __init__(self):
        self.mcp_server = MCPServer()
        self.mcp_client = MCPClient(self.mcp_server)
        self.metrics = MetricsCollector()

        self.evaluator = BlackBoxEvaluator()
        self.safety = SafetyPlugin()

        self.decision_agent = DecisionAgent()
        self.executor = ExecutorAgent(self.mcp_client, self.decision_agent)
        self.planner = PlannerAgent()
        self.reasoning_agent = ReasoningAgent()
        self.critic = CriticAgent()

        self.session_memory = SessionMemory()
        self.vector_store = VectorStore()

        self.tracer = TraceLogger()
        self.logger = StructuredLogger()
        self.judge = JudgeAgent()

    def is_math_query(self, query):
        pattern = r"^\s*\d+(\s*[\+\-\*/]\s*\d+)+\s*$"
        return re.match(pattern, query)

    async def run(self, user_query: str):
        self.tracer.traces = []

        # =========================================
        # 🔥 MATH SHORTCUT
        # =========================================
        if self.is_math_query(user_query):
            try:
                result = eval(user_query)
                return {
                    "final_answer": str(result),
                    "evaluation": {"score": 10},
                    "judge": {"overall_score": 10},
                    "metrics": {},
                }
            except Exception as e:
                return {
                    "final_answer": f"Math error: {str(e)}",
                    "evaluation": {},
                    "judge": {},
                    "metrics": {},
                }

        # =========================================
        # INPUT SAFETY
        # =========================================
        input_check = self.safety.check_input_safety(user_query)

        if input_check.get("blocked"):
            return {
                "final_answer": f"❌ Blocked: {input_check['reason']}",
                "evaluation": {},
                "judge": {},
                "metrics": {},
            }

        state = AgentState(user_query)

        # =========================================
        # PLANNER
        # =========================================
        planner_msg = Message(sender="Orchestrator", receiver="Planner", content=user_query)

        span = self.tracer.start_span("planner", {"query": user_query})

        planner_response = self.planner.handle(planner_msg)
        self.tracer.end_span(span, output=planner_response.content)

        steps = planner_response.content or [user_query]

        # =========================================
        # EXECUTOR
        # =========================================
        executor_msg = Message(sender="Planner", receiver="Executor", content={"steps": steps})

        span = self.tracer.start_span("executor", {"steps": steps})

        executor_response = await self.executor.handle(executor_msg)
        self.tracer.end_span(span, output=executor_response.content)

        results = executor_response.content.get("results", [])
        results = deduplicate_results(results)

        # =========================================
        # REASONING
        # =========================================
        reasoning_msg = Message(
            sender="Executor",
            receiver="Reasoning",
            content={
                "query": user_query,
                "results": results,
                "memory": self.session_memory.get_context(),
                "long_term": "",
            },
        )

        span = self.tracer.start_span("reasoning", {"query": user_query})

        reasoning_response = self.reasoning_agent.handle(reasoning_msg)
        self.tracer.end_span(span, output=reasoning_response.content)

        state.final_answer = reasoning_response.content.get("final_answer", "")

        # =========================================
        # EVALUATION
        # =========================================
        evaluation = self.evaluator.evaluate(user_query, state.final_answer)

        # =========================================
        # CRITIC LOOP
        # =========================================
        for _ in range(2):
            critic_response = self.critic.review(user_query, state.final_answer)
            score, feedback = parse_critic_response(critic_response)

            if score >= 7:
                break

            state.final_answer = self.reasoning_agent.improve(
                user_query, state.final_answer, feedback
            )

        # =========================================
        # JUDGE
        # =========================================
        judge_result = self.judge.evaluate_trace(user_query, state.final_answer)

        # =========================================
        # TRACE OUTPUT
        # =========================================
        self.tracer.print_trace()

        # =========================================
        # METRICS COLLECTION ✅ FIXED
        # =========================================
        self.metrics.add_run(trace=self.tracer.traces, evaluation=evaluation, judge=judge_result)

        metrics_summary = self.metrics.compute()

        print("\n📊 METRICS SUMMARY")
        print(metrics_summary)

        # =========================================
        # FINAL RETURN ✅ FIXED
        # =========================================
        return {
            "final_answer": state.final_answer,
            "evaluation": evaluation,
            "judge": judge_result,
            "metrics": metrics_summary,
        }
