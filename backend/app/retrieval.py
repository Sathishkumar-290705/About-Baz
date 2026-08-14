import chromadb
from sentence_transformers import SentenceTransformer

from app.config import settings


# Load embedding model
embedding_model = SentenceTransformer(settings.embedding_model)

# Connect to ChromaDB
chroma_client = chromadb.PersistentClient(
    path=settings.chroma_path_absolute
)

collection = chroma_client.get_collection(
    name=settings.chroma_collection_name
)


def retrieve_facts(query: str, top_k: int | None = None):
    """
    Retrieve the most relevant facts from ChromaDB.
    """

    if top_k is None:
        top_k = settings.top_k

    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
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