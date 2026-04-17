import sys
import os
import asyncio   # ✅ FIX

import streamlit as st

# ✅ Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from orchestrator.workflow import Orchestrator

st.set_page_config(page_title="DeepSearch AI", layout="wide")

st.title("🔍 DeepSearch AI Assistant")

# ================================
# 🔧 SESSION STATE INIT
# ================================
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = Orchestrator()

if "history" not in st.session_state:
    st.session_state.history = []

# ================================
# 🧑 USER INPUT
# ================================
query = st.text_input("Ask your question:")

# ================================
# 🚀 RUN AGENT
# ================================
if st.button("Search") and query.strip():
    with st.spinner("Thinking..."):

        response = asyncio.run(
            st.session_state.orchestrator.run(query)
        )

        st.session_state.history.append({
    "query": query,
    "answer": response["final_answer"],
    "score": response["score"],
    "quality": response.get("quality", {})
})

        st.session_state.last_response = response

# ================================
# 📊 DISPLAY HISTORY
# ================================
for item in st.session_state.history:
    st.markdown(f"🧑 {item['query']}")
    st.markdown(f"🤖 {item['answer']}")
    st.markdown(f"⭐ Score: {item['score']}")

    q = item.get("quality", {})

    if q:
        st.markdown(f"📊 Effectiveness: {q.get('effectiveness')}")
        st.markdown(f"⚡ Efficiency: {q.get('efficiency')}")
        st.markdown(f"🛡 Robustness: {q.get('robustness')}")
        st.markdown(f"🔒 Safety: {q.get('safety')}")
        st.markdown(f"🏆 Final Score: {q.get('final_score')}")
        st.markdown(f"💬 Feedback: {q.get('feedback')}")

    st.markdown("---")