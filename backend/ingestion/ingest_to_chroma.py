import json
import sys
from pathlib import Path

import chromadb
from google import genai
from google.genai.types import EmbedContentConfig

# Allow imports from backend/
BACKEND_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_ROOT))

from app.config import settings

client = genai.Client(api_key=settings.gemini_api_key)


def load_facts():
    """Load facts from facts.json."""
    with open(settings.facts_json_path, "r", encoding="utf-8") as file:
        return json.load(file)


def create_embeddings(facts):
    """Generate embeddings for all facts using Gemini's embedding API."""
    texts = [fact["text"] for fact in facts]

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts,
        config=EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
    )

    return [embedding.values for embedding in response.embeddings]


def ingest():
    facts = load_facts()

    print(f"Loaded {len(facts)} facts.")

    embeddings = create_embeddings(facts)

    db_client = chromadb.PersistentClient(
        path=settings.chroma_path_absolute
    )

    collection = db_client.get_or_create_collection(
        name=settings.chroma_collection_name
    )

    ids = [f"fact_{index + 1}" for index in range(len(facts))]
    documents = [fact["text"] for fact in facts]
    metadatas = []

    for fact in facts:
        metadata = {"access": fact["access"]}
        if fact["access"] == "private":
            metadata["tier"] = fact["tier"]
        metadatas.append(metadata)

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Ingested {len(facts)} facts into ChromaDB.")
    print(f"Collection: {settings.chroma_collection_name}")
    print(f"Database: {settings.chroma_path_absolute}")


