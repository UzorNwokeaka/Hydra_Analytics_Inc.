from fastapi import FastAPI
from app.routes import search, qa, summarize

app = FastAPI(
    title="Hydra Analytics Regulatory Compliance Intelligence API",
    description="RAG-powered semantic legal search, compliance Q&A, and legal summarisation API.",
    version="1.0.0"
)

app.include_router(search.router, prefix="/search", tags=["Semantic Search"])
app.include_router(qa.router, prefix="/qa", tags=["Compliance Q&A"])
app.include_router(summarize.router, prefix="/summarize", tags=["Legal Summarisation"])


@app.get("/")
def root():
    return {
        "status": "success",
        "message": "Hydra Analytics Compliance Intelligence API is running."
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "hydra-compliance-rag-api"
    }