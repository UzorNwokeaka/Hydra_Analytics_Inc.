from fastapi import APIRouter

from app.schemas.request_models import RegulatoryChangeRequest
from app.services.change_tracking_service import analyze_regulatory_changes


router = APIRouter()


@router.post("/compare-versions")
def compare_regulatory_versions(request: RegulatoryChangeRequest):
    return analyze_regulatory_changes(
        document_title=request.document_title,
        old_version_label=request.old_version_label,
        new_version_label=request.new_version_label,
        old_text=request.old_text,
        new_text=request.new_text
    )