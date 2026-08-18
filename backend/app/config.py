"""
Central configuration for the backend.
Loads values from .env and exposes them as a single Settings object.
Nothing else in the codebase should read os.environ directly -
everything goes through `settings` imported from here.
"""
#pydantic_settings is a drop-in replacement for pydantic.BaseSettings that supports nested settings and other features.    
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# backend/ is the parent of app/, so we anchor paths relative to it
# this makes the app runnable regardless of the current working directory
BACKEND_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # --- Gemini API ---
    gemini_api_key: str 
    gemini_model: str = "gemini-3.6-flash"

    # --- ChromaDB ---
    chroma_path: str = "./chroma_db"
    chroma_collection_name: str = "sathish_facts"

    # --- Embeddings ---
    embedding_model: str = "all-MiniLM-L6-v2"
    
    # --- Password tiers ---
    tier_1_password: str
    tier_2_password: str
    tier_3_password: str
    tier_4_password: str

    # --- Retrieval ---
    # how many chunks to pull back per query before access-filtering
    top_k: int = 5

    model_config = SettingsConfigDict(
        env_file=str(BACKEND_ROOT / ".env"),
        env_file_encoding="utf-8",
    )

    @property
    def chroma_path_absolute(self) -> str:
        """Resolve chroma_path relative to backend root, not cwd."""
        path = Path(self.chroma_path)
        if path.is_absolute():
            return str(path)
        return str(BACKEND_ROOT / path)

    @property
    def facts_json_path(self) -> str:
        return str(BACKEND_ROOT / "data" / "facts.json")


# Single shared instance - import this everywhere else
settings = Settings()
