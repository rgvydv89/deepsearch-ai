import asyncio
import os
import sys

import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer

from evaluation.auto_metrics import AutoMetrics
from evaluation.golden_set import TEST_DATA

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from evaluation.hitl_store import HITLStore
from orchestrator.workflow import Orchestrator

st.set_page_config(page_title="DeepSearch AI", layout="wide")

st.title("🔍 DeepSearch AI - Reviewer UI")

# =========================
# INIT
# =========================
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = Orchestrator()

if "latest" not in st.session_state:
    st.session_state.latest = None

store = HITLStore()

# =========================
# INPUT
# =========================
query = st.text_input("Enter your query")

if st.button("Run Agent") and query:
    with st.spinner("Running agent..."):
        response = asyncio.run(st.session_state.orchestrator.run(query))

    st.session_state.latest = {"query": query, "response": response}

# =========================
# SHOW DATA IF EXISTS
# =========================
if st.session_state.latest:
    data = st.session_state.latest
    response = data["response"]
    metrics = response.get("metrics", {})

    # =========================================
    # 📊 METRICS DASHBOARD UI
    # =========================================
    if metrics:
        st.subheader("📊 Agent Metrics Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Runs", metrics.get("total_runs", 0))
        col2.metric("Avg Latency (ms)", metrics.get("avg_latency_ms", 0))
        col3.metric("Error Rate", metrics.get("error_rate", 0))

        col4, col5 = st.columns(2)

        col4.metric("Avg Eval Score", metrics.get("avg_eval_score", 0))
        col5.metric("Avg Judge Score", metrics.get("avg_judge_score", 0))

        # =========================================
        # TOOL USAGE
        # =========================================
        if "tool_usage" in metrics:
            st.subheader("🛠️ Tool Usage")

            df = pd.DataFrame(list(metrics["tool_usage"].items()), columns=["Tool", "Count"])

            st.bar_chart(df.set_index("Tool"))

        # =========================================
        # QUALITY SCORES
        # =========================================
        st.subheader("⭐ Quality Scores")

        score_df = pd.DataFrame(
            {
                "Metric": ["Eval Score", "Judge Score"],
                "Score": [metrics.get("avg_eval_score", 0), metrics.get("avg_judge_score", 0)],
            }
        )

        st.bar_chart(score_df.set_index("Metric"))

    # =========================
    # REVIEWER UI (2 PANEL)
    # =========================
    col1, col2 = st.columns(2)

    # LEFT → CONVERSATION
    with col1:
        st.subheader("💬 Conversation")

        st.markdown("**User Query:**")
        st.write(data["query"])

        st.markdown("**Agent Answer:**")
        st.write(response["final_answer"])

        st.markdown("**Blackbox Evaluation:**")
        st.json(response.get("evaluation", {}))

    # RIGHT → REASONING
    with col2:
        st.subheader("🧠 Agent Reasoning")

        st.markdown("**Judge Output:**")
        st.json(response.get("judge", {}))

    st.markdown("---")

    # =========================
# RUN AUTOMATED METRICS
# =========================
if st.button("🚀 Run Automated Metrics"):
    with st.spinner("Running automated evaluation..."):

        # Load embedding model
        embedder = SentenceTransformer("all-MiniLM-L6-v2")

        metrics_engine = AutoMetrics(embedder)

        # Wrapper for async orchestrator
        class SyncWrapper:
            def __init__(self, orchestrator):
                self.orchestrator = orchestrator

            def run_sync(self, query):
                return asyncio.run(self.orchestrator.run(query))

        system = SyncWrapper(st.session_state.orchestrator)

        scores = []
        results_table = []

        for item in TEST_DATA:
            query = item["query"]
            expected = item["expected"]

            response = system.run_sync(query)
            generated = response.get("final_answer", "")

            score = metrics_engine.evaluate(expected, generated)

            scores.append(score)

            results_table.append({"Query": query, "Score": score, "Answer": generated[:100]})

        avg_score = sum(scores) / len(scores) if scores else 0

        st.session_state.metrics_result = {
            "scores": scores,
            "avg": round(avg_score, 3),
            "table": results_table,
        }

        # =========================
# SHOW METRICS RESULT
# =========================
if "metrics_result" in st.session_state:
    result = st.session_state.metrics_result

    st.subheader("📊 Automated Metrics Result")

    st.metric("Average Score", result["avg"])

    import pandas as pd

    df = pd.DataFrame(result["table"])

    st.dataframe(df)

    st.subheader("📈 Score Distribution")

    st.bar_chart(df.set_index("Query")["Score"])

    # =========================
    # HUMAN FEEDBACK
    # =========================
    st.subheader("🧑 Human Feedback")

    feedback = st.radio("Was this helpful?", ["👍 Yes", "👎 No"], horizontal=True)

    issue = st.selectbox(
        "Tag Issue",
        ["None", "Bad Plan", "Wrong Tool", "Hallucination", "Bad Answer", "Poor Context Usage"],
    )

    rating = st.slider("Quality Rating (1-10)", 1, 10, 7)

    comment = st.text_area("Optional Comment")

    if st.button("Submit Feedback"):
        record = {
            "query": data["query"],
            "answer": response["final_answer"],
            "feedback": feedback,
            "issue": issue,
            "rating": rating,
            "comment": comment,
            "judge": response.get("judge", {}),
            "evaluation": response.get("evaluation", {}),
        }

        store.save(record)

        st.success("✅ Feedback saved!")
