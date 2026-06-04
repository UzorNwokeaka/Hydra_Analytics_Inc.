from app.services.llm_service import generate_llm_response
from app.services.search_service import semantic_search


LEGAL_DISCLAIMER = (
    "This output is generated from retrieved compliance documents and is intended "
    "for regulatory research support only. It should not be treated as formal legal advice "
    "without review by a qualified legal professional."
)


def _build_context(results) -> str:
    context_blocks = []

    for i, result in enumerate(results, start=1):
        metadata = result.get("metadata", {})

        block = f"""
[Source {i}]
Title: {metadata.get("title", "Unknown")}
Jurisdiction: {metadata.get("jurisdiction", "Unknown")}
Category: {metadata.get("category", "Unknown")}
Source URL: {metadata.get("source_url", "Not provided")}
Chunk Index: {metadata.get("chunk_index", "Unknown")}
Similarity Score: {result.get("score")}

Text:
{metadata.get("chunk_text", "")}
"""
        context_blocks.append(block)

    return "\n---\n".join(context_blocks)


def _build_sources(results) -> list[dict]:
    sources = []

    for i, result in enumerate(results, start=1):
        metadata = result.get("metadata", {})

        sources.append({
            "source_number": i,
            "title": metadata.get("title"),
            "jurisdiction": metadata.get("jurisdiction"),
            "category": metadata.get("category"),
            "source_url": metadata.get("source_url"),
            "chunk_index": metadata.get("chunk_index"),
            "chunk_text": metadata.get("chunk_text"),
            "score": result.get("score")
        })

    return sources


def generate_regulatory_comparison(
    topic: str,
    jurisdiction_1: str,
    jurisdiction_2: str,
    category: str,
    top_k: int = 3
):
    results_1 = semantic_search(
        query=topic,
        top_k=top_k,
        jurisdiction=jurisdiction_1,
        category=category
    )

    results_2 = semantic_search(
        query=topic,
        top_k=top_k,
        jurisdiction=jurisdiction_2,
        category=category
    )

    context_1 = _build_context(results_1)
    context_2 = _build_context(results_2)

    if not context_1.strip() and not context_2.strip():
        return {
            "topic": topic,
            "jurisdiction_1": jurisdiction_1,
            "jurisdiction_2": jurisdiction_2,
            "category": category,
            "comparison": (
                "Information not found in the available regulatory knowledge base.\n\n"
                + LEGAL_DISCLAIMER
            ),
            "sources_1": [],
            "sources_2": []
        }

    prompt = f"""
You are a senior regulatory compliance analyst.

Compare the regulatory requirements for the topic below using ONLY the retrieved context.

Topic:
{topic}

Jurisdiction 1:
{jurisdiction_1}

Retrieved Context for Jurisdiction 1:
{context_1}

Jurisdiction 2:
{jurisdiction_2}

Retrieved Context for Jurisdiction 2:
{context_2}

Provide the comparison in this structure:

1. Executive Summary
2. Key Similarities
3. Key Differences
4. Compliance Implications
5. Practical Recommendation
6. Information Gaps

Strict rules:
- Use only the retrieved context.
- Do not invent laws, dates, penalties, or obligations.
- If one jurisdiction has insufficient information, clearly say so.
- Reference sources using [Source 1], [Source 2] where relevant.
- Keep the tone professional and suitable for legal/compliance teams.
"""

    llm_output = generate_llm_response(prompt)

    return {
        "topic": topic,
        "jurisdiction_1": jurisdiction_1,
        "jurisdiction_2": jurisdiction_2,
        "category": category,
        "comparison": llm_output + "\n\n" + LEGAL_DISCLAIMER,
        "sources_1": _build_sources(results_1),
        "sources_2": _build_sources(results_2)
    }


def extract_legal_clauses(text: str):
    prompt = f"""
You are a legal compliance document analyst.

Extract structured compliance intelligence from the legal/compliance text below.

Text:
{text}

Return the result using this structure:

1. Legal Obligations
2. Deadlines or Retention Periods
3. Reporting Requirements
4. Prohibited Actions
5. Responsible Parties
6. Required Evidence or Records
7. Compliance Risks
8. Practical Action Points

Strict rules:
- Use only the supplied text.
- Do not invent missing deadlines or penalties.
- If a section is not present, write "Not specified in the provided text."
- Use clear bullet points.
"""

    llm_output = generate_llm_response(prompt)

    return {
        "extracted_clauses": llm_output + "\n\n" + LEGAL_DISCLAIMER
    }


def generate_compliance_checklist(
    topic: str,
    jurisdiction: str | None = None,
    category: str | None = None,
    top_k: int = 3
):
    results = semantic_search(
        query=topic,
        top_k=top_k,
        jurisdiction=jurisdiction,
        category=category
    )

    context = _build_context(results)

    if not context.strip():
        return {
            "topic": topic,
            "jurisdiction": jurisdiction,
            "category": category,
            "checklist": (
                "Information not found in the available regulatory knowledge base.\n\n"
                + LEGAL_DISCLAIMER
            ),
            "sources": []
        }

    prompt = f"""
You are a compliance operations specialist.

Using ONLY the retrieved regulatory context, generate a practical compliance checklist.

Topic:
{topic}

Jurisdiction:
{jurisdiction}

Category:
{category}

Retrieved Context:
{context}

Create a checklist with the following columns:

- Compliance Action
- Responsible Team or Person
- Evidence Required
- Review Frequency
- Risk if Not Completed

Strict rules:
- Use only the retrieved context.
- Do not invent obligations not found in the context.
- If information is missing, state "Not specified in retrieved sources."
- Make the checklist practical for compliance analysts.
"""

    llm_output = generate_llm_response(prompt)

    return {
        "topic": topic,
        "jurisdiction": jurisdiction,
        "category": category,
        "checklist": llm_output + "\n\n" + LEGAL_DISCLAIMER,
        "sources": _build_sources(results)
    }