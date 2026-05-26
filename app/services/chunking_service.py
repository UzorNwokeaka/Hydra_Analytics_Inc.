from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_legal_document(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", ";", " ", ""]
    )

    return splitter.split_text(text)