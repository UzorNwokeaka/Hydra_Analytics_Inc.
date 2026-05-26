from pathlib import Path
from app.services.ingestion_service import load_document


RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")


def process_documents():
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    for file_path in RAW_DATA_DIR.iterdir():
        if file_path.suffix.lower() not in [".pdf", ".txt"]:
            continue

        cleaned_text = load_document(str(file_path))

        output_file = PROCESSED_DATA_DIR / f"{file_path.stem}_cleaned.txt"
        output_file.write_text(cleaned_text, encoding="utf-8")

        print(f"Processed: {file_path.name} -> {output_file.name}")


if __name__ == "__main__":
    process_documents()