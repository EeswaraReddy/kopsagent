# src/knowledgeops/connectors/confluence.py
import os
import requests

CONFLUENCE_BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
CONFLUENCE_EMAIL = os.getenv("CONFLUENCE_EMAIL")

class ConfluenceIngestor:
    def __init__(self):
        if not (CONFLUENCE_BASE_URL and CONFLUENCE_API_TOKEN and CONFLUENCE_EMAIL):
            raise ValueError("Confluence credentials missing in .env")
        self.base_url = f"{CONFLUENCE_BASE_URL}/wiki/rest/api"

    def fetch_space(self, space_key: str, limit: int = 10):
        url = f"{self.base_url}/content"
        params = {"spaceKey": space_key, "limit": limit, "expand": "body.storage"}
        resp = requests.get(url, params=params, auth=(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN))

        if resp.status_code != 200:
            raise Exception(f"Confluence API error: {resp.text}")

        pages = resp.json().get("results", [])
        docs = []
        for p in pages:
            title = p.get("title")
            body = p.get("body", {}).get("storage", {}).get("value", "")
            docs.append({"title": title, "text": body})
        return docs
