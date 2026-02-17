"""
Job Finder application data models
Includes User, Job, and Advertisement models
"""

from dataclasses import dataclass, field
from typing import Optional


# User model - stores registered user information
@dataclass
class User:
    """User model"""

    id: Optional[int] = None
    name: str = ""
    email: str = ""
    password_hash: str = ""
    specialty: str = ""
    user_code: str = ""
    resume_path: Optional[str] = None
    created_at: Optional[str] = None

    # Convert user data to dictionary for API or display usage
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "specialty": self.specialty,
            "user_code": self.user_code,
            "resume_path": self.resume_path,
            "created_at": self.created_at,
        }


# Job model - stores job listing information
@dataclass
class Job:
    """Job listing model"""

    id: Optional[int] = None
    title: str = ""
    category: str = ""
    company: str = ""
    country: str = ""
    salary: Optional[float] = None
    description: str = ""
    created_at: Optional[str] = None

    # Convert job data to dictionary
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "company": self.company,
            "country": self.country,
            "salary": self.salary,
            "description": self.description,
            "created_at": self.created_at,
        }


# Advertisement model - stores ad banner information with display weight
@dataclass
class Advertisement:
    """Advertisement model"""

    id: Optional[int] = None
    title: str = ""
    description: str = ""
    company: str = ""
    payment_weight: int = 1  # Display weight - higher value means more frequent display
    icon: str = "bullhorn"
    active: bool = True
    created_at: Optional[str] = None

    # Convert advertisement data to dictionary
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "company": self.company,
            "payment_weight": self.payment_weight,
            "icon": self.icon,
            "active": self.active,
            "created_at": self.created_at,
        }
