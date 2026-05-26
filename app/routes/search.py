from fastapi import APIRouter
from app.schemas.request_models import SearchRequest
from app.services.search_service import semantic_search

router = APIRouter()


@router.post("/")
def search_regulations(request: SearchRequest):
    matches = semantic_search(
        query=request.query,
        top_k=request.top_k,
        jurisdiction=request.jurisdiction,
        category=request.category
    )

    results = []

    for match in matches:
        metadata = match.get("metadata", {})

        results.append({
            "score": match.get("score"),
            "title": metadata.get("title"),
            "jurisdiction": metadata.get("jurisdiction"),
            "category": metadata.get("category"),
            "source_url": metadata.get("source_url"),
            "chunk_text": metadata.get("chunk_text")
        })

    return {
        "query": request.query,
        "total_results": len(results),
        "results": results
    }