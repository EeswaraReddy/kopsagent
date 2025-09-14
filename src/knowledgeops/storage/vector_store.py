# src/knowledgeops/storage/vector_store.py
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from chromadb.config import Settings


class VectorStore:
    def __init__(self):
        # Local lightweight embedding model (no API calls, CPU-friendly)
        self.embedding_fn = FastEmbedEmbeddings()

        # Persistent Chroma store
        self.db = Chroma(
            persist_directory=os.getenv("CHROMA_DIR", "./.chromadb"),
            embedding_function=self.embedding_fn,
            client_settings=Settings(anonymized_telemetry=False)
        )

    def add_documents(self, docs):
        texts = [doc["text"] for doc in docs]
        metadatas = [{"title": doc["title"]} for doc in docs]
        ids = [f"doc-{i}" for i in range(len(docs))]

        self.db.add_texts(texts=texts, metadatas=metadatas, ids=ids)

    def query(self, query: str, n_results: int = 3):
        results = self.db.similarity_search(query, k=n_results)
        context = " ".join([doc.page_content for doc in results]) if results else ""
        return context
