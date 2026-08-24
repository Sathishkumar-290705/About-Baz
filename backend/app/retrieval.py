import chromadb
from google import genai
from google.genai.types import EmbedContentConfig

from app.config import settings

embed_client = genai.Client(api_key=settings.gemini_api_key)

chroma_client = chromadb.PersistentClient(
    path=settings.chroma_path_absolute
)

_collection = None


def get_collection():
    global _collection
    if _collection is None:
        _collection = chroma_client.get_or_create_collection(
            name=settings.chroma_collection_name
        )
    return _collection


def retrieve_facts(query: str, top_k: int | None = None):
    if top_k is None:
        top_k = settings.top_k

    response = embed_client.models.embed_content(
        model="gemini-embedding-001",
        contents=query,
        config=EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    )
    query_embedding = response.embeddings[0].values

    results = get_collection().query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    facts = []
    for i, document in enumerate(results["documents"][0]):
        facts.append({
            "text": document,
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return facts