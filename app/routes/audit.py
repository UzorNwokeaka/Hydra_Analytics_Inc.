from fastapi import APIRouter
from app.services.audit_service import read_audit_logs

router = APIRouter()


@router.get("/logs")
def get_audit_logs(limit: int = 50):
    return {
        "total_returned": limit,
        "audit_logs": read_audit_logs(limit=limit)
    }