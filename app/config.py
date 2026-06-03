import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")

    PINECONE_INDEX_NAME: str = os.getenv(
        "PINECONE_INDEX_NAME",
        "hydra-compliance-index"
    )

    PINECONE_CLOUD: str = os.getenv(
        "PINECONE_CLOUD",
        "aws"
    )

    PINECONE_REGION: str = os.getenv(
        "PINECONE_REGION",
        "us-east-1"
    )

    EMBEDDING_PROVIDER: str = os.getenv(
        "EMBEDDING_PROVIDER",
        "local"
    )

    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    PINECONE_EMBEDDING_MODEL: str = os.getenv(
        "PINECONE_EMBEDDING_MODEL",
        "multilingual-e5-large"
    )

    EMBEDDING_DIMENSION: int = int(
        os.getenv("EMBEDDING_DIMENSION", "384")
    )

    LLM_PROVIDER: str = os.getenv(
        "LLM_PROVIDER",
        "ollama"
    )

    OLLAMA_MODEL: str = os.getenv(
        "OLLAMA_MODEL",
        "llama3.2:3b"
    )

    OLLAMA_BASE_URL: str = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    )

    GROQ_API_KEY: str = os.getenv(
        "GROQ_API_KEY",
        ""
    )

    GROQ_MODEL: str = os.getenv(
        "GROQ_MODEL",
        "llama-3.1-8b-instant"
    )

    IS_RENDER: bool = os.getenv(
        "RENDER",
        "false"
    ).lower() == "true"


settings = Settings()