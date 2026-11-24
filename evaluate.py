"""Small retrieval quality harness for profile Q&A."""

from modules.data_processing import split_profile_data, create_vector_database
from modules.data_extraction import extract_linkedin_profile


QUESTIONS = [
    {"question": "What is the person's current role?", "expected": "title"},
    {"question": "Which companies did the person work at?", "expected": "experience"},
]


def main():
    profile = extract_linkedin_profile(
        "https://www.linkedin.com/in/leonkatsnelson/",
        mock=True,
    )
    if not profile:
        raise RuntimeError("Could not load mock profile data for evaluation")

    index = create_vector_database(split_profile_data(profile))
    retriever = index.as_retriever(similarity_top_k=5)
    for item in QUESTIONS:
        nodes = retriever.retrieve(item["question"])
        hit = any(item["expected"].lower() in node.node.text.lower() for node in nodes)
        print(f"{item['question']} | retrieval_hit={hit}")


if __name__ == "__main__":
    main()
