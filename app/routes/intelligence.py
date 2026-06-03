from fastapi import APIRouter
from app.schemas.request_models import (
    ComparisonRequest,
    ClauseExtractionRequest,
    ChecklistRequest
)
from app.services.intelligence_service import (
    generate_regulatory_comparison,
    extract_legal_clauses,
    generate_compliance_checklist
)

router = APIRouter()


@router.post("/compare")
def compare_regulations(request: ComparisonRequest):
    return generate_regulatory_comparison(
        topic=request.topic,
        jurisdiction_1=request.jurisdiction_1,
        jurisdiction_2=request.jurisdiction_2,
        category=request.category,
        top_k=request.top_k
    )


@router.post("/extract-clauses")
def extract_clauses(request: ClauseExtractionRequest):
    return extract_legal_clauses(
        text=request.text
    )


@router.post("/checklist")
def create_checklist(request: ChecklistRequest):
    return generate_compliance_checklist(
        topic=request.topic,
        jurisdiction=request.jurisdiction,
        category=request.category,
        top_k=request.top_k
    )