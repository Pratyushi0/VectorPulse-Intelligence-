import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from worker import ingest_alienvault_data
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

load_dotenv()

app = FastAPI(title="VectorPulse Core API")

# Allow Next.js frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = QdrantClient(url=os.getenv("QDRANT_URL"))
vector_store = QdrantVectorStore(client=client, collection_name="cti_intel")

class IngestRequest(BaseModel):
    threat_actor: str

class ChatRequest(BaseModel):
    prompt: str

@app.post("/api/ingest/otx")
async def trigger_otx_ingestion(request: IngestRequest):
    # Send the heavy task to the Celery worker queue
    task = ingest_alienvault_data.delay(request.threat_actor)
    return {"message": f"Ingestion started for {request.threat_actor}", "task_id": task.id}

@app.post("/api/chat")
async def chat_with_intel(request: ChatRequest):
    try:
        # Load the existing vector database
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        
        # Initialize the RAG query engine
        query_engine = index.as_query_engine(
            similarity_top_k=5,
            system_prompt=(
                "You are an expert SOC Intelligence Analyst for Project VectorPulse. "
                "Answer the user's question using ONLY the provided context from our threat feeds. "
                "Always cite your sources, pulse names, and IOCs from the metadata. "
                "If you don't know, state that there is insufficient intelligence in the current database."
            )
        )
        
        response = query_engine.query(request.prompt)
        return {"answer": str(response)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))