import ollama
from groq import Groq
from app.config import settings


def generate_ollama_response(prompt: str, model: str | None = None) -> str:
    selected_model = model or settings.OLLAMA_MODEL

    response = ollama.chat(
        model=selected_model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


def generate_groq_response(prompt: str, model: str | None = None) -> str:
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing.")

    selected_model = model or settings.GROQ_MODEL

    client = Groq(api_key=settings.GROQ_API_KEY)

    response = client.chat.completions.create(
        model=selected_model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=1200
    )

    return response.choices[0].message.content


def generate_llm_response(prompt: str, model: str | None = None) -> str:
    provider = settings.LLM_PROVIDER.lower()

    if provider == "groq":
        return generate_groq_response(prompt, model=model)

    if provider == "ollama":
        return generate_ollama_response(prompt, model=model)

    raise ValueError(
        f"Unsupported LLM_PROVIDER: {settings.LLM_PROVIDER}"
    )