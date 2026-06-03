def calculate_retrieval_confidence(sources: list[dict]) -> dict:
    if not sources:
        return {
            "average_score": 0,
            "confidence_label": "No Evidence",
            "confidence_explanation": "No relevant source documents were retrieved."
        }

    scores = [
        source.get("score", 0)
        for source in sources
        if source.get("score") is not None
    ]

    if not scores:
        average_score = 0
    else:
        average_score = sum(scores) / len(scores)

    if average_score >= 0.75:
        label = "High"
        explanation = "Retrieved sources are strongly aligned with the query."
    elif average_score >= 0.55:
        label = "Medium"
        explanation = "Retrieved sources are moderately aligned with the query."
    elif average_score > 0:
        label = "Low"
        explanation = "Retrieved sources have weak semantic alignment with the query."
    else:
        label = "No Evidence"
        explanation = "No reliable source evidence was found."

    return {
        "average_score": round(average_score, 4),
        "confidence_label": label,
        "confidence_explanation": explanation
    }


def classify_compliance_risk(answer: str, sources: list[dict]) -> dict:
    text = answer.lower()

    high_risk_terms = [
        "breach",
        "penalty",
        "unauthorised",
        "unauthorized",
        "suspicious",
        "money laundering",
        "high-risk",
        "non-compliance",
        "violation",
        "regulatory action"
    ]

    medium_risk_terms = [
        "monitoring",
        "retention",
        "approval",
        "report",
        "record",
        "due diligence",
        "access control",
        "training"
    ]

    high_hits = sum(1 for term in high_risk_terms if term in text)
    medium_hits = sum(1 for term in medium_risk_terms if term in text)

    if high_hits >= 2:
        risk_level = "High"
        rationale = "The response contains multiple high-risk compliance indicators."
    elif high_hits == 1 or medium_hits >= 3:
        risk_level = "Medium"
        rationale = "The response contains compliance-sensitive obligations or controls."
    else:
        risk_level = "Low"
        rationale = "The response does not contain strong risk indicators."

    if not sources:
        risk_level = "Unknown"
        rationale = "Risk could not be assessed because no source evidence was retrieved."

    return {
        "risk_level": risk_level,
        "risk_rationale": rationale
    }