import os
import vt
from celery import Celery
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.gemini import GeminiEmbedding

load_dotenv()

# --- 1. AI CONFIGURATION (Gemini Free Tier) ---
Settings.embed_model = GeminiEmbedding(
    model_name="models/embedding-001", 
    api_key=os.getenv("Your_API_Gemini_key")
)

# --- 2. INFRASTRUCTURE SETUP ---
# Celery uses Redis to manage the task queue
celery_app = Celery("vectorpulse_tasks", broker=os.getenv("REDIS_URL"), backend=os.getenv("REDIS_URL"))

# Connect to Qdrant Vector Database
client = QdrantClient(url=os.getenv("QDRANT_URL"))
vector_store = QdrantVectorStore(client=client, collection_name="cti_intel")

# --- 3. THE EXTRACTION TASK ---
@celery_app.task(name="ingest_vt_data")
def ingest_threat_data(indicator: str):
    """
    Fetches threat intel from VirusTotal, converts to vectors, and stores in Qdrant.
    Works for Domains (google.com) or IPs (8.8.8.8).
    """
    try:
        with vt.Client(os.getenv("07624df53505f9e3016acdcf2a8f151c16aa8ece72c4e7ff4c16b6bdbc3f2c5e")) as vt_client:
            # Determine if it's a URL/Domain or IP for the correct API endpoint
            vt_path = f"/urls/{vt.url_id(indicator)}" if "." in indicator else f"/ip_addresses/{indicator}"
            
            analysis = vt_client.get_object(vt_path)
            stats = analysis.last_analysis_stats
            
            # Create a structured text summary for the AI to read later
            intel_text = (
                f"Threat Report for {indicator}. "
                f"Community Analysis: {stats.get('malicious', 0)} malicious flags, "
                f"{stats.get('harmless', 0)} harmless flags. "
                f"Reputation Score: {analysis.get('reputation', 'N/A')}. "
                f"Categories: {analysis.get('categories', 'None')}."
            )

            # Convert text into a LlamaIndex Document
            doc = Document(text=intel_text, metadata={"source": "VirusTotal", "target": indicator})

            # Generate Embeddings and Save to Qdrant
            VectorStoreIndex.from_documents([doc], vector_store=vector_store)
            
            return f"Successfully indexed {indicator}"

    except Exception as e:
        return f"Extraction Failed: {str(e)}"
