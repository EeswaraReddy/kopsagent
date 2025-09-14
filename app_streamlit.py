import streamlit as st
import requests
import os

st.set_page_config(page_title="KnowledgeOps Helm Agent", layout="wide")
st.title("📦 KnowledgeOps Agent — Helm PR & Deployment")

query = st.text_input("Ask the Agent", key="agent_query")
dry_run = st.checkbox("Dry Run (simulate actions)", value=True)

if st.button("Execute"):
    if query:
        with st.spinner("Planning and executing..."):
            try:
                resp = requests.post(
                    "http://127.0.0.1:8000/v1/agent/query",
                    json={"query": query, "dry_run": dry_run},
                    timeout=120
                )
                resp.raise_for_status()
                result = resp.json()
                st.subheader("Plan")
                st.code(result["plan"])
                st.subheader("Actions")
                for act in result["actions"]:
                    st.write(f"- {act}")
            except Exception as e:
                st.error(str(e))
