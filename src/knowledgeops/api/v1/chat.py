from fastapi import APIRouter
from pydantic import BaseModel
from src.knowledgeops.storage.vector_store import VectorStore
from src.knowledgeops.llm.groq_client import GroqClient


router = APIRouter()


class QueryRequest(BaseModel):
question: str


@router.post("")
async def chat(req: QueryRequest):
store = VectorStore()
contexts = store.search(req.question, k=5)
llm = GroqClient()
answer = llm.ask(req.question, contexts)
return {"answer": answer, "contexts": contexts}