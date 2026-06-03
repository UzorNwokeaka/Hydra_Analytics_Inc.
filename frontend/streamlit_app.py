import os
import html
import requests
import streamlit as st


API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)

st.set_page_config(
    page_title="Hydra Analytics Compliance Intelligence",
    page_icon="⚖️",
    layout="wide"
)


def safe_html(text):
    if text is None:
        return ""
    return html.escape(str(text)).replace("\n", "<br>")


st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #ffffff 0%, #f7f9fc 100%) !important;
        color: #000000 !important;
    }

    html, body, p, div, span, label, h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    [data-testid="stSidebar"] {
        background: #f1f4f8 !important;
        border-right: 1px solid #d0d7de !important;
    }

    [data-testid="stSidebar"] * {
        color: #000000 !important;
    }

    [data-testid="stSidebar"] label {
        font-size: 17px !important;
        font-weight: 800 !important;
        color: #000000 !important;
        margin-top: 12px !important;
    }

    [data-testid="stSidebar"] .stRadio,
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stSlider {
        background-color: #ffffff !important;
        border: 1px solid #c0c7d1 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }

    div[role="radiogroup"] label {
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #000000 !important;
    }

    [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #8c96a3 !important;
        border-radius: 8px !important;
    }

    [data-baseweb="select"] * {
        color: #000000 !important;
        background-color: #ffffff !important;
    }

    div[data-baseweb="popover"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    div[data-baseweb="popover"] * {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    ul[role="listbox"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    li[role="option"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }

    li[role="option"]:hover {
        background-color: #e8f0fe !important;
        color: #000000 !important;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #8c96a3 !important;
        border-radius: 8px !important;
    }

    .stButton > button,
    button[kind="primary"],
    button[kind="secondary"],
    button[data-testid="baseButton-secondary"],
    button[data-testid="baseButton-primary"] {
        background-color: #0b5cab !important;
        color: #ffffff !important;
        border: 2px solid #063f78 !important;
        border-radius: 10px !important;
        padding: 0.65rem 1.2rem !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.18) !important;
    }

    .stButton > button *,
    button[kind="primary"] *,
    button[kind="secondary"] *,
    button[data-testid="baseButton-secondary"] *,
    button[data-testid="baseButton-primary"] * {
        color: #ffffff !important;
    }

    .stButton > button:hover,
    button[kind="primary"]:hover,
    button[kind="secondary"]:hover {
        background-color: #084d91 !important;
        color: #ffffff !important;
        border: 2px solid #063f78 !important;
    }

    [data-testid="stSlider"] * {
        color: #000000 !important;
    }

    [data-testid="stSlider"] div[role="slider"] {
        background-color: #0b5cab !important;
        border: 3px solid #000000 !important;
        width: 20px !important;
        height: 20px !important;
    }

    [data-testid="stFileUploader"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px dashed #0b5cab !important;
        border-radius: 12px !important;
        padding: 16px !important;
    }

    [data-testid="stFileUploader"] * {
        color: #000000 !important;
    }

    .hero-card {
        background: #ffffff;
        border: 1px solid #d0d7de;
        border-left: 8px solid #0b5cab;
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 22px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    }

    .main-title {
        color: #000000 !important;
        font-size: 36px;
        font-weight: 800;
        margin-bottom: 0.4rem;
        line-height: 1.2;
    }

    .subtitle {
        color: #222222 !important;
        font-size: 17px;
        line-height: 1.55;
        margin-bottom: 0;
    }

    .source-card {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #b8c0cc;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.07);
    }

    .answer-box {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #111111;
        border-left: 6px solid #0b5cab;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 18px;
        line-height: 1.6;
        box-shadow: 0 3px 10px rgba(0,0,0,0.07);
    }

    .legal-text-box {
        background-color: #f8f9fb !important;
        color: #000000 !important;
        border: 1px solid #999999;
        border-radius: 10px;
        padding: 14px;
        margin-top: 8px;
        line-height: 1.6;
    }

    .info-banner {
        background-color: #eef6ff;
        color: #000000;
        border: 1px solid #9cc9f5;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 20px;
        font-weight: 600;
    }

    .footer {
        color: #000000 !important;
        font-size: 14px;
        margin-top: 30px;
    }

    [data-testid="stAlert"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #999999 !important;
        border-radius: 10px !important;
    }

    [data-testid="stAlert"] * {
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="hero-card">
        <div class="main-title">⚖️ Hydra Analytics Regulatory Compliance Intelligence Platform</div>
        <div class="subtitle">
        AI-powered LegalTech platform for semantic regulatory search, compliance Q&A,
        legal summarisation, document upload, and advanced compliance intelligence.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


menu = st.sidebar.radio(
    "Choose Function",
    [
        "Semantic Search",
        "Compliance Q&A",
        "Legal Summarisation",
        "Upload Legal Document",
        "Compliance Checklist",
        "Clause Extraction",
        "Regulatory Comparison",
        "Audit Logs",
        "Regulatory Change Tracking"
    ]
)

jurisdiction = st.sidebar.selectbox(
    "Jurisdiction",
    ["European Union", "United Kingdom", "Global", "United States", "Netherlands"]
)

category = st.sidebar.selectbox(
    "Category",
    [
        "Data Privacy",
        "Anti-Money Laundering",
        "ESG Reporting",
        "Healthcare Compliance",
        "Financial Regulation",
        "Internal Policy"
    ]
)

top_k = st.sidebar.slider("Number of Retrieved Sources", 1, 10, 3)


if menu == "Semantic Search":
    st.header("Semantic Legal Search")

    st.markdown(
        """
        <div class="info-banner">
        Search regulations using natural language instead of exact legal keywords.
        </div>
        """,
        unsafe_allow_html=True
    )

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
                st.markdown(
                    f"""
                    <div class="source-card">
                        <h4>Result {i}: {safe_html(result.get("title"))}</h4>
                        <p><b>Score:</b> {safe_html(result.get("score"))}</p>
                        <p><b>Jurisdiction:</b> {safe_html(result.get("jurisdiction"))}</p>
                        <p><b>Category:</b> {safe_html(result.get("category"))}</p>
                        <p><b>Source:</b> {safe_html(result.get("source_url"))}</p>
                        <p><b>Retrieved Legal Text:</b></p>
                        <div class="legal-text-box">
                            {safe_html(result.get("chunk_text"))}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.error(response.text)


elif menu == "Compliance Q&A":
    st.header("Compliance Question Answering with Source Traceability")

    st.markdown(
        """
        <div class="info-banner">
        Ask a compliance question and verify the AI response against retrieved legal evidence, confidence scoring, and risk classification.
        </div>
        """,
        unsafe_allow_html=True
    )

    question = st.text_area(
        "Ask a compliance question",
        "What does GDPR say about keeping personal data accurate?"
    )

    if st.button("Generate Source-Grounded Answer"):
        payload = {
            "question": question,
            "jurisdiction": jurisdiction,
            "category": category,
            "top_k": top_k
        }

        with st.spinner("Retrieving sources and generating compliance response..."):
            response = requests.post(f"{API_BASE_URL}/qa/", json=payload)

        if response.status_code == 200:
            data = response.json()

            confidence = data.get("confidence", {})
            risk = data.get("risk", {})

            metric_col1, metric_col2, metric_col3 = st.columns(3)

            with metric_col1:
                st.metric(
                    "Retrieval Confidence",
                    confidence.get("confidence_label", "Unknown")
                )

            with metric_col2:
                st.metric(
                    "Compliance Risk",
                    risk.get("risk_level", "Unknown")
                )

            with metric_col3:
                st.metric(
                    "Response Time",
                    f"{data.get('response_time_seconds', 'N/A')} sec"
                )

            st.markdown(
                f"""
                <div class="source-card">
                    <p><b>Confidence Explanation:</b> {safe_html(confidence.get("confidence_explanation"))}</p>
                    <p><b>Average Retrieval Score:</b> {safe_html(confidence.get("average_score"))}</p>
                    <p><b>Risk Rationale:</b> {safe_html(risk.get("risk_rationale"))}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            left_col, right_col = st.columns([1.05, 1])

            with left_col:
                st.subheader("AI-Generated Compliance Answer")
                st.markdown(
                    f"""
                    <div class="answer-box">
                        {safe_html(data.get("answer"))}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with right_col:
                st.subheader("Verified Retrieved Sources")

                for source in data.get("sources", []):
                    st.markdown(
                        f"""
                        <div class="source-card">
                            <h4>[Source {safe_html(source.get("source_number"))}] {safe_html(source.get("title"))}</h4>
                            <p><b>Jurisdiction:</b> {safe_html(source.get("jurisdiction"))}</p>
                            <p><b>Category:</b> {safe_html(source.get("category"))}</p>
                            <p><b>Source URL:</b> {safe_html(source.get("source_url"))}</p>
                            <p><b>Chunk Index:</b> {safe_html(source.get("chunk_index"))}</p>
                            <p><b>Similarity Score:</b> {safe_html(source.get("score"))}</p>
                            <div class="legal-text-box">
                                {safe_html(source.get("chunk_text"))}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.error(response.text)
            
elif menu == "Upload Legal Document":
    st.header("Upload and Index Legal Document")

    uploaded_file = st.file_uploader("Upload legal document", type=["pdf", "txt"])
    title = st.text_input("Document Title")
    source_url = st.text_input("Source URL or Reference", "uploaded-via-streamlit")

    if st.button("Upload and Index Document"):
        if uploaded_file is None:
            st.error("Please upload a PDF or TXT file.")
        elif not title:
            st.error("Please provide a document title.")
        else:
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            data = {
                "title": title,
                "jurisdiction": jurisdiction,
                "category": category,
                "source_url": source_url
            }

            response = requests.post(
                f"{API_BASE_URL}/upload/",
                files=files,
                data=data
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    st.success(result.get("message"))
                    st.json(result)
                else:
                    st.error(result.get("message", "Upload failed."))
            else:
                st.error(response.text)


elif menu == "Compliance Checklist":
    st.header("Compliance Checklist Generation")

    st.markdown(
        """
        <div class="info-banner">
        Convert retrieved regulatory obligations into practical compliance action items.
        </div>
        """,
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "Checklist Topic",
        "customer due diligence"
    )

    if st.button("Generate Compliance Checklist"):
        payload = {
            "topic": topic,
            "jurisdiction": jurisdiction,
            "category": category,
            "top_k": top_k
        }

        response = requests.post(
            f"{API_BASE_URL}/intelligence/checklist",
            json=payload
        )

        if response.status_code == 200:
            data = response.json()

            st.subheader("Generated Compliance Checklist")
            st.markdown(
                f"""
                <div class="answer-box">
                    {safe_html(data.get("checklist"))}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.subheader("Retrieved Sources")
            for source in data.get("sources", []):
                st.markdown(
                    f"""
                    <div class="source-card">
                        <h4>[Source {safe_html(source.get("source_number"))}] {safe_html(source.get("title"))}</h4>
                        <p><b>Jurisdiction:</b> {safe_html(source.get("jurisdiction"))}</p>
                        <p><b>Category:</b> {safe_html(source.get("category"))}</p>
                        <p><b>Similarity Score:</b> {safe_html(source.get("score"))}</p>
                        <div class="legal-text-box">
                            {safe_html(source.get("chunk_text"))}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.error(response.text)


elif menu == "Clause Extraction":
    st.header("Clause Extraction")

    st.markdown(
        """
        <div class="info-banner">
        Extract obligations, deadlines, reporting duties, responsible parties, and compliance risks from legal text.
        </div>
        """,
        unsafe_allow_html=True
    )

    clause_text = st.text_area(
        "Paste legal/compliance text",
        height=300
    )

    if st.button("Extract Compliance Clauses"):
        payload = {
            "text": clause_text
        }

        response = requests.post(
            f"{API_BASE_URL}/intelligence/extract-clauses",
            json=payload
        )

        if response.status_code == 200:
            data = response.json()

            st.subheader("Extracted Compliance Clauses")
            st.markdown(
                f"""
                <div class="answer-box">
                    {safe_html(data.get("extracted_clauses"))}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.error(response.text)


elif menu == "Regulatory Comparison":
    st.header("Regulatory Comparison")

    st.markdown(
        """
        <div class="info-banner">
        Compare compliance requirements across jurisdictions or regulatory documents.
        </div>
        """,
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "Comparison Topic",
        "personal data protection obligations"
    )

    jurisdiction_1 = st.selectbox(
        "First Jurisdiction",
        ["European Union", "United Kingdom", "Global", "United States", "Netherlands"],
        index=0
    )

    jurisdiction_2 = st.selectbox(
        "Second Jurisdiction",
        ["European Union", "United Kingdom", "Global", "United States", "Netherlands"],
        index=1
    )

    if st.button("Compare Regulations"):
        payload = {
            "topic": topic,
            "jurisdiction_1": jurisdiction_1,
            "jurisdiction_2": jurisdiction_2,
            "category": category,
            "top_k": top_k
        }

        response = requests.post(
            f"{API_BASE_URL}/intelligence/compare",
            json=payload
        )

        if response.status_code == 200:
            data = response.json()

            st.subheader("Regulatory Comparison Result")
            st.markdown(
                f"""
                <div class="answer-box">
                    {safe_html(data.get("comparison"))}
                </div>
                """,
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:
                st.subheader(f"Sources: {jurisdiction_1}")
                for source in data.get("sources_1", []):
                    st.markdown(
                        f"""
                        <div class="source-card">
                            <h4>{safe_html(source.get("title"))}</h4>
                            <p><b>Category:</b> {safe_html(source.get("category"))}</p>
                            <div class="legal-text-box">
                                {safe_html(source.get("chunk_text"))}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            with col2:
                st.subheader(f"Sources: {jurisdiction_2}")
                for source in data.get("sources_2", []):
                    st.markdown(
                        f"""
                        <div class="source-card">
                            <h4>{safe_html(source.get("title"))}</h4>
                            <p><b>Category:</b> {safe_html(source.get("category"))}</p>
                            <div class="legal-text-box">
                                {safe_html(source.get("chunk_text"))}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.error(response.text)

elif menu == "Audit Logs":
    st.header("Audit Logs")

    st.markdown(
        """
        <div class="info-banner">
        Review recent compliance Q&A interactions for governance, traceability, and audit monitoring.
        </div>
        """,
        unsafe_allow_html=True
    )

    limit = st.slider("Number of Audit Records", 5, 100, 20)

    if st.button("Load Audit Logs"):
        response = requests.get(
            f"{API_BASE_URL}/audit/logs",
            params={"limit": limit}
        )

        if response.status_code == 200:
            data = response.json()
            logs = data.get("audit_logs", [])

            if not logs:
                st.info("No audit logs found yet. Run a Compliance Q&A query first.")
            else:
                for i, log in enumerate(reversed(logs), start=1):
                    confidence = log.get("confidence", {})
                    risk = log.get("risk", {})

                    st.markdown(
                        f"""
                        <div class="source-card">
                            <h4>Audit Record {i}</h4>
                            <p><b>Timestamp:</b> {safe_html(log.get("timestamp"))}</p>
                            <p><b>Question:</b> {safe_html(log.get("question"))}</p>
                            <p><b>Jurisdiction:</b> {safe_html(log.get("jurisdiction"))}</p>
                            <p><b>Category:</b> {safe_html(log.get("category"))}</p>
                            <p><b>Source Count:</b> {safe_html(log.get("source_count"))}</p>
                            <p><b>Confidence:</b> {safe_html(confidence.get("confidence_label"))}</p>
                            <p><b>Risk Level:</b> {safe_html(risk.get("risk_level"))}</p>
                            <p><b>Response Time:</b> {safe_html(log.get("response_time_seconds"))} seconds</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.error(response.text)
            
elif menu == "Regulatory Change Tracking":
    st.header("Regulatory Change Tracking")

    st.markdown(
        """
        <div class="info-banner">
        Compare two versions of a regulation or compliance policy to identify additions,
        removals, modified obligations, compliance impact, and recommended actions.
        </div>
        """,
        unsafe_allow_html=True
    )

    document_title = st.text_input(
        "Document Title",
        "Data Privacy Policy"
    )

    old_version_label = st.text_input(
        "Old Version Label",
        "2025 Version"
    )

    new_version_label = st.text_input(
        "New Version Label",
        "2026 Version"
    )

    old_text = st.text_area(
        "Paste Old Version Text",
        height=220,
        value=(
            "Personal data must be processed lawfully, fairly and transparently. "
            "Personal data must be retained only for as long as necessary. "
            "Employees must report suspected data breaches to the Data Protection Officer."
        )
    )

    new_text = st.text_area(
        "Paste New Version Text",
        height=220,
        value=(
            "Personal data must be processed lawfully, fairly and transparently. "
            "Personal data must be retained only for as long as necessary and reviewed every 12 months. "
            "Employees must report suspected data breaches to the Data Protection Officer immediately. "
            "All employees must complete annual data protection training."
        )
    )

    if st.button("Analyse Regulatory Changes"):
        payload = {
            "document_title": document_title,
            "old_version_label": old_version_label,
            "new_version_label": new_version_label,
            "old_text": old_text,
            "new_text": new_text
        }

        with st.spinner("Comparing versions and analysing compliance impact..."):
            response = requests.post(
                f"{API_BASE_URL}/change-tracking/compare-versions",
                json=payload
            )

        if response.status_code == 200:
            data = response.json()

            st.subheader("Regulatory Change Analysis")

            st.markdown(
                f"""
                <div class="answer-box">
                    {safe_html(data.get("change_analysis"))}
                </div>
                """,
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Added Requirements")
                added_items = data.get("added_items", [])

                if added_items:
                    for item in added_items:
                        st.markdown(
                            f"""
                            <div class="source-card">
                                {safe_html(item)}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.info("No additions detected.")

            with col2:
                st.subheader("Removed Requirements")
                removed_items = data.get("removed_items", [])

                if removed_items:
                    for item in removed_items:
                        st.markdown(
                            f"""
                            <div class="source-card">
                                {safe_html(item)}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.info("No removals detected.")

            st.info(f"Response Time: {data.get('response_time_seconds')} seconds")

        else:
            st.error(response.text)

st.markdown(
    """
    <div class="footer">
    <hr>
    <b>Hydra Analytics Regulatory Compliance Intelligence Platform</b><br>
    Powered by FastAPI, Pinecone, Hugging Face Embeddings, LangChain text splitting, and Ollama local LLMs.
    </div>
    """,
    unsafe_allow_html=True
)