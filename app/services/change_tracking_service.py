import difflib
import time
from app.services.llm_service import generate_llm_response

from app.services.audit_service import write_audit_log


MODEL_NAME = "llama3.2:3b"

LEGAL_DISCLAIMER = (
    "This regulatory change analysis is generated for compliance research support only. "
    "It should not be treated as formal legal advice without review by a qualified legal professional."
)


def generate_text_diff(old_text: str, new_text: str) -> dict:
    old_lines = [line.strip() for line in old_text.splitlines() if line.strip()]
    new_lines = [line.strip() for line in new_text.splitlines() if line.strip()]

    diff = list(
        difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile="old_version",
            tofile="new_version",
            lineterm=""
        )
    )

    added = []
    removed = []

    for line in diff:
        if line.startswith("+") and not line.startswith("+++"):
            added.append(line[1:])
        elif line.startswith("-") and not line.startswith("---"):
            removed.append(line[1:])

    return {
        "added_text": added,
        "removed_text": removed,
        "raw_diff": diff
    }


def analyze_regulatory_changes(
    document_title: str,
    old_version_label: str,
    new_version_label: str,
    old_text: str,
    new_text: str
):
    start_time = time.perf_counter()

    diff_result = generate_text_diff(old_text, new_text)

    prompt = f"""
You are a senior regulatory compliance analyst.

Compare the old and new versions of the regulatory/compliance document below.

Document Title:
{document_title}

Old Version:
{old_version_label}

Old Text:
{old_text}

New Version:
{new_version_label}

New Text:
{new_text}

Detected Added Text:
{diff_result["added_text"]}

Detected Removed Text:
{diff_result["removed_text"]}

Provide the analysis using this structure:

1. Executive Summary
2. Key Additions
3. Key Removals
4. Modified or Strengthened Requirements
5. Compliance Impact
6. Risk Level: Low, Medium, or High
7. Recommended Actions for Compliance Teams
8. Information Gaps

Strict rules:
- Use only the old and new text provided.
- Do not invent laws, penalties, dates, or obligations.
- Clearly distinguish between added, removed, and modified requirements.
- Keep the tone suitable for legal, compliance, and executive stakeholders.
"""

    llm_output = generate_llm_response(prompt)

    response_time_seconds = round(time.perf_counter() - start_time, 2)

    result = {
        "document_title": document_title,
        "old_version_label": old_version_label,
        "new_version_label": new_version_label,
        "added_items": diff_result["added_text"],
        "removed_items": diff_result["removed_text"],
        "change_analysis": llm_output + "\n\n" + LEGAL_DISCLAIMER,
        "response_time_seconds": response_time_seconds
    }

    write_audit_log({
        "event_type": "regulatory_change_tracking",
        "document_title": document_title,
        "old_version_label": old_version_label,
        "new_version_label": new_version_label,
        "added_count": len(diff_result["added_text"]),
        "removed_count": len(diff_result["removed_text"]),
        "response_time_seconds": response_time_seconds
    })

    return result