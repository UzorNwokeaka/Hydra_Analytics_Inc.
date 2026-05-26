from fastapi import APIRouter
from app.schemas.request_models import SummaryRequest
from app.services.summarization_service import summarize_legal_text

router = APIRouter()


@router.post("/")
def summarize(request: SummaryRequest):
    summary = summarize_legal_text(
        text=request.text,
        max_words=request.max_words
    )

    return {
        "summary": summary,
        "max_words": request.max_words,
        "disclaimer": "This is compliance research support, not formal legal advice."
    }