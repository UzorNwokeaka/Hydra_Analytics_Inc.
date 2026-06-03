from app.services.explainability_service import (
    calculate_retrieval_confidence,
    classify_compliance_risk
)


def test_high_retrieval_confidence():
    sources = [
        {"score": 0.82},
        {"score": 0.78}
    ]

    result = calculate_retrieval_confidence(sources)

    assert result["confidence_label"] == "High"
    assert result["average_score"] > 0.75


def test_no_evidence_confidence():
    result = calculate_retrieval_confidence([])

    assert result["confidence_label"] == "No Evidence"


def test_high_compliance_risk():
    answer = "There was an unauthorised access incident and a data breach."
    sources = [{"score": 0.8}]

    result = classify_compliance_risk(answer, sources)

    assert result["risk_level"] == "High"


def test_unknown_risk_without_sources():
    answer = "Personal data must be protected."
    sources = []

    result = classify_compliance_risk(answer, sources)

    assert result["risk_level"] == "Unknown"