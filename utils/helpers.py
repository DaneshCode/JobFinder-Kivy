"""
Job Finder application helper functions
Includes encryption, validation, and formatting utilities
"""

import uuid
import hashlib
import re


# Generate a unique user code using UUID
def generate_user_code():
    """Generate a unique user code"""
    return f"JF-{uuid.uuid4().hex[:8].upper()}"


# Hash password using SHA-256 algorithm for secure database storage
def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


# Verify password by comparing its hash with the stored hash
def verify_password(password: str, hashed: str) -> bool:
    """Verify password by comparing hashes"""
    return hash_password(password) == hashed


# Validate email format using regular expression (Regex)
def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


# Check password strength - must be at least 6 characters
def validate_password(password: str) -> tuple:
    """
    Check password strength
    Returns: (is_valid, message)
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, "Password is valid"


# Format salary for display - convert number to dollar format
def format_salary(salary):
    """Format salary for display"""
    if salary is None or salary == 0:
        return "Not specified"
    return f"${salary:,.0f}/year"
