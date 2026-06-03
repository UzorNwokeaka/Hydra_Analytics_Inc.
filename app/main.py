from fastapi import FastAPI
from app.routes import search, qa, summarize, upload, intelligence, audit

app = FastAPI(
    title="Hydra Analytics Regulatory Compliance Intelligence API",
    description=(
        "RAG-powered semantic legal search, compliance Q&A, document upload, "
        "legal summarisation, advanced compliance intelligence, and auditability API."
    ),
    version="3.0.0"
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
        "version": "3.0.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "hydra-compliance-rag-api",
        "version": "3.0.0"
    }