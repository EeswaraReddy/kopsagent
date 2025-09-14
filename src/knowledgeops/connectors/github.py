import os
import requests
from typing import List, Dict

class GitHubIngestor:
    """
    Simple GitHub repo fetcher to return file contents for vector ingestion.
    """

    def __init__(self, token: str = None):
        # Prefer passed token, fallback to .env
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN not set in .env")

        self.headers = {"Authorization": f"token {self.token}"}
        print("✅ Loaded GitHub token (masked):", self.token[:4] + "..." if self.token else "None")

    def fetch_repo_files(
        self,
        repo: str,
        branch: str = "main",
        file_extensions: List[str] = None
    ) -> List[Dict]:
        """
        Fetch all files in a repo (recursively) and return list of docs for ingestion.
        Only include files with given extensions (if provided).
        """
        if file_extensions is None:
            file_extensions = [".py", ".md", ".tf", ".yaml", ".yml", ".json"]

        base_url = f"https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1"
        r = requests.get(base_url, headers=self.headers, timeout=60)
        r.raise_for_status()
        tree = r.json().get("tree", [])

        docs = []
        for f in tree:
            path = f.get("path")
            if f.get("type") != "blob":
                continue
            if not any(path.endswith(ext) for ext in file_extensions):
                continue

            # Fetch raw file content
            raw_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"
            file_resp = requests.get(raw_url, headers=self.headers, timeout=30)
            if file_resp.status_code == 200:
                text = file_resp.text
                docs.append({"title": path, "text": text})

        return docs

    # 👇 Alias so main.py works
    def fetch_repo(self, repo: str, branch: str = "main") -> List[Dict]:
        return self.fetch_repo_files(repo, branch)

    import os
import requests
from typing import List, Dict


class GitHubIngestor:
    """
    Simple GitHub repo fetcher and writer to return file contents for vector ingestion,
    and also support creating branches, committing files, and opening PRs.
    """

    def __init__(self, token: str = None):
        # Prefer passed token, fallback to .env
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN not set in .env")

        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github+json"
        }
        print("✅ Loaded GitHub token (masked):", self.token[:4] + "..." if self.token else "None")

    # ------------------- Existing -------------------
    def fetch_repo_files(
        self,
        repo: str,
        branch: str = "main",
        file_extensions: List[str] = None
    ) -> List[Dict]:
        """
        Fetch all files in a repo (recursively) and return list of docs for ingestion.
        Only include files with given extensions (if provided).
        """
        if file_extensions is None:
            file_extensions = [".py", ".md", ".tf", ".yaml", ".yml", ".json"]

        base_url = f"https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1"
        r = requests.get(base_url, headers=self.headers, timeout=60)
        r.raise_for_status()
        tree = r.json().get("tree", [])

        docs = []
        for f in tree:
            path = f.get("path")
            if f.get("type") != "blob":
                continue
            if not any(path.endswith(ext) for ext in file_extensions):
                continue

            # Fetch raw file content
            raw_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"
            file_resp = requests.get(raw_url, headers=self.headers, timeout=30)
            if file_resp.status_code == 200:
                text = file_resp.text
                docs.append({"title": path, "text": text})

        return docs

    # 👇 Alias so main.py works
    def fetch_repo(self, repo: str, branch: str = "main") -> List[Dict]:
        return self.fetch_repo_files(repo, branch)

    # ------------------- New -------------------
    def get_branch_sha(self, repo: str, branch: str = "main") -> str:
        """Get the latest commit SHA of a branch."""
        url = f"https://api.github.com/repos/{repo}/git/refs/heads/{branch}"
        r = requests.get(url, headers=self.headers, timeout=30)
        r.raise_for_status()
        return r.json()["object"]["sha"]

    def create_branch(self, repo: str, new_branch: str, from_branch: str = "main") -> str:
        """Create a new branch from an existing branch."""
        sha = self.get_branch_sha(repo, from_branch)
        url = f"https://api.github.com/repos/{repo}/git/refs"
        payload = {"ref": f"refs/heads/{new_branch}", "sha": sha}
        r = requests.post(url, headers=self.headers, json=payload, timeout=30)
        if r.status_code not in (200, 201):
            raise Exception(f"Error creating branch: {r.text}")
        return new_branch

    def commit_file(self, repo: str, branch: str, file_path: str, content: str, message: str):
        """Commit a file into a branch."""
        # 1. Get file SHA if exists
        get_url = f"https://api.github.com/repos/{repo}/contents/{file_path}?ref={branch}"
        r = requests.get(get_url, headers=self.headers, timeout=30)
        sha = r.json().get("sha") if r.status_code == 200 else None

        # 2. PUT new content
        url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
        payload = {
            "message": message,
            "content": content.encode("utf-8").decode("utf-8"),  # base64 handled by GitHub automatically
            "branch": branch
        }
        if sha:
            payload["sha"] = sha
        r = requests.put(url, headers=self.headers, json=payload, timeout=30)
        if r.status_code not in (200, 201):
            raise Exception(f"Error committing file: {r.text}")
        return r.json()

    def create_pull_request(self, repo: str, new_branch: str, base_branch: str = "main", title: str = None, body: str = None):
        """Open a PR from new_branch into base_branch."""
        url = f"https://api.github.com/repos/{repo}/pulls"
        payload = {
            "title": title or f"PR: Merge {new_branch} into {base_branch}",
            "head": new_branch,
            "base": base_branch,
            "body": body or "Auto-generated by HelmAgent."
        }
        r = requests.post(url, headers=self.headers, json=payload, timeout=30)
        if r.status_code not in (200, 201):
            raise Exception(f"Error creating PR: {r.text}")
        return r.json()
