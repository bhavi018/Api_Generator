"""
AI Code Reviewer using Claude
Analyzes code for security, performance, and best practices
"""

import anthropic
import os
import json
from typing import Dict, List
import re


class AICodeReviewer:
    """AI-powered code reviewer using Claude"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def review_code(self, code: str, language: str) -> Dict:
        """
        Comprehensive code review

        Returns:
        {
            "overall_score": 8.5,
            "security_issues": [...],
            "performance_issues": [...],
            "best_practices": [...],
            "code_smells": [...],
            "suggestions": [...]
        }
        """

        prompt = f"""You are an expert code reviewer specializing in {language}. 
        
Analyze this code and provide a detailed review in JSON format.

Code to review:
```{language}
{code}
```

Provide your analysis in this exact JSON structure:
{{
    "overall_score": <number 1-10>,
    "summary": "<brief summary>",
    "security_issues": [
        {{
            "severity": "<critical|high|medium|low>",
            "line": <line_number or "multiple">,
            "issue": "<description>",
            "recommendation": "<how to fix>",
            "example": "<code example if applicable>"
        }}
    ],
    "performance_issues": [
        {{
            "severity": "<high|medium|low>",
            "line": <line_number or "multiple">,
            "issue": "<description>",
            "recommendation": "<how to fix>",
            "impact": "<performance impact>"
        }}
    ],
    "best_practices": [
        {{
            "category": "<naming|structure|documentation|error_handling>",
            "suggestion": "<description>",
            "importance": "<high|medium|low>"
        }}
    ],
    "code_quality_metrics": {{
        "readability": <1-10>,
        "maintainability": <1-10>,
        "testability": <1-10>,
        "documentation": <1-10>
    }},
    "positive_aspects": [
        "<list good practices found>"
    ]
}}

Focus on:
1. Security vulnerabilities (SQL injection, XSS, authentication issues)
2. Performance bottlenecks (N+1 queries, inefficient algorithms)
3. Code organization and structure
4. Error handling and validation
5. Best practices for {language}"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=4000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}],
            )

            # Extract JSON from response
            response_text = message.content[0].text
            json_match = re.search(r"\{[\s\S]*\}", response_text)

            if json_match:
                review_data = json.loads(json_match.group(0))
                return review_data
            else:
                return self._create_error_response("Failed to parse AI response")

        except Exception as e:
            return self._create_error_response(str(e))

    def suggest_improvements(self, code: str, language: str) -> str:
        """Generate improved version of the code"""

        prompt = f"""You are an expert {language} developer. Improve this code by:
1. Fixing security issues
2. Optimizing performance
3. Following best practices
4. Adding proper error handling
5. Improving code structure

Original Code:
```{language}
{code}
```

Return ONLY the improved code without explanations."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=8000,
                temperature=0.2,
                messages=[{"role": "user", "content": prompt}],
            )

            improved_code = message.content[0].text
            # Remove markdown code blocks if present
            improved_code = re.sub(r"```[\w]*\n?", "", improved_code).strip()
            return improved_code

        except Exception as e:
            return f"Error generating improvements: {str(e)}"

    def explain_code(self, code: str, language: str) -> str:
        """Generate detailed explanation of the code"""

        prompt = f"""Explain this {language} code in a clear, educational way.

Code:
```{language}
{code}
```

Provide:
1. High-level overview of what the code does
2. Explanation of key components
3. How different parts interact
4. Important patterns or techniques used
5. Potential use cases

Make it suitable for someone learning {language}."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=3000,
                temperature=0.5,
                messages=[{"role": "user", "content": prompt}],
            )

            return message.content[0].text

        except Exception as e:
            return f"Error generating explanation: {str(e)}"

    def generate_tests(self, code: str, language: str) -> str:
        """Generate test cases for the code"""

        test_frameworks = {
            "python": "pytest",
            "java": "JUnit 5",
            "javascript": "Jest",
            "csharp": "xUnit",
        }

        framework = test_frameworks.get(
            language.lower(), "appropriate testing framework"
        )

        prompt = f"""Generate comprehensive test cases for this {language} code using {framework}.

Code to test:
```{language}
{code}
```

Generate tests that cover:
1. Happy path scenarios
2. Edge cases
3. Error handling
4. Input validation
5. Integration scenarios (if applicable)

Return complete, runnable test code."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=6000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}],
            )

            test_code = message.content[0].text
            test_code = re.sub(r"```[\w]*\n?", "", test_code).strip()
            return test_code

        except Exception as e:
            return f"Error generating tests: {str(e)}"

    def _create_error_response(self, error_message: str) -> Dict:
        """Create error response in expected format"""
        return {
            "overall_score": 0,
            "summary": f"Error during review: {error_message}",
            "security_issues": [],
            "performance_issues": [],
            "best_practices": [],
            "code_quality_metrics": {
                "readability": 0,
                "maintainability": 0,
                "testability": 0,
                "documentation": 0,
            },
            "positive_aspects": [],
            "error": error_message,
        }


class SecurityScanner:
    """Specialized security vulnerability scanner"""

    def __init__(self):
        self.vulnerability_patterns = {
            "sql_injection": [
                r"\.execute\([^?]*\+",  # String concatenation in SQL
                r"f['\"].*SELECT.*{",  # f-string in SQL
            ],
            "xss": [
                r"innerHTML\s*=",
                r"dangerouslySetInnerHTML",
            ],
            "hardcoded_secrets": [
                r"password\s*=\s*['\"][^'\"]+['\"]",
                r"api_key\s*=\s*['\"][^'\"]+['\"]",
                r"secret\s*=\s*['\"][^'\"]+['\"]",
            ],
            "weak_crypto": [
                r"md5\(",
                r"sha1\(",
            ],
        }

    def scan(self, code: str) -> List[Dict]:
        """Quick pattern-based security scan"""
        issues = []

        for vuln_type, patterns in self.vulnerability_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, code, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    line_num = code[: match.start()].count("\n") + 1
                    issues.append(
                        {
                            "type": vuln_type,
                            "line": line_num,
                            "severity": "high",
                            "code_snippet": match.group(0),
                        }
                    )

        return issues


# Utility functions for integration with FastAPI
def review_generated_code(code: str, language: str, api_key: str = None) -> Dict:
    """Main function to review generated code"""
    try:
        reviewer = AICodeReviewer(api_key)
        review_result = reviewer.review_code(code, language)

        # Add quick security scan
        scanner = SecurityScanner()
        quick_scan = scanner.scan(code)

        if quick_scan:
            review_result["quick_security_scan"] = quick_scan

        return review_result
    except Exception as e:
        return {
            "error": str(e),
            "message": "Failed to perform code review. Please check API key.",
        }


def get_code_improvements(code: str, language: str, api_key: str = None) -> str:
    """Get improved version of code"""
    try:
        reviewer = AICodeReviewer(api_key)
        return reviewer.suggest_improvements(code, language)
    except Exception as e:
        return f"Error: {str(e)}"


def generate_code_tests(code: str, language: str, api_key: str = None) -> str:
    """Generate test suite for code"""
    try:
        reviewer = AICodeReviewer(api_key)
        return reviewer.generate_tests(code, language)
    except Exception as e:
        return f"Error: {str(e)}"


# Example usage
if __name__ == "__main__":
    sample_code = """
    from fastapi import FastAPI
    
    app = FastAPI()
    
    @app.get("/users/{user_id}")
    def get_user(user_id: str):
        # Vulnerable SQL query
        query = "SELECT * FROM users WHERE id = " + user_id
        result = db.execute(query)
        return result
    """

    reviewer = AICodeReviewer()
    review = reviewer.review_code(sample_code, "python")
    print(json.dumps(review, indent=2))
