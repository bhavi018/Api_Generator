import streamlit as st
import requests
from ai_refactor import suggest_improvements

st.set_page_config(page_title="FastAPI Code Generator", layout="wide")
st.title("🚀 FastAPI Code Generator with AI Refactoring")

# -------------------
# Step 1 & 2: Org + CRUD Code (same as Phase 3)
# -------------------
org_name = st.text_input("Enter Organization Name")

if st.button("Generate CRUD API"):
    response = requests.get(
        "http://127.0.0.1:8000/generate_org", params={"name": org_name}
    )
    org_data = response.json()
    org_id = org_data["org_id"]
    api_key = org_data["api_key"]

    code_res = requests.get(
        "http://127.0.0.1:8000/generate_sample_code",
        params={"org_id": org_id, "org_name": org_name},
    )
    generated_code = code_res.json()["generated_code"]

    st.subheader("📄 Auto-Generated FastAPI Code")
    st.code(generated_code, language="python")

    st.session_state.generated_code = generated_code

# -------------------
# Step 4: AI Suggestions & Refactoring
# -------------------
if "generated_code" in st.session_state:
    st.header("Step 4: AI Suggestions & Refactoring")
    if st.button("Get AI Suggestions & Refactor Code"):
        with st.spinner("Analyzing code with AI..."):
            ai_response = suggest_improvements(st.session_state.generated_code)
            st.subheader("💡 AI Suggestions & Refactored Code")
            st.text(ai_response)
