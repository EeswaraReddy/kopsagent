import streamlit as st
import requests

st.set_page_config(page_title="KnowledgeOps Helm Agent", layout="wide")
st.title("📦 KnowledgeOps Agent — Helm PR & Deployment")

query = st.text_input("Ask the Agent", key="agent_query")
repo = st.text_input("GitHub Repo (owner/repo)", value="EeswaraReddy/kopsagent")
dry_run = st.checkbox("Dry Run (simulate actions)", value=True)

if st.button("Execute"):
    if query:
        with st.spinner("Planning and executing..."):
            try:
                resp = requests.post(
                    "http://127.0.0.1:8000/v1/agent/query",
                    json={
                        "query": query,
                        "dry_run": dry_run,
                        "repo": repo,   # now always set
                    },
                    timeout=120
                )
                resp.raise_for_status()
                result = resp.json()

                st.subheader("Plan")
                st.code(result.get("plan", "No plan returned"))

                if "helm_chart" in result:
                    st.subheader("Generated Helm Chart")
                    st.code(result["helm_chart"])

                if "actions" in result:
                    st.subheader("Actions")
                    for act in result["actions"]:
                        st.write(f"- {act}")

                if "pr_url" in result:
                    st.success(f"✅ PR Created: {result['pr_url']}")

            except Exception as e:
                st.error(str(e))
