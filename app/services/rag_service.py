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
Similarity Score: {match.get("score")}

Legal Text:
{metadata.get("chunk_text", "")}
"""
        context_blocks.append(block)

    return "\n---\n".join(context_blocks)


def generate_grounded_answer(question: str, context: str) -> str:
    if not context.strip():
        return (
            "The available compliance documents do not provide enough information "
            "to answer this question reliably.\n\n"
            + LEGAL_DISCLAIMER
        )

    prompt = f"""
You are a regulatory compliance intelligence assistant for Hydra Analytics.

Answer the user's question using ONLY the retrieved legal context below.

Strict rules:
1. Do not invent laws, deadlines, penalties, obligations, or legal interpretations.
2. If the context does not contain enough information, say so clearly.
3. Use a professional compliance analyst tone.
4. Mention the source title and jurisdiction where relevant.
5. Keep the answer clear, structured, and practical.
6. End with the compliance disclaimer.

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

    sources = []

    for match in matches:
        metadata = match.get("metadata", {})
        sources.append({
            "title": metadata.get("title"),
            "jurisdiction": metadata.get("jurisdiction"),
            "category": metadata.get("category"),
            "source_url": metadata.get("source_url"),
            "score": match.get("score")
        })

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }