from memory.session_memory import SessionMemory
from memory.vector_store import VectorStore
from agents.planner import PlannerAgent
from agents.search_agent import SearchAgent
from agents.reasoning_agent import ReasoningAgent
from agents.executor import ExecutorAgent
from agents.evaluator import EvaluatorAgent
from tools.utils import deduplicate_results
from agents.decision_agent import DecisionAgent

from orchestrator.state import AgentState
from orchestrator.nodes import *


class Orchestrator:
    def __init__(self):
        # ✅ Agents
        self.planner = PlannerAgent()
        self.search_agent = SearchAgent()
        self.reasoning_agent = ReasoningAgent()
        self.evaluator = EvaluatorAgent()
        self.decision_agent = DecisionAgent()
        self.executor = ExecutorAgent(self.search_agent)

        # ✅ Memory
        self.session_memory = SessionMemory()
        self.vector_store = VectorStore()

    def run(self, user_query: str):
        state = AgentState(user_query)

        # 🧠 Memory
        session_context = self.session_memory.get_context()

        long_term_results = self.vector_store.search(user_query)
        long_term_context = "\n".join(
            [item for sublist in long_term_results for item in sublist]
        )

        # 🔥 GRAPH EXECUTION
        state = planner_node(state, self.planner)
        state = executor_node(state, self.executor, self.decision_agent)

        state.results = deduplicate_results(state.results)

        print("[DEBUG] Total results:", len(state.results))

        state = reasoning_node(
            state, self.reasoning_agent, session_context, long_term_context
        )

        state = evaluation_node(state, self.evaluator, user_query)

        # 🔁 Retry loop
        if state.score < 6:
            print("[Graph] Retry triggered")

            state = reasoning_node(
                state,
                self.reasoning_agent,
                session_context,
                long_term_context + "\nImprove answer"
            )

        # 🧠 Store memory
        self.session_memory.add(user_query, state.final_answer)
        self.vector_store.add(user_query, state.final_answer)

        return {
            "final_answer": state.final_answer,
            "score": state.score,
            "feedback": state.feedback
        }