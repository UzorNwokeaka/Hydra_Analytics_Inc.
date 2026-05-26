from pinecone import Pinecone
from app.config import settings


pc = Pinecone(api_key=settings.PINECONE_API_KEY)

INDEX_NAME = settings.PINECONE_INDEX_NAME


def reset_index():
    existing_indexes = pc.list_indexes().names()

    if INDEX_NAME in existing_indexes:
        print(f"Deleting index: {INDEX_NAME}")
        pc.delete_index(INDEX_NAME)
        print("Index deleted successfully.")
    else:
        print("Index does not exist.")


if __name__ == "__main__":
    reset_index()