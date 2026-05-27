import ollama
from app.services.search_service import semantic_search


LEGAL_DISCLAIMER = (
    "This response is generated from retrieved compliance documents and is intended "
    "for regulatory research support only. It should not be treated as formal legal advice "
    "without review by a qualified legal professional."
)


def build_context(matches) -> str:
    context_blocks = []

    for i, match in enumerate(matches, start=1):
        metadata = match.get("metadata", {})

        block = f"""
[Source {i}]
Title: {metadata.get("title", "Unknown")}
Jurisdiction: {metadata.get("jurisdiction", "Unknown")}
Category: {metadata.get("category", "Unknown")}
Source URL: {metadata.get("source_url", "Not provided")}
Chunk Index: {metadata.get("chunk_index", "Unknown")}
Similarity Score: {match.get("score")}

Legal Text:
{metadata.get("chunk_text", "")}
"""
        context_blocks.append(block)

    return "\n---\n".join(context_blocks)


def build_sources(matches) -> list[dict]:
    sources = []

    for i, match in enumerate(matches, start=1):
        metadata = match.get("metadata", {})

        sources.append({
            "source_number": i,
            "title": metadata.get("title"),
            "jurisdiction": metadata.get("jurisdiction"),
            "category": metadata.get("category"),
            "source_url": metadata.get("source_url"),
            "chunk_index": metadata.get("chunk_index"),
            "chunk_text": metadata.get("chunk_text"),
            "score": match.get("score")
        })

    return sources


def generate_grounded_answer(question: str, context: str) -> str:
    if not context.strip():
        return (
            "Information not found in the available regulatory knowledge base.\n\n"
            + LEGAL_DISCLAIMER
        )

    prompt = f"""
You are a regulatory compliance intelligence assistant for Hydra Analytics.

Answer the user's question using ONLY the retrieved legal context below.

Strict rules:
1. Do not invent laws, deadlines, penalties, obligations, or legal interpretations.
2. If the retrieved context does not contain enough information, say:
   "Information not found in the available regulatory knowledge base."
3. Use a professional compliance analyst tone.
4. Cite sources inline using this format: [Source 1], [Source 2].
5. Keep the answer practical, structured, and easy for compliance analysts to verify.
6. Do not provide personal legal advice.

Retrieved Legal Context:
{context}

User Question:
{question}

Answer:
"""

    response = ollama.chat(
        model="mistral",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"] + "\n\n" + LEGAL_DISCLAIMER


def answer_question(
    question: str,
    top_k: int = 5,
    jurisdiction: str | None = None,
    category: str | None = None
):
    matches = semantic_search(
        query=question,
        top_k=top_k,
        jurisdiction=jurisdiction,
        category=category
    )

    context = build_context(matches)
    answer = generate_grounded_answer(question, context)
    sources = build_sources(matches)

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "source_count": len(sources)
    }