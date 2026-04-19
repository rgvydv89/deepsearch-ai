import streamlit as st
from hitl_store import HITLStore

st.title("📊 DeepSearch AI - Analytics Dashboard")

store = HITLStore()
data = store.load()

if not data:
    st.warning("No feedback data available.")
    st.stop()

# =========================================
# FEEDBACK STATS
# =========================================
total = len(data)
positive = sum(1 for d in data if "👍" in d.get("feedback", ""))
negative = total - positive

st.subheader("👍 Feedback Summary")

st.write(f"Total Responses: {total}")
st.write(f"Positive: {positive}")
st.write(f"Negative: {negative}")

# =========================================
# ISSUE DISTRIBUTION
# =========================================
issue_counts = {}

for d in data:
    issue = d.get("issue", "None")
    issue_counts[issue] = issue_counts.get(issue, 0) + 1

st.subheader("🚨 Issue Distribution")
st.bar_chart(issue_counts)

# =========================================
# JUDGE SCORES
# =========================================
judge_scores = []

for d in data:
    judge = d.get("judge", {})
    score = judge.get("overall_score")
    if score:
        judge_scores.append(score)

if judge_scores:
    avg_score = sum(judge_scores) / len(judge_scores)
    st.subheader("🧠 Judge Score")
    st.write(f"Average Score: {round(avg_score, 2)}")
    st.line_chart(judge_scores)

# =========================================
# RECENT FAILURES
# =========================================
st.subheader("❌ Recent Negative Feedback")

for d in reversed(data):
    if "👎" in d.get("feedback", ""):
        st.markdown("### Query")
        st.write(d["query"])

        st.markdown("**Answer:**")
        st.write(d["answer"])

        st.markdown(f"**Issue:** {d.get('issue')}")
        st.markdown(f"**Comment:** {d.get('comment')}")

        st.markdown("---")
