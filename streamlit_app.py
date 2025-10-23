import streamlit as st
import requests
import json

# Page configuration with custom theme
st.set_page_config(
    page_title="FastAPI Code Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for professional styling
st.markdown(
    """
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .success-box {
        padding: 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: 1rem 0;
    }
    .info-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .step-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Session state initialization
if "org_name" not in st.session_state:
    st.session_state.org_name = ""
if "org_id" not in st.session_state:
    st.session_state.org_id = ""
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "token" not in st.session_state:
    st.session_state.token = ""

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🚀 FastAPI Code Generator")
    st.markdown(
        "*Generate production-ready FastAPI code with SQLAlchemy & Authentication*"
    )
with col2:
    if st.session_state.token:
        st.success("🟢 Authenticated")

st.divider()

# -------------------
# Authentication Section
# -------------------
if not st.session_state.token:
    st.markdown(
        '<div class="step-header">🔒 Authentication Required</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown("### Login to Continue")
            st.markdown("Please authenticate with your organization credentials")
            st.markdown("</div>", unsafe_allow_html=True)

            with st.form("login_form", clear_on_submit=False):
                org_id_input = st.text_input(
                    "Organization ID",
                    value=st.session_state.org_id,
                    placeholder="Enter your org ID",
                )
                role_input = st.selectbox(
                    "Select Role", ["admin", "user"], help="Choose your access level"
                )

                st.write("")
                submitted = st.form_submit_button("🔐 Login", use_container_width=True)

                if submitted:
                    with st.spinner("Authenticating..."):
                        try:
                            response = requests.post(
                                "http://127.0.0.1:8000/token",
                                params={"org_id": org_id_input, "role": role_input},
                            )
                            if response.status_code == 200:
                                st.session_state.token = response.json()["access_token"]
                                st.session_state.org_id = org_id_input
                                st.success("✅ Authentication successful!")
                                st.rerun()
                            else:
                                st.error(
                                    "❌ Authentication failed. Please check your credentials."
                                )
                        except Exception as e:
                            st.error(f"❌ Connection error: {str(e)}")
    st.stop()

# -------------------
# Sidebar with Status
# -------------------
with st.sidebar:
    st.markdown("### 📊 Session Status")

    if st.session_state.org_id:
        st.metric("Organization ID", st.session_state.org_id[:12] + "...")
    if st.session_state.org_name:
        st.metric("Organization", st.session_state.org_name)

    st.divider()

    st.markdown("### 🎯 Quick Actions")
    if st.button("🔄 Refresh Session", use_container_width=True):
        st.rerun()

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.token = ""
        st.rerun()

    st.divider()
    st.markdown("### 📚 Documentation")
    st.markdown(
        """
    - [API Reference](#)
    - [Setup Guide](#)
    - [Best Practices](#)
    """
    )

# -------------------
# Step 1: Organization Setup
# -------------------
st.markdown(
    '<div class="step-header">Step 1: Organization Setup</div>', unsafe_allow_html=True
)

col1, col2 = st.columns([2, 1])
with col1:
    with st.container():
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        org_name = st.text_input(
            "Organization Name",
            value=st.session_state.org_name,
            placeholder="e.g., Acme Corporation",
            help="Enter a unique name for your organization",
        )

        col_btn1, col_btn2 = st.columns([1, 2])
        with col_btn1:
            create_btn = st.button("✨ Create Organization", type="primary")

        st.markdown("</div>", unsafe_allow_html=True)

with col2:
    if st.session_state.org_id and st.session_state.api_key:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("#### ✅ Organization Active")
        st.caption(f"**{st.session_state.org_name}**")
        st.markdown("</div>", unsafe_allow_html=True)

if create_btn:
    if not org_name.strip():
        st.error("⚠️ Please enter a valid organization name")
    else:
        with st.spinner("Creating organization..."):
            try:
                response = requests.get(
                    "http://127.0.0.1:8000/generate_org", params={"name": org_name}
                )
                if response.status_code == 200:
                    org_data = response.json()
                    st.session_state.org_id = org_data["org_id"]
                    st.session_state.api_key = org_data["api_key"]
                    st.session_state.org_name = org_name

                    st.success("✅ Organization created successfully!")

                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.info(f"**Org ID:** `{st.session_state.org_id}`")
                    with col_b:
                        st.info(f"**API Key:** `{st.session_state.api_key}`")

                    st.rerun()
                else:
                    st.error("❌ Failed to create organization")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# -------------------
# Step 2: Generate CRUD API Code
# -------------------
if st.session_state.org_id:
    st.markdown(
        '<div class="step-header">Step 2: Generate FastAPI CRUD Code</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown(
            "Generate complete FastAPI code with authentication, database models, and CRUD operations"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        generate_btn = st.button(
            "⚡ Generate Code", type="primary", use_container_width=True
        )

    if generate_btn:
        with st.spinner("Generating code..."):
            try:
                code_res = requests.get(
                    "http://127.0.0.1:8000/generate_sample_code",
                    params={
                        "org_id": st.session_state.org_id,
                        "org_name": st.session_state.org_name,
                    },
                )
                if code_res.status_code == 200:
                    code_data = code_res.json()
                    st.session_state.generated_code = code_data["generated_code"]
                    st.success("✅ Code generated successfully!")
                    st.rerun()
                else:
                    st.error("❌ Code generation failed")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    if "generated_code" in st.session_state:
        st.markdown("#### 📄 Generated FastAPI Code")

        tab1, tab2 = st.tabs(["📝 View Code", "💾 Download"])

        with tab1:
            st.code(
                st.session_state.generated_code, language="python", line_numbers=True
            )

        with tab2:
            col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
            with col_d2:
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown("### Download Your Code")
                st.markdown(
                    f"**Filename:** `{st.session_state.org_name.lower()}_api.py`"
                )
                st.download_button(
                    label="⬇️ Download Python API Code",
                    data=st.session_state.generated_code,
                    file_name=f"{st.session_state.org_name.lower()}_api.py",
                    mime="text/plain",
                    use_container_width=True,
                    type="primary",
                )
                st.markdown("</div>", unsafe_allow_html=True)

# -------------------
# Step 3: API Testing
# -------------------
if "generated_code" in st.session_state:
    st.markdown(
        '<div class="step-header">Step 3: API Testing & Validation</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("#### Test Your Generated API")
        st.markdown("Ensure your FastAPI server is running on `http://127.0.0.1:8000`")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        test_action = st.selectbox(
            "Select Operation",
            ["GET User", "POST User", "PUT User", "DELETE User"],
            help="Choose the CRUD operation to test",
        )

    with st.expander("🔧 Request Parameters", expanded=True):
        col_p1, col_p2 = st.columns(2)

        with col_p1:
            user_id = st.text_input(
                "Org User ID", value="user001", placeholder="user001"
            )
            user_name = st.text_input("Name", value="John Doe", placeholder="John Doe")

        with col_p2:
            contact_no = st.text_input(
                "Contact Number", value="1234567890", placeholder="1234567890"
            )
            employee_code = st.text_input(
                "Employee Code", value="EMP001", placeholder="EMP001"
            )

    col_test1, col_test2, col_test3 = st.columns([1, 1, 2])
    with col_test1:
        test_btn = st.button("🚀 Run Test", type="primary", use_container_width=True)

    if test_btn:
        base_url = f"http://127.0.0.1:8000/api/org/{st.session_state.org_id}/users/"
        headers = {"Authorization": f"Bearer {st.session_state.token}"}

        with st.spinner(f"Executing {test_action}..."):
            try:
                if test_action == "GET User":
                    res = requests.get(base_url + user_id, headers=headers)
                elif test_action == "POST User":
                    payload = {
                        "org_user_id": user_id,
                        "org_id": st.session_state.org_id,
                        "name": user_name,
                        "contact_no": contact_no,
                        "employee_code": employee_code,
                        "created_date": "2025-10-21T10:00:00",
                        "valid_till": "2025-12-31T23:59:59",
                    }
                    res = requests.post(base_url, json=payload, headers=headers)
                elif test_action == "PUT User":
                    payload = {
                        "org_user_id": user_id,
                        "org_id": st.session_state.org_id,
                        "name": user_name,
                        "contact_no": contact_no,
                        "employee_code": employee_code,
                        "created_date": "2025-10-21T10:00:00",
                        "valid_till": "2025-12-31T23:59:59",
                    }
                    res = requests.put(
                        base_url + user_id, json=payload, headers=headers
                    )
                else:
                    res = requests.delete(base_url + user_id, headers=headers)

                st.markdown("#### 📊 Response")

                if res.status_code in [200, 201]:
                    st.success(f"✅ Status Code: {res.status_code}")
                    st.json(res.json())
                else:
                    st.error(f"❌ Status Code: {res.status_code}")
                    st.code(res.text, language="json")

            except Exception as e:
                st.error(f"❌ Connection Error: {str(e)}")
                st.info("💡 Make sure your FastAPI server is running on port 8000")

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #718096; padding: 2rem 0;'>
        <p>FastAPI Code Generator v1.0 | Built with Streamlit</p>
    </div>
""",
    unsafe_allow_html=True,
)


# {
# "message":"User created"
# "user":{
# "employee_code":"EMP001"
# "contact_no":"1234567890"
# "valid_till":"2025-12-31T23:59:59"
# "name":"John Doe"
# "org_id":"3c3ebb9d-050e-5ad5-99f1-a16d8b14fe52"
# "org_user_id":"user002"
# "created_date":"2025-10-21T10:00:00"
# }
