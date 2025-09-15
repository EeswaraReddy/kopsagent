# src/knowledgeops/main.py
import os
import dotenv
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict



# ✅ Load environment variables from project root `.env`
dotenv.load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

required_envs = ["GITHUB_TOKEN", "CONFLUENCE_EMAIL", "CONFLUENCE_API_TOKEN"]
for var in required_envs:
    if not os.getenv(var):
        raise RuntimeError(f"❌ Environment variable {var} not set. Check your .env file.")


from knowledgeops.connectors.confluence import ConfluenceIngestor
from knowledgeops.storage.vector_store import VectorStore
from knowledgeops.llm.groq_client import GroqLLM
from knowledgeops.connectors.github_ingestor  import GitHubIngestor
from knowledgeops.agents.helm_agent import HelmAgent
#from github_client import GithubClient


app = FastAPI(title="KnowledgeOps Agent")

# init components
vector_store = VectorStore()
llm = GroqLLM()

# -------------------------------
# Request Models
# -------------------------------
class ConfluenceIngestRequest(BaseModel):
    space_key: str
    limit: int = 10


class ChatRequest(BaseModel):
    query: str


# -------------------------------
# Routes
# -------------------------------
@app.post("/v1/ingest/confluence")
def ingest_confluence(req: ConfluenceIngestRequest):
    try:
        ingestor = ConfluenceIngestor()
        docs = ingestor.fetch_space(req.space_key, req.limit)
        vector_store.add_documents(docs)
        return {"status": "success", "ingested_docs": len(docs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/chat")
def chat(req: ChatRequest):
    try:
        context = vector_store.query(req.query)
        answer = llm.query(req.query, context)
        return {"query": req.query, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
class GitHubIngestRequest(BaseModel):
    owner: str
    repo: str
    branch: str = "main"
    extensions: list[str] = [".py", ".md", ".tf", ".yaml", ".yml", ".json"]


@app.post("/v1/ingest/github")
def ingest_github(req: GitHubIngestRequest):
    try:
        from knowledgeops.connectors.github_ingestor  import GitHubIngestor
        ingestor = GitHubIngestor()
        docs = ingestor.fetch_repo_files(
            repo=f"{req.owner}/{req.repo}",
            branch=req.branch,
            file_extensions=req.extensions
        )
        vector_store.add_documents(docs)
        return {"status": "success", "ingested_docs": len(docs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class AgentQueryRequest(BaseModel):
    query: str
    dry_run: bool = True
    repo: str = os.getenv("DEFAULT_REPO", "your-org/your-repo")  # fallback

# -------------------------------
# Routes
# -------------------------------
@app.post("/v1/agent/query")
def agent_query(req: AgentQueryRequest) -> Dict:
    try:
        agent = HelmAgent()

        # Step 1: Plan
        plan = agent.plan_action(req.query)

        # Step 2: Execute (dry-run by default)
        result = agent.execute_plan(
            query=req.query,
            repo=req.repo,
            dry_run=req.dry_run
        )

        return {
            "plan": plan,
            "helm_chart": result.get("helm_chart"),
            "pr_url": result.get("pr_url"),
            "dry_run": req.dry_run
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
