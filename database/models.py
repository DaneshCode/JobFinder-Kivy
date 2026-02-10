"""
مدل‌های داده برنامه جاب فایندر
شامل مدل‌های کاربر، شغل و تبلیغات
"""

from dataclasses import dataclass, field
from typing import Optional


# مدل کاربر - نگهداری اطلاعات کاربران ثبت‌نام شده
@dataclass
class User:
    """مدل کاربر"""

    id: Optional[int] = None
    name: str = ""
    email: str = ""
    password_hash: str = ""
    specialty: str = ""
    user_code: str = ""
    resume_path: Optional[str] = None
    created_at: Optional[str] = None

    # تبدیل اطلاعات کاربر به دیکشنری برای استفاده در API یا نمایش
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


# مدل شغل - نگهداری اطلاعات آگهی‌های شغلی
@dataclass
class Job:
    """مدل آگهی شغلی"""

    id: Optional[int] = None
    title: str = ""
    category: str = ""
    company: str = ""
    country: str = ""
    salary: Optional[float] = None
    description: str = ""
    created_at: Optional[str] = None

    # تبدیل اطلاعات شغل به دیکشنری
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


# مدل تبلیغات - نگهداری اطلاعات بنرهای تبلیغاتی با وزن نمایش
@dataclass
class Advertisement:
    """مدل تبلیغات"""

    id: Optional[int] = None
    title: str = ""
    description: str = ""
    company: str = ""
    payment_weight: int = 1  # وزن نمایش - هرچه بیشتر باشد بیشتر نمایش داده می‌شود
    icon: str = "bullhorn"
    active: bool = True
    created_at: Optional[str] = None

    # تبدیل اطلاعات تبلیغ به دیکشنری
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
