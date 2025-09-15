# src/knowledgeops/connectors/github_ingestor.py

import os
import base64
import requests
from typing import List, Dict, Optional


class GitHubIngestor:
    """
    Handles GitHub repo operations:
    - Fetch repo files (by extension)
    - Create branch
    - Commit file
    - Create PR
    """

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GitHub token not found. Please set GITHUB_TOKEN env variable.")
        self.base_url = "https://api.github.com"
        self.headers = {"Authorization": f"token {self.token}",
                        "Accept": "application/vnd.github.v3+json"}

    # ------------------
    # Fetch repo files
    # ------------------
    def fetch_files(self, repo: str, branch: str = "main",
                    extensions: Optional[List[str]] = None) -> List[Dict]:
        """
        Get files from a repo branch (optionally filter by extension).
        """
        url = f"{self.base_url}/repos/{repo}/git/trees/{branch}?recursive=1"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        data = resp.json()

        results = []
        for item in data.get("tree", []):
            if item["type"] == "blob":
                if extensions and not any(item["path"].endswith(ext) for ext in extensions):
                    continue
                file_url = f"{self.base_url}/repos/{repo}/contents/{item['path']}?ref={branch}"
                file_resp = requests.get(file_url, headers=self.headers)
                file_resp.raise_for_status()
                file_data = file_resp.json()
                content = base64.b64decode(file_data.get("content", "")).decode("utf-8", errors="ignore")
                results.append({"path": item["path"], "content": content})
        return results

    # ------------------
    # Branch + commit + PR
    # ------------------
    def get_branch_sha(self, repo: str, branch: str) -> str:
        """Get commit SHA of a branch."""
        url = f"{self.base_url}/repos/{repo}/git/refs/heads/{branch}"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        return resp.json()["object"]["sha"]

    def create_branch(self, repo: str, base_branch: str, new_branch: str) -> Dict:
        """Create a new branch from base_branch."""
        sha = self.get_branch_sha(repo, base_branch)
        url = f"{self.base_url}/repos/{repo}/git/refs"
        payload = {"ref": f"refs/heads/{new_branch}", "sha": sha}
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code not in (200, 201):
            raise Exception(f"Error creating branch: {resp.text}")
        return resp.json()

    def commit_file(self, repo: str, branch: str, path: str, content: str, message: str) -> Dict:
        """Commit a file to a branch."""
        url = f"{self.base_url}/repos/{repo}/contents/{path}"
        encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        payload = {"message": message, "content": encoded, "branch": branch}
        resp = requests.put(url, headers=self.headers, json=payload)
        if resp.status_code not in (200, 201):
            raise Exception(f"Error committing file: {resp.text}")
        return resp.json()

    def create_pr(self, repo: str, head_branch: str, base_branch: str,
                  title: str, body: str = "") -> Dict:
        """Create a pull request."""
        url = f"{self.base_url}/repos/{repo}/pulls"
        payload = {"title": title, "head": head_branch, "base": base_branch, "body": body}
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code not in (200, 201):
            raise Exception(f"Error creating PR: {resp.text}")
        return resp.json()
