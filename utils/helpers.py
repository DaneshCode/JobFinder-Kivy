"""
توابع کمکی برنامه جاب فایندر
شامل توابع رمزنگاری، اعتبارسنجی و فرمت‌بندی
"""

import uuid
import hashlib
import re


# تولید کد کاربری یکتا با استفاده از UUID
def generate_user_code():
    """تولید یک کد کاربری منحصربه‌فرد"""
    return f"JF-{uuid.uuid4().hex[:8].upper()}"


# هش کردن رمز عبور با الگوریتم SHA-256 برای ذخیره امن در دیتابیس
def hash_password(password: str) -> str:
    """هش کردن رمز عبور با SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


# بررسی صحت رمز عبور با مقایسه هش آن با هش ذخیره شده
def verify_password(password: str, hashed: str) -> bool:
    """بررسی رمز عبور با مقایسه هش"""
    return hash_password(password) == hashed


# اعتبارسنجی فرمت ایمیل با استفاده از عبارت منظم (Regex)
def validate_email(email: str) -> bool:
    """بررسی صحت فرمت ایمیل"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


# بررسی قدرت رمز عبور - حداقل ۶ کاراکتر باید داشته باشد
def validate_password(password: str) -> tuple:
    """
    بررسی قدرت رمز عبور
    خروجی: (معتبر است یا نه، پیام)
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, "Password is valid"


# فرمت‌بندی حقوق برای نمایش به کاربر - تبدیل عدد به فرمت دلاری
def format_salary(salary):
    """فرمت‌بندی حقوق برای نمایش"""
    if salary is None or salary == 0:
        return "Not specified"
    return f"${salary:,.0f}/year"
