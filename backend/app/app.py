from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routes.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once when the app starts
    from ingestion.ingest_to_chroma import ingest
    print("Running ingestion on startup...")
    ingest()
    print("Ingestion complete.")
    yield
    # (nothing needed on shutdown)


def create_app() -> FastAPI:
    app = FastAPI(
        title="About Sathish API",
        description="Personal RAG chatbot for answering questions about Sathish.",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(chat_router)

    return app


app = create_app()