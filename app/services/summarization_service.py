import ollama


LEGAL_DISCLAIMER = (
    "This summary is generated for compliance research support only and should not "
    "be treated as formal legal advice without professional review."
)


def summarize_legal_text(text: str, max_words: int = 250) -> str:
    prompt = f"""
You are a legal compliance summarisation assistant.

Summarise the legal text below in no more than {max_words} words.

Focus on:
- Key obligations
- Compliance risks
- Responsible parties
- Important restrictions
- Practical business implications

Do not invent information that is not in the text.

Legal Text:
{text}

Summary:
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"] + "\n\n" + LEGAL_DISCLAIMER