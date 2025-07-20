import streamlit as st
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from datetime import datetime
import pandas as pd
import tempfile
import os
import json


# ========== Load Azure Credentials ==========
with open("secrets/azure_cred.json") as f:
    creds = json.load(f)

AZURE_KEY = creds["AZURE_KEY"]
AZURE_ENDPOINT = creds["AZURE_ENDPOINT"]
MODEL_ID = creds["MODEL_ID"]

# ========== Azure Client ==========
client = DocumentAnalysisClient(
    endpoint=AZURE_ENDPOINT,
    credential=AzureKeyCredential(AZURE_KEY)
)


# ========== Normalize Labels for Fuzzy Matching ==========
def normalize_label(label):
    return label.strip().lower().replace(" ", "").replace("_", "")

# ========== Detect Signature Presence ==========
def detect_signature_from_fields(doc):
    signature_keywords = [
        "Director1 sign", "Director2 sign", "signatures", "company secretary sign", "sign", "chairman signature", "ceo signature"
    ]

    for field_name, field in doc.fields.items():
        if not field or not hasattr(field, "content") or not field.content:
            continue

        field_name_lower = field_name.strip().lower()
        content_lower = field.content.strip().lower()

        for keyword in signature_keywords:
            if keyword in field_name_lower or keyword in content_lower:
                return "Yes"
    return "Yes"

# ========== Analyze Uploaded PDF ==========
def analyze_uploaded_pdf(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name

    with open(tmp_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id=MODEL_ID,
            document=f
        )
    result = poller.result()
    os.remove(tmp_path)
    return result

# ========== Extract Fields to DataFrame ==========
def extract_fields_to_dataframe(result, extraction_date, start_time, end_time):
    data = []

    expected_fields = [
        "Company Name",
        "Director Name",
        "Registration Number",
        "Registered Office",
        "FinancialYearEnd",
        "Company Auditor",
        "Shared Capital",
        "Date",
        "Director",
        "Company Secretary",
        "Audit Committee",
        "registered auditor"
    ]

    for idx, doc in enumerate(result.documents):
        doc_data = {
            "Document #": idx + 1,
            "Type": doc.doc_type,
            "Confidence": doc.confidence,
            "Extraction Date": extraction_date,
            "Start Time": start_time,
            "End Time": end_time,
            "Signature Present": detect_signature_from_fields(doc)
        }

        # Init all expected fields
        for field in expected_fields:
            doc_data[field] = ""

        # Map extracted fields to normalized expected fields
        for name, field in doc.fields.items():
            if not field or not hasattr(field, "content") or not field.content:
                continue

            extracted_label = normalize_label(name)
            for expected in expected_fields:
                if normalize_label(expected) == extracted_label:
                    doc_data[expected] = field.content
                    break

        data.append(doc_data)

    return pd.DataFrame(data)


# ========== Streamlit UI ==========
st.set_page_config(page_title="Azure Document Intelligence Viewer", layout="wide")
st.title("📄 Azure AI Document Intelligence (Custom Model)")

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file:
    st.info("⏳ Analyzing document with Azure AI...")

    try:
        # Timestamp logging
        start_dt = datetime.now()
        start_time = start_dt.strftime("%H:%M:%S")
        extraction_date = start_dt.strftime("%d/%m/%Y")

        # Analyze document
        result = analyze_uploaded_pdf(uploaded_file)
        end_time = datetime.now().strftime("%H:%M:%S")

        # Extract fields
        df = extract_fields_to_dataframe(result, extraction_date, start_time, end_time)

        st.success("✅ Document processed successfully!")
        st.dataframe(df)

        # CSV Download
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", csv, "extracted_fields.csv", "text/csv")

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
