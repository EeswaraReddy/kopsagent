# src/knowledgeops/llm/groq_client.py
import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class GroqLLM:
    def __init__(self, model="llama-3.1-8b-instant"):
        if not GROQ_API_KEY:
            raise ValueError("Missing GROQ_API_KEY in .env")
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    def query(self, question: str, context: str):
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a DevOps AI assistant. Use context to answer."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
            ],
            "temperature": 0.2
        }
        resp = requests.post(self.base_url, headers=headers, json=payload)
        if resp.status_code != 200:
            raise Exception(f"Groq API error: {resp.text}")
        return resp.json()["choices"][0]["message"]["content"]
