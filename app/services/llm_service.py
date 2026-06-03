import ollama
from app.config import settings


def generate_llm_response(prompt: str, model: str | None = None) -> str:
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