import streamlit as st
import requests
import json
import os

# Page configuration
st.set_page_config(
    page_title="FastAPI Multi-Language Code Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main { padding: 2rem; }
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
    .lang-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-weight: 500;
        margin: 0.2rem;
    }
    .python-badge { background: #3776ab; color: white; }
    .java-badge { background: #007396; color: white; }
    .js-badge { background: #f7df1e; color: black; }
    .csharp-badge { background: #239120; color: white; }
    .security-badge { 
        padding: 0.3rem 0.6rem; 
        border-radius: 4px; 
        font-size: 0.85rem; 
        font-weight: 600;
    }
    .critical { background: #dc3545; color: white; }
    .high { background: #fd7e14; color: white; }
    .medium { background: #ffc107; color: black; }
    .low { background: #28a745; color: white; }
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
if "selected_language" not in st.session_state:
    st.session_state.selected_language = "python"
if "supported_languages" not in st.session_state:
    st.session_state.supported_languages = []
if "review_count" not in st.session_state:
    st.session_state.review_count = 0
if "anthropic_api_key" not in st.session_state:
    st.session_state.anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", "")

# Fetch supported languages on startup
if not st.session_state.supported_languages:
    try:
        response = requests.get("http://127.0.0.1:8000/supported_languages")
        if response.status_code == 200:
            st.session_state.supported_languages = response.json()["languages"]
    except:
        pass

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🚀 Multi-Language API Code Generator with AI")
    st.markdown(
        "*Generate production-ready API code in Python, Java, JavaScript, or C# with AI-powered review*"
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
# Sidebar
# -------------------
with st.sidebar:
    st.markdown("### 📊 Session Status")

    if st.session_state.org_id:
        st.metric("Organization ID", st.session_state.org_id[:12] + "...")
    if st.session_state.org_name:
        st.metric("Organization", st.session_state.org_name)

    st.divider()

    # Platform Metrics
    st.markdown("### 📈 Platform Metrics")
    st.metric("Code Reviews", st.session_state.review_count)
    st.metric("Languages Supported", 4)

    st.divider()

    # Language Badge Display
    if st.session_state.supported_languages:
        st.markdown("### 🌐 Supported Languages")
        for lang in st.session_state.supported_languages:
            badge_class = f"{lang['value']}-badge"
            st.markdown(
                f'<span class="lang-badge {badge_class}">{lang["name"]}</span>',
                unsafe_allow_html=True,
            )

    st.divider()

    # API Key Configuration
    st.markdown("### 🔑 AI Configuration")
    api_key_input = st.text_input(
        "Anthropic API Key",
        value=st.session_state.anthropic_api_key,
        type="password",
        help="Required for AI features",
    )
    if api_key_input != st.session_state.anthropic_api_key:
        st.session_state.anthropic_api_key = api_key_input
        st.success("✅ API Key updated")

    if not st.session_state.anthropic_api_key:
        st.warning("⚠️ Set API key to enable AI features")

    st.divider()

    st.markdown("### 🎯 Quick Actions")
    if st.button("🔄 Refresh Session", use_container_width=True):
        st.rerun()

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.token = ""
        st.rerun()

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
        st.success("#### ✅ Organization Active")
        st.caption(f"**{st.session_state.org_name}**")

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
# Step 2: Language Selection & Code Generation
# -------------------
if st.session_state.org_id:
    st.markdown(
        '<div class="step-header">Step 2: Select Language & Generate Code</div>',
        unsafe_allow_html=True,
    )

    # Language Selection
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("#### 🌐 Choose Your Programming Language")

    col1, col2, col3, col4 = st.columns(4)

    language_options = {
        "Python": {"value": "python", "icon": "🐍", "framework": "FastAPI"},
        "Java": {"value": "java", "icon": "☕", "framework": "Spring Boot"},
        "JavaScript": {"value": "javascript", "icon": "🟨", "framework": "Express.js"},
        "C#": {"value": "csharp", "icon": "💜", "framework": ".NET Core"},
    }

    cols = [col1, col2, col3, col4]
    for idx, (lang_name, lang_info) in enumerate(language_options.items()):
        with cols[idx]:
            if st.button(
                f"{lang_info['icon']} {lang_name}\n{lang_info['framework']}",
                key=f"lang_{lang_info['value']}",
                use_container_width=True,
                type=(
                    "primary"
                    if st.session_state.selected_language == lang_info["value"]
                    else "secondary"
                ),
            ):
                st.session_state.selected_language = lang_info["value"]
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Display selected language
    st.info(f"**Selected Language:** {st.session_state.selected_language.upper()}")

    # Generate Code Button
    col_gen1, col_gen2, col_gen3 = st.columns([1, 1, 2])
    with col_gen1:
        generate_btn = st.button(
            "⚡ Generate Code", type="primary", use_container_width=True
        )

    if generate_btn:
        with st.spinner(
            f"Generating {st.session_state.selected_language.upper()} code..."
        ):
            try:
                code_res = requests.get(
                    "http://127.0.0.1:8000/generate_sample_code",
                    params={
                        "org_id": st.session_state.org_id,
                        "org_name": st.session_state.org_name,
                        "language": st.session_state.selected_language,
                    },
                )
                if code_res.status_code == 200:
                    code_data = code_res.json()
                    st.session_state.generated_code = code_data["generated_code"]
                    st.session_state.file_extension = code_data["file_extension"]
                    st.session_state.code_language = code_data["language"]
                    st.success(
                        f"✅ {st.session_state.selected_language.upper()} code generated successfully!"
                    )
                    st.rerun()
                else:
                    st.error("❌ Code generation failed")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    # Display Generated Code
    if "generated_code" in st.session_state:
        st.markdown("#### 📄 Generated API Code")

        tab1, tab2, tab3 = st.tabs(["📝 View Code", "💾 Download", "📋 Copy"])

        with tab1:
            st.code(
                st.session_state.generated_code,
                language=st.session_state.code_language,
                line_numbers=True,
            )

        with tab2:
            col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
            with col_d2:
                st.markdown('<div class="info-card">', unsafe_allow_html=True)
                st.markdown("### Download Your Code")
                filename = f"{st.session_state.org_name.lower().replace(' ', '_')}_api{st.session_state.file_extension}"
                st.markdown(f"**Filename:** `{filename}`")
                st.download_button(
                    label=f"⬇️ Download {st.session_state.code_language.upper()} Code",
                    data=st.session_state.generated_code,
                    file_name=filename,
                    mime="text/plain",
                    use_container_width=True,
                    type="primary",
                )
                st.markdown("</div>", unsafe_allow_html=True)

        with tab3:
            st.text_area(
                "Copy Code to Clipboard",
                st.session_state.generated_code,
                height=300,
                help="Select all and copy (Ctrl+A, Ctrl+C)",
            )

# -------------------
# Step 3: AI Code Review & Enhancement
# -------------------
if "generated_code" in st.session_state:
    st.markdown(
        '<div class="step-header">Step 3: AI Code Review & Enhancement</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.anthropic_api_key:
        st.warning(
            "⚠️ Please set your Anthropic API Key in the sidebar to use AI features"
        )
    else:
        col_ai1, col_ai2, col_ai3 = st.columns(3)

        with col_ai1:
            review_btn = st.button(
                "🤖 AI Code Review", type="primary", use_container_width=True
            )

        with col_ai2:
            improve_btn = st.button(
                "🔧 Improve Code", type="secondary", use_container_width=True
            )

        with col_ai3:
            test_gen_btn = st.button(
                "🧪 Generate Tests", type="secondary", use_container_width=True
            )

        # AI Code Review
        if review_btn:
            with st.spinner(
                "🤖 AI is analyzing your code for security, performance, and best practices..."
            ):
                try:
                    review_response = requests.post(
                        "http://127.0.0.1:8000/ai/review_code",
                        json={
                            "code": st.session_state.generated_code,
                            "language": st.session_state.selected_language,
                            "api_key": st.session_state.anthropic_api_key,
                        },
                    )

                    if review_response.status_code == 200:
                        review_data = review_response.json()
                        st.session_state.review_count += 1

                        # Check for errors
                        if "error" in review_data:
                            st.error(f"❌ {review_data['error']}")
                            if "message" in review_data:
                                st.info(review_data["message"])
                        else:
                            st.success("✅ AI Code Review Completed!")

                            # Overall Metrics
                            st.markdown("#### 📊 Code Quality Metrics")
                            col1, col2, col3, col4 = st.columns(4)

                            with col1:
                                score = review_data.get("overall_score", 0)
                                score_color = (
                                    "🟢" if score >= 8 else "🟡" if score >= 6 else "🔴"
                                )
                                st.metric("Overall Score", f"{score_color} {score}/10")

                            metrics = review_data.get("code_quality_metrics", {})
                            with col2:
                                st.metric(
                                    "Readability", f"{metrics.get('readability', 0)}/10"
                                )
                            with col3:
                                st.metric(
                                    "Maintainability",
                                    f"{metrics.get('maintainability', 0)}/10",
                                )
                            with col4:
                                st.metric(
                                    "Testability", f"{metrics.get('testability', 0)}/10"
                                )

                            # Summary
                            if "summary" in review_data:
                                st.info(f"**Summary:** {review_data['summary']}")

                            # Security Issues
                            security_issues = review_data.get("security_issues", [])
                            if security_issues:
                                st.markdown("#### 🔒 Security Issues")
                                for issue in security_issues:
                                    severity = issue.get("severity", "low")
                                    with st.expander(
                                        f"⚠️ {severity.upper()}: {issue.get('issue', 'Security concern')}",
                                        expanded=(severity in ["critical", "high"]),
                                    ):
                                        st.markdown(
                                            f"**Line:** {issue.get('line', 'N/A')}"
                                        )
                                        st.markdown(
                                            f"**Issue:** {issue.get('issue', 'N/A')}"
                                        )
                                        st.markdown(
                                            f"**Recommendation:** {issue.get('recommendation', 'N/A')}"
                                        )
                                        if "example" in issue and issue["example"]:
                                            st.code(
                                                issue["example"],
                                                language=st.session_state.code_language,
                                            )
                            else:
                                st.success("✅ No security issues found!")

                            # Performance Issues
                            perf_issues = review_data.get("performance_issues", [])
                            if perf_issues:
                                st.markdown("#### ⚡ Performance Improvements")
                                for issue in perf_issues:
                                    with st.expander(
                                        f"💡 {issue.get('issue', 'Performance issue')}"
                                    ):
                                        st.markdown(
                                            f"**Line:** {issue.get('line', 'N/A')}"
                                        )
                                        st.markdown(
                                            f"**Impact:** {issue.get('impact', 'N/A')}"
                                        )
                                        st.markdown(
                                            f"**Fix:** {issue.get('recommendation', 'N/A')}"
                                        )
                            else:
                                st.success("✅ No major performance issues!")

                            # Best Practices
                            best_practices = review_data.get("best_practices", [])
                            if best_practices:
                                st.markdown("#### 📚 Best Practices Suggestions")
                                for practice in best_practices:
                                    importance = practice.get("importance", "medium")
                                    icon = (
                                        "🔴"
                                        if importance == "high"
                                        else "🟡" if importance == "medium" else "🟢"
                                    )
                                    st.markdown(
                                        f"{icon} **{practice.get('category', 'General')}**: {practice.get('suggestion', 'N/A')}"
                                    )

                            # Positive Aspects
                            positive = review_data.get("positive_aspects", [])
                            if positive:
                                st.markdown("#### ✨ What's Good")
                                for aspect in positive:
                                    st.markdown(f"✓ {aspect}")
                    else:
                        st.error(
                            f"❌ Review failed with status code: {review_response.status_code}"
                        )

                except Exception as e:
                    st.error(f"❌ AI Review failed: {str(e)}")
                    st.info(
                        "💡 Make sure your Anthropic API key is valid and you have sufficient credits"
                    )

        # Code Improvement
        if improve_btn:
            with st.spinner("🔧 AI is improving your code..."):
                try:
                    improve_response = requests.post(
                        "http://127.0.0.1:8000/ai/improve_code",
                        json={
                            "code": st.session_state.generated_code,
                            "language": st.session_state.selected_language,
                            "api_key": st.session_state.anthropic_api_key,
                        },
                    )

                    if improve_response.status_code == 200:
                        improved_data = improve_response.json()

                        st.success("✅ Code Improved!")

                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("##### 📝 Original Code")
                            st.code(
                                improved_data["original_code"][:1000] + "...",
                                language=st.session_state.selected_language,
                            )

                        with col2:
                            st.markdown("##### ✨ Improved Code")
                            st.code(
                                improved_data["improved_code"][:1000] + "...",
                                language=st.session_state.selected_language,
                            )

                        # Option to replace
                        if st.button("✅ Use Improved Version", type="primary"):
                            st.session_state.generated_code = improved_data[
                                "improved_code"
                            ]
                            st.success("Code updated! Scroll up to view.")
                            st.rerun()

                        # Download improved version
                        st.download_button(
                            "⬇️ Download Improved Code",
                            improved_data["improved_code"],
                            file_name=f"{st.session_state.org_name.lower()}_improved{st.session_state.file_extension}",
                            mime="text/plain",
                        )
                    else:
                        st.error("❌ Code improvement failed")

                except Exception as e:
                    st.error(f"❌ Improvement failed: {str(e)}")

        # Test Generation
        if test_gen_btn:
            with st.spinner("🧪 Generating comprehensive test suite..."):
                try:
                    test_response = requests.post(
                        "http://127.0.0.1:8000/ai/generate_tests",
                        json={
                            "code": st.session_state.generated_code,
                            "language": st.session_state.selected_language,
                            "api_key": st.session_state.anthropic_api_key,
                        },
                    )

                    if test_response.status_code == 200:
                        test_data = test_response.json()

                        st.success(f"✅ Tests Generated using {test_data['framework']}")

                        st.markdown("#### 🧪 Generated Test Suite")
                        st.code(
                            test_data["test_code"],
                            language=st.session_state.selected_language,
                        )

                        st.download_button(
                            "⬇️ Download Test Suite",
                            test_data["test_code"],
                            file_name=f"test_{st.session_state.org_name.lower()}{st.session_state.file_extension}",
                            mime="text/plain",
                            type="primary",
                        )
                    else:
                        st.error("❌ Test generation failed")

                except Exception as e:
                    st.error(f"❌ Test generation failed: {str(e)}")

# -------------------
# Step 4: API Testing (Only for Python)
# -------------------
if "generated_code" in st.session_state and st.session_state.code_language == "python":
    st.markdown(
        '<div class="step-header">Step 4: API Testing & Validation</div>',
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
        <p>🤖 AI-Powered Multi-Language API Code Generator v2.0 | Built with Streamlit, FastAPI & Claude AI</p>
        <p style='font-size: 0.9rem;'>Featuring: Multi-Language Generation • AI Code Review • Security Scanning • Test Generation</p>
    </div>
""",
    unsafe_allow_html=True,
)
