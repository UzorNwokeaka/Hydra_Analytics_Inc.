import traceback
from fastapi import APIRouter, HTTPException
from app.schemas.request_models import SummaryRequest
from app.services.summarization_service import summarize_legal_text

router = APIRouter()


@router.post("/")
def summarize(request: SummaryRequest):
    try:
        summary = summarize_legal_text(
            text=request.text,
            max_words=request.max_words
        )

        return {
            "summary": summary,
            "disclaimer": (
                "This summary is generated for compliance research support only "
                "and should not be treated as formal legal advice."
            )
        }

    except Exception as e:
        print("SUMMARIZATION ERROR:", str(e))
        print(traceback.format_exc())

        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )