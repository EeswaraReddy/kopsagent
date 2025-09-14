from fastapi import APIRouter
from src.knowledgeops.connectors.confluence import ConfluenceConnector


router = APIRouter()


@router.post("/confluence")
async def ingest_confluence():
connector = ConfluenceConnector()
docs = connector.fetch_pages()
count = connector.ingest(docs)
return {"status": "ok", "pages_ingested": count}