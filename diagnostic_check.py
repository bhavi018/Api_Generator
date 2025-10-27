"""
Diagnostic script to check if all files and dependencies are properly set up
"""

import os
import sys


def check_file(filename):
    """Check if a file exists"""
    exists = os.path.exists(filename)
    status = "✅" if exists else "❌"
    print(f"{status} {filename}")
    return exists


def check_import(module_name):
    """Check if a module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ {module_name}")
        return True
    except ImportError as e:
        print(f"❌ {module_name} - {str(e)}")
        return False


print("=" * 60)
print("DIAGNOSTIC CHECK FOR FASTAPI CODE GENERATOR")
print("=" * 60)

print("\n📁 Checking Required Files:")
print("-" * 60)
files_to_check = [
    "main.py",
    "models.py",
    "database.py",
    "auth.py",
    "utils.py",
    "code_translator.py",
    "ai_code_reviewer.py",
    "streamlit_app.py",
    "requirements.txt",
    ".env",
]

all_files_exist = True
for file in files_to_check:
    if not check_file(file):
        all_files_exist = False

print("\n📦 Checking Required Packages:")
print("-" * 60)
packages_to_check = [
    "fastapi",
    "uvicorn",
    "sqlalchemy",
    "streamlit",
    "requests",
    "pydantic",
    "jose",  # python-jose
    "anthropic",
]

all_packages_installed = True
for package in packages_to_check:
    if not check_import(package):
        all_packages_installed = False

print("\n🔑 Checking Environment Variables:")
print("-" * 60)
env_vars = ["ANTHROPIC_API_KEY"]
api_key_set = False

try:
    from dotenv import load_dotenv

    load_dotenv()
    print("✅ .env file loaded")
except:
    print("⚠️  python-dotenv not installed or .env file missing")

for var in env_vars:
    value = os.environ.get(var)
    if value:
        print(f"✅ {var} is set (length: {len(value)})")
        if var == "ANTHROPIC_API_KEY" and len(value) > 10:
            api_key_set = True
    else:
        print(f"❌ {var} is NOT set")

print("\n🔍 Checking FastAPI Server:")
print("-" * 60)
try:
    import requests

    response = requests.get("http://127.0.0.1:8000/", timeout=2)
    print(f"✅ FastAPI server is running (Status: {response.status_code})")

    # Check if AI endpoints exist
    print("\n   Checking AI endpoints:")
    endpoints = ["/ai/review_code", "/ai/improve_code", "/ai/generate_tests"]

    for endpoint in endpoints:
        try:
            # Try OPTIONS request to check if endpoint exists
            res = requests.options(f"http://127.0.0.1:8000{endpoint}", timeout=2)
            if res.status_code != 404:
                print(f"   ✅ {endpoint} exists")
            else:
                print(f"   ❌ {endpoint} NOT FOUND (404)")
        except:
            print(f"   ❌ {endpoint} cannot be reached")

except requests.exceptions.ConnectionError:
    print("❌ FastAPI server is NOT running")
    print("   Run: python main.py")
except Exception as e:
    print(f"❌ Error checking server: {str(e)}")

print("\n📊 Summary:")
print("=" * 60)
if all_files_exist:
    print("✅ All required files present")
else:
    print("❌ Some files are missing - check above")

if all_packages_installed:
    print("✅ All packages installed")
else:
    print("❌ Some packages missing - run: pip install -r requirements.txt")

if api_key_set:
    print("✅ Anthropic API key is configured")
else:
    print("❌ Anthropic API key not set - check .env file")

print("\n💡 Next Steps:")
print("-" * 60)
if not all_files_exist:
    print("1. Create missing files from the artifacts provided")
if not all_packages_installed:
    print("2. Install missing packages: pip install -r requirements.txt")
if not api_key_set:
    print("3. Set ANTHROPIC_API_KEY in .env file")
print("4. Restart FastAPI server: python main.py")
print("5. Restart Streamlit: streamlit run streamlit_app.py")

print("\n" + "=" * 60)
print("DIAGNOSTIC CHECK COMPLETE")
print("=" * 60)
