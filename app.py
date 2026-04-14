import sys
import os
import streamlit as st

# ✅ Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from orchestrator.workflow import Orchestrator


st.set_page_config(page_title="DeepSearch AI", layout="wide")

st.title("🔍 DeepSearch AI Assistant")

if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = Orchestrator()

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Ask your question:")

if st.button("Search") and query:
    with st.spinner("Thinking..."):
        response = st.session_state.orchestrator.run(query)

        st.session_state.history.append({
            "query": query,
            "answer": response.get("final_answer"),
            "score": response.get("score")
        })

# Display history
for item in reversed(st.session_state.history):
    st.markdown(f"### 🧑 {item['query']}")
    st.markdown(f"🤖 {item['answer']}")
    st.markdown(f"⭐ Score: {item['score']}")
    st.markdown("---")