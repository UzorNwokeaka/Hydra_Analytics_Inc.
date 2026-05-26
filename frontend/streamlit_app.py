import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Hydra Analytics Compliance Intelligence",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Hydra Analytics Regulatory Compliance Intelligence Platform")

st.markdown(
    """
    AI-powered legal intelligence platform for semantic regulatory search,
    compliance Q&A, and legal summarisation using RAG, Pinecone, FastAPI,
    Hugging Face embeddings, and Ollama/Mistral.
    """
)

menu = st.sidebar.radio(
    "Choose Function",
    [
        "Semantic Search",
        "Compliance Q&A",
        "Legal Summarisation"
    ]
)

jurisdiction = st.sidebar.selectbox(
    "Jurisdiction",
    ["European Union", "United Kingdom", "Global"]
)

category = st.sidebar.selectbox(
    "Category",
    ["Data Privacy", "Anti-Money Laundering", "ESG Reporting"]
)

top_k = st.sidebar.slider("Number of retrieved sources", 1, 10, 3)


if menu == "Semantic Search":
    st.header("Semantic Legal Search")

    query = st.text_input(
        "Enter your legal/compliance search query",
        "What principles apply to processing personal data?"
    )

    if st.button("Search Regulations"):
        payload = {
            "query": query,
            "jurisdiction": jurisdiction,
            "category": category,
            "top_k": top_k
        }

        response = requests.post(f"{API_BASE_URL}/search/", json=payload)

        if response.status_code == 200:
            data = response.json()

            st.success(f"Retrieved {data['total_results']} result(s).")

            for i, result in enumerate(data["results"], start=1):
                with st.expander(f"Result {i}: {result['title']}"):
                    st.write(f"**Score:** {result['score']}")
                    st.write(f"**Jurisdiction:** {result['jurisdiction']}")
                    st.write(f"**Category:** {result['category']}")
                    st.write(f"**Source:** {result['source_url']}")
                    st.write(result["chunk_text"])
        else:
            st.error(response.text)


elif menu == "Compliance Q&A":
    st.header("Compliance Question Answering")

    question = st.text_area(
        "Ask a compliance question",
        "What does GDPR say about keeping personal data accurate?"
    )

    if st.button("Generate Answer"):
        payload = {
            "question": question,
            "jurisdiction": jurisdiction,
            "category": category,
            "top_k": top_k
        }

        response = requests.post(f"{API_BASE_URL}/qa/", json=payload)

        if response.status_code == 200:
            data = response.json()

            st.subheader("AI-Generated Compliance Answer")
            st.write(data["answer"])

            st.subheader("Retrieved Sources")
            for source in data["sources"]:
                st.markdown(
                    f"""
                    **Title:** {source['title']}  
                    **Jurisdiction:** {source['jurisdiction']}  
                    **Category:** {source['category']}  
                    **Source:** {source['source_url']}  
                    **Similarity Score:** {source['score']}
                    """
                )
        else:
            st.error(response.text)


elif menu == "Legal Summarisation":
    st.header("Legal Document Summarisation")

    text = st.text_area(
        "Paste legal text to summarise",
        height=250
    )

    max_words = st.slider("Maximum words", 50, 500, 150)

    if st.button("Summarise Legal Text"):
        payload = {
            "text": text,
            "max_words": max_words
        }

        response = requests.post(f"{API_BASE_URL}/summarize/", json=payload)

        if response.status_code == 200:
            data = response.json()

            st.subheader("Generated Summary")
            st.write(data["summary"])

            st.info(data["disclaimer"])
        else:
            st.error(response.text)