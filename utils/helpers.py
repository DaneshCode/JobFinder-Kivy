"""
Utility helper functions for Job Finder application
"""

import uuid
import hashlib
import re


def generate_user_code():
    """Generate a unique user code"""
    return f"JF-{uuid.uuid4().hex[:8].upper()}"


def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return hash_password(password) == hashed


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_password(password: str) -> tuple:
    """
    Validate password strength
    Returns (is_valid, message)
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, "Password is valid"


def format_salary(salary):
    """Format salary for display"""
    if salary is None or salary == 0:
        return "Not specified"
    return f"${salary:,.0f}/year"
