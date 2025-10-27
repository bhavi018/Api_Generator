from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import User, UserDB
from database import engine, Base, get_db
from utils import generate_org_id, generate_api_key
from auth import create_access_token, verify_token
from code_translator import get_code_for_language
from pydantic import BaseModel
from typing import Optional

# Import AI reviewer functions
try:
    from ai_code_reviewer import (
        review_generated_code,
        get_code_improvements,
        generate_code_tests,
    )

    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("Warning: AI code reviewer not available. Install 'anthropic' package.")

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Code Generator with Multi-Language Support & AI Review",
    description="Generate REST APIs in multiple languages with AI-powered code review",
    version="2.0.0",
)

db_orgs = {}


# Request models for AI features
class CodeReviewRequest(BaseModel):
    code: str
    language: str
    api_key: Optional[str] = None


class CodeImprovementRequest(BaseModel):
    code: str
    language: str
    api_key: Optional[str] = None


@app.get("/")
def read_root():
    return {
        "message": "FastAPI Code Generator API",
        "version": "2.0",
        "ai_available": AI_AVAILABLE,
        "endpoints": {
            "generate_org": "/generate_org",
            "generate_code": "/generate_sample_code",
            "ai_review": "/ai/review_code",
            "ai_improve": "/ai/improve_code",
            "ai_tests": "/ai/generate_tests",
            "supported_languages": "/supported_languages",
        },
    }


@app.get("/generate_org")
def generate_org(name: str):
    """Generate organization with unique ID and API key"""
    org_id = generate_org_id(name)
    api_key = generate_api_key()
    if org_id not in db_orgs:
        db_orgs[org_id] = {"api_key": api_key}
    return {"org_id": org_id, "api_key": api_key, "org_name": name}


# --------------------------
# CRUD endpoints using DB
# --------------------------


@app.post("/api/org/{org_id}/users/")
def create_user(
    org_id: str,
    user: User,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token),
):
    """Create a new user (Admin only)"""
    if token_data["org_id"] != org_id or token_data["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    user_db = UserDB(**user.dict())
    db.add(user_db)
    try:
        db.commit()
        db.refresh(user_db)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "User created", "user": user_db}


@app.get("/api/org/{org_id}/users/{org_user_id}")
def get_user(org_id: str, org_user_id: str, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = db.query(UserDB).filter_by(org_user_id=org_user_id, org_id=org_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/api/org/{org_id}/users/{org_user_id}")
def update_user(
    org_id: str,
    org_user_id: str,
    updated_user: User,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token),
):
    """Update user (Admin only)"""
    if token_data["org_id"] != org_id or token_data["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    user = db.query(UserDB).filter_by(org_user_id=org_user_id, org_id=org_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in updated_user.dict().items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return {"message": "User updated", "user": user}


@app.delete("/api/org/{org_id}/users/{org_user_id}")
def delete_user(
    org_id: str,
    org_user_id: str,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token),
):
    """Delete user (Admin only)"""
    if token_data["org_id"] != org_id or token_data["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    user = db.query(UserDB).filter_by(org_user_id=org_user_id, org_id=org_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}


@app.post("/token")
def login(org_id: str, role: str = "user"):
    """Generate access token"""
    token = create_access_token(data={"org_id": org_id, "role": role})
    return {"access_token": token, "token_type": "bearer"}


# --------------------------
# Code Generation Endpoints
# --------------------------


@app.get("/generate_sample_code")
def generate_sample_code(org_id: str, org_name: str, language: str = "python"):
    """
    Generate CRUD API code in specified programming language

    Supported languages:
    - python (FastAPI)
    - java (Spring Boot)
    - javascript (Node.js + Express)
    - csharp (ASP.NET Core)
    """
    result = get_code_for_language(language, org_id, org_name)

    if "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"],
            headers={
                "X-Supported-Languages": ",".join(result.get("supported_languages", []))
            },
        )

    return {
        "generated_code": result["code"],
        "language": result["language"],
        "file_extension": result["extension"],
        "mime_type": result["mime_type"],
        "org_id": org_id,
        "org_name": org_name,
    }


@app.get("/supported_languages")
def get_supported_languages():
    """Get list of supported programming languages"""
    return {
        "languages": [
            {
                "name": "Python",
                "value": "python",
                "framework": "FastAPI",
                "description": "High-performance async Python web framework",
            },
            {
                "name": "Java",
                "value": "java",
                "framework": "Spring Boot",
                "description": "Enterprise-grade Java framework",
            },
            {
                "name": "JavaScript",
                "value": "javascript",
                "framework": "Node.js + Express",
                "description": "Fast, unopinionated web framework for Node.js",
            },
            {
                "name": "C#",
                "value": "csharp",
                "framework": "ASP.NET Core",
                "description": "Cross-platform .NET framework",
            },
        ]
    }


# --------------------------
# AI Code Review Endpoints
# --------------------------


@app.post("/ai/review_code")
def ai_review_code(request: CodeReviewRequest):
    """
    AI-powered code review
    Analyzes security, performance, and best practices
    """
    if not AI_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="AI features not available. Install 'anthropic' package: pip install anthropic",
        )

    try:
        review_result = review_generated_code(
            request.code, request.language, request.api_key
        )
        return review_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI review failed: {str(e)}")


@app.post("/ai/improve_code")
def ai_improve_code(request: CodeImprovementRequest):
    """
    Get AI-improved version of code
    Fixes security issues, optimizes performance, follows best practices
    """
    if not AI_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="AI features not available. Install 'anthropic' package: pip install anthropic",
        )

    try:
        improved_code = get_code_improvements(
            request.code, request.language, request.api_key
        )
        return {
            "original_code": request.code,
            "improved_code": improved_code,
            "language": request.language,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Code improvement failed: {str(e)}"
        )


@app.post("/ai/generate_tests")
def ai_generate_tests(request: CodeReviewRequest):
    """
    Generate comprehensive test suite for code
    """
    if not AI_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="AI features not available. Install 'anthropic' package: pip install anthropic",
        )

    try:
        test_code = generate_code_tests(request.code, request.language, request.api_key)
        return {
            "test_code": test_code,
            "language": request.language,
            "framework": {
                "python": "pytest",
                "java": "JUnit 5",
                "javascript": "Jest",
                "csharp": "xUnit",
            }.get(request.language.lower(), "standard testing framework"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test generation failed: {str(e)}")


# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "ai_available": AI_AVAILABLE, "database": "connected"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
