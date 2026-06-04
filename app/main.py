from fastapi import FastAPI
from app.routes import search, qa, summarize, upload, intelligence, audit, change_tracking

app = FastAPI(
    title="Hydra Analytics Regulatory Compliance Intelligence API",
    description=(
        "RAG-powered semantic legal search, compliance Q&A, document upload, "
        "legal summarisation, advanced compliance intelligence, and auditability API."
    ),
    version="4.0.0"
)

app.include_router(search.router, prefix="/search", tags=["Semantic Search"])
app.include_router(qa.router, prefix="/qa", tags=["Compliance Q&A"])
app.include_router(summarize.router, prefix="/summarize", tags=["Legal Summarisation"])
app.include_router(upload.router, prefix="/upload", tags=["Document Upload"])
app.include_router(
    intelligence.router,
    prefix="/intelligence",
    tags=["Advanced Compliance Intelligence"]
)
app.include_router(audit.router, prefix="/audit", tags=["Audit Logs"])


@app.get("/")
def root():
    return {
        "status": "success",
        "message": "Hydra Analytics Compliance Intelligence API is running.",
        "version": "4.0.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "hydra-compliance-rag-api",
        "version": "4.0.0"
    }
    
app.include_router(
    change_tracking.router,
    prefix="/change-tracking",
    tags=["Regulatory Change Tracking"]
)


@app.get("/debug-config")
def debug_config():
    from app.config import settings

    return {
        "llm_provider": settings.LLM_PROVIDER,
        "groq_model": settings.GROQ_MODEL,
        "groq_key_present": bool(settings.GROQ_API_KEY),
        "embedding_provider": settings.EMBEDDING_PROVIDER,
        "pinecone_index": settings.PINECONE_INDEX_NAME,
        "is_render": settings.IS_RENDER
    }