import streamlit as st
import requests
import json

st.set_page_config(page_title="Mini Document Validator 🚢", page_icon="🚢", layout="centered")

st.title("🚢 Mini Document Validator")
st.write("Validate insurance policy documents using AI-powered extraction and business rule checks.")

backend_url = "http://localhost:8080/validate"

# Text input
document_text = st.text_area(
    "Paste your insurance document text below:",
    height=200,
    placeholder="Example: Marine Hull Insurance Policy HM-2025-10-A4B covers vessel MV Neptune ..."
)

if st.button("Validate Document"):
    if not document_text.strip():
        st.warning("Please enter a document text before submitting.")
    else:
        with st.spinner("Validating document..."):
            try:
                response = requests.post(backend_url, json={"text": document_text})
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Validation Successful")
                    st.subheader("Extracted Data:")
                    st.json(data["extracted_data"])
                    st.subheader("Validation Results:")
                    for rule in data["validation_results"]:
                        status = "🟢 PASS" if rule["status"] == "PASS" else "🔴 FAIL"
                        st.write(f"**{rule['rule']}** → {status}  \n{rule['message']}")
                else:
                    st.error(f"Server returned {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Error contacting backend: {e}")

st.markdown("---")
st.caption("Powered by FastAPI + Google Gemini AI • Genoshi Technologies LLP Assignment")
