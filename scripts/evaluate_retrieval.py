import json
from pathlib import Path

from app.services.search_service import semantic_search


GOLDEN_DATASET_PATH = Path("data/evaluation/golden_questions.json")


def keyword_match(text: str, keywords: list[str]) -> float:
    text_lower = text.lower()

    matched = 0

    for keyword in keywords:
        if keyword.lower() in text_lower:
            matched += 1

    if not keywords:
        return 0.0

    return matched / len(keywords)


def evaluate_retrieval():
    questions = json.loads(GOLDEN_DATASET_PATH.read_text(encoding="utf-8"))

    total_questions = len(questions)
    source_hits = 0
    keyword_scores = []

    print("Hydra Analytics RAG Retrieval Evaluation")
    print("=" * 70)

    for item in questions:
        question = item["question"]

        results = semantic_search(
            query=question,
            top_k=3,
            jurisdiction=item["jurisdiction"],
            category=item["category"]
        )

        combined_text = " ".join(
            result.get("metadata", {}).get("chunk_text", "")
            for result in results
        )

        combined_titles = " ".join(
            result.get("metadata", {}).get("title", "")
            for result in results
        )

        source_keyword = item["expected_source_keyword"]

        source_found = source_keyword.lower() in combined_titles.lower()

        if source_found:
            source_hits += 1

        answer_keyword_score = keyword_match(
            combined_text,
            item["expected_answer_keywords"]
        )

        keyword_scores.append(answer_keyword_score)

        print(f"Question: {question}")
        print(f"Expected Source Keyword: {source_keyword}")
        print(f"Source Found: {source_found}")
        print(f"Keyword Coverage Score: {answer_keyword_score:.2f}")
        print("-" * 70)

    source_accuracy = source_hits / total_questions
    average_keyword_score = sum(keyword_scores) / len(keyword_scores)

    print("FINAL EVALUATION SUMMARY")
    print("=" * 70)
    print(f"Total Questions: {total_questions}")
    print(f"Source Accuracy: {source_accuracy:.2%}")
    print(f"Average Keyword Coverage: {average_keyword_score:.2%}")


if __name__ == "__main__":
    evaluate_retrieval()