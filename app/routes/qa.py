from fastapi import APIRouter
from app.schemas.request_models import QARequest
from app.services.rag_service import answer_question

router = APIRouter()


@router.post("/")
def compliance_qa(request: QARequest):
    return answer_question(
        question=request.question,
        top_k=request.top_k,
        jurisdiction=request.jurisdiction,
        category=request.category
    )