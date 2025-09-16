# src/knowledgeops/llm/local_client.py
import requests


class GroqLLM:
    """
    Generic LLM client for DevOps tasks using a locally hosted LLM.
    """

    def __init__(self, base_url="https://devllm.xxxxxxx.com/v1/chat/completions", model="tinyllama"):
        self.base_url = base_url
        self.model = model

        # 🔹 Strict DevOps instructions baked into the system prompt
        self.devops_instructions = (
            "You are a DevOps AI assistant. "
            "Use the provided context and repo information to generate "
            "production-ready DevOps outputs, including Helm charts, Terraform, "
            "scripts, or configuration files. "
            "Follow best practices, ensure outputs are copy-paste ready, "
            "and provide step-by-step reasoning if changes are needed. "
            "Do not add explanations outside of the requested code or configs."
        )

    def query(self, question: str, context: str):
        """
        Send a prompt + context to the local LLM and return the response.
        """
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.devops_instructions},
                {"role": "user", "content": f"Context:\n{context}\n\nTask:\n{question}"},
            ],
            "temperature": 0.2,
        }

        resp = requests.post(self.base_url, json=payload)
        if resp.status_code != 200:
            raise Exception(f"Local LLM error: {resp.text}")

        try:
            content = resp.json()["choices"][0]["message"]["content"]
            return content.strip() if content else ""
        except Exception:
            raise Exception(f"Unexpected response format: {resp.text}")
