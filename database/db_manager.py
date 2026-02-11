"""
مدیریت پایگاه داده برنامه Job Finder
این ماژول تمام عملیات پایگاه داده را با استفاده از SQLite انجام می‌دهد
"""

# وارد کردن کتابخانه‌های مورد نیاز
import sqlite3
import os
from datetime import datetime
from typing import List, Optional
import random

# وارد کردن مدل‌های داده
from .models import User, Job, Advertisement


class DatabaseManager:
    """کلاس مدیریت پایگاه داده - از الگوی Singleton استفاده می‌کند"""

    # متغیر برای نگهداری تنها نمونه از کلاس
    _instance = None

    def __new__(cls):
        """ایجاد نمونه جدید فقط اگر قبلاً ایجاد نشده باشد (الگوی Singleton)"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """مقداردهی اولیه - فقط یکبار اجرا می‌شود"""
        if self._initialized:
            return

        # دریافت مسیر پایگاه داده
        self.db_path = self._get_db_path()
        self.conn = None
        self._initialized = True
        # ایجاد جداول پایگاه داده
        self.initialize_database()

    def _get_db_path(self):
        """تعیین مسیر فایل پایگاه داده بر اساس پلتفرم (اندروید یا دسکتاپ)"""
        try:
            # تلاش برای اجرا روی اندروید
            from android.storage import app_storage_path  # type: ignore[import-not-found]

            return os.path.join(app_storage_path(), "jobfinder.db")
        except ImportError:
            # اجرا روی دسکتاپ - ذخیره در پوشه data
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
            os.makedirs(data_dir, exist_ok=True)
            return os.path.join(data_dir, "jobfinder.db")

    def get_connection(self):
        """دریافت اتصال به پایگاه داده - در صورت نیاز اتصال جدید ایجاد می‌کند"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            # تنظیم برای دسترسی به ستون‌ها با نام
            self.conn.row_factory = sqlite3.Row
        return self.conn

    def initialize_database(self):
        """ایجاد جداول پایگاه داده در صورت عدم وجود"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # جدول کاربران - ذخیره اطلاعات کاربران ثبت‌نام شده
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                specialty TEXT,
                user_code TEXT UNIQUE NOT NULL,
                resume_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # جدول مشاغل - ذخیره آگهی‌های شغلی
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                company TEXT NOT NULL,
                country TEXT NOT NULL,
                salary REAL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # جدول تبلیغات - ذخیره تبلیغات نمایشی
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS advertisements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                company TEXT NOT NULL,
                payment_weight INTEGER DEFAULT 1,
                icon TEXT DEFAULT 'bullhorn',
                active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # ایجاد ایندکس‌ها برای جستجوی سریع‌تر
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_category ON jobs(category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_title ON jobs(title)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_country ON jobs(country)")

        conn.commit()

        # درج داده‌های اولیه اگر جداول خالی هستند
        self._seed_initial_data()

    def _seed_initial_data(self):
        """درج داده‌های نمونه اولیه در صورت خالی بودن جداول"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # بررسی وجود مشاغل
        cursor.execute("SELECT COUNT(*) FROM jobs")
        if cursor.fetchone()[0] == 0:
            self._seed_jobs()

        # بررسی وجود تبلیغات
        cursor.execute("SELECT COUNT(*) FROM advertisements")
        if cursor.fetchone()[0] == 0:
            self._seed_advertisements()

    def _seed_jobs(self):
        """درج مشاغل نمونه در پایگاه داده"""
        # لیست مشاغل نمونه با دسته‌بندی‌های مختلف
        jobs = [
            # ============ مهندسی کامپیوتر ============
            (
                "Senior Python Developer",
                "Computer Engineering",
                "TechCorp Inc.",
                "United States",
                120000,
                "We are looking for an experienced Python developer to join our team. You will work on cutting-edge projects using Django, FastAPI, and machine learning technologies.",
            ),
            (
                "Full Stack Developer",
                "Computer Engineering",
                "StartupX",
                "Israel",
                85000,
                "Work on both frontend and backend using Node.js, React, and PostgreSQL in a fast-paced startup environment.",
            ),
            # ============ معماری ============
            (
                "Senior Architect",
                "Architecture",
                "DesignBuild Studio",
                "United States",
                95000,
                "Lead architectural design projects for commercial and residential buildings with sustainable design focus.",
            ),
            (
                "Interior Designer",
                "Architecture",
                "Modern Interiors",
                "United Kingdom",
                55000,
                "Create innovative interior designs for luxury homes and commercial spaces.",
            ),
            # ============ مهندسی عمران ============
            (
                "Structural Engineer",
                "Civil Engineering",
                "StructureTech",
                "United States",
                88000,
                "Design and analyze structural systems for bridges, buildings, and infrastructure projects.",
            ),
            (
                "Construction Manager",
                "Civil Engineering",
                "BuildMaster Corp.",
                "Germany",
                92000,
                "Oversee construction projects ensuring quality, safety, and budget compliance.",
            ),
            # ============ حسابداری ============
            (
                "Senior Accountant",
                "Accounting",
                "FinanceFirst Corp.",
                "United States",
                75000,
                "Manage financial records, prepare reports, and ensure regulatory compliance.",
            ),
            (
                "Tax Specialist",
                "Accounting",
                "TaxPro Advisors",
                "Canada",
                82000,
                "Provide tax planning and compliance services for corporate clients.",
            ),
            # ============ مهندسی برق ============
            (
                "Power Systems Engineer",
                "Electrical Engineering",
                "PowerGrid Corp.",
                "United States",
                92000,
                "Design and maintain electrical power generation and distribution systems.",
            ),
            (
                "Electronics Engineer",
                "Electrical Engineering",
                "CircuitTech",
                "Japan",
                78000,
                "Design electronic circuits and components for consumer products.",
            ),
            # ============ مهندسی مکانیک ============
            (
                "HVAC Engineer",
                "Mechanical Engineering",
                "ClimateControl Inc.",
                "United States",
                78000,
                "Design heating, ventilation, and air conditioning systems for buildings.",
            ),
            (
                "Automotive Engineer",
                "Mechanical Engineering",
                "AutoDesign Corp.",
                "Germany",
                88000,
                "Design and develop automotive components and systems.",
            ),
            # ============ بهداشت و درمان ============
            (
                "Registered Nurse",
                "Healthcare",
                "CityMedical Hospital",
                "United States",
                72000,
                "Provide patient care and coordinate with healthcare team members.",
            ),
            (
                "Pharmacist",
                "Healthcare",
                "PharmaCare",
                "Australia",
                98000,
                "Dispense medications and provide pharmaceutical consultation.",
            ),
            # ============ حقوق ============
            (
                "Corporate Lawyer",
                "Law",
                "LegalEagle LLP",
                "United States",
                145000,
                "Provide legal counsel on corporate transactions and compliance.",
            ),
            (
                "Immigration Lawyer",
                "Law",
                "VisaExperts",
                "Canada",
                88000,
                "Assist clients with immigration applications and legal issues.",
            ),
            # ============ بازاریابی ============
            (
                "Digital Marketing Manager",
                "Marketing",
                "DigitalGrowth Inc.",
                "United States",
                85000,
                "Lead digital marketing campaigns across multiple channels.",
            ),
            (
                "SEO Specialist",
                "Marketing",
                "SearchRank Pro",
                "Canada",
                62000,
                "Optimize website content for search engine visibility.",
            ),
            # ============ آموزش ============
            (
                "University Professor",
                "Education",
                "StateUniversity",
                "Canada",
                95000,
                "Conduct research and teach undergraduate and graduate courses.",
            ),
            (
                "Corporate Trainer",
                "Education",
                "SkillUp Training",
                "Japan",
                58000,
                "Develop and deliver professional training programs.",
            ),
        ]

        conn = self.get_connection()
        cursor = conn.cursor()

        # درج هر شغل در پایگاه داده
        for job in jobs:
            cursor.execute(
                """
                INSERT INTO jobs (title, category, company, country, salary, description)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                job,
            )

        conn.commit()

    def _seed_advertisements(self):
        """درج تبلیغات نمونه در پایگاه داده"""
        # لیست تبلیغات نمونه
        ads = [
            (
                "Learn Python Today!",
                "Master Python programming with our comprehensive course. 50% off this week!",
                "CodeAcademy Pro",
                5,
                "school",
            ),
            (
                "Cloud Certification",
                "Get AWS certified and boost your career. Free practice exams included!",
                "CloudLearn",
                3,
                "cloud",
            ),
            (
                "Resume Builder",
                "Create professional resumes in minutes with our AI-powered tool.",
                "ResumeGenius",
                4,
                "file-document",
            ),
            (
                "Remote Jobs Platform",
                "Find the best remote jobs worldwide. Join 1M+ professionals.",
                "RemoteOK",
                2,
                "earth",
            ),
            (
                "Coding Bootcamp",
                "Become a full-stack developer in 12 weeks. Job guarantee!",
                "TechBootcamp",
                5,
                "laptop",
            ),
            (
                "Interview Prep",
                "Ace your tech interviews with our mock interviews and practice problems.",
                "InterviewPro",
                3,
                "account-tie",
            ),
            (
                "Freelance Network",
                "Connect with clients and find freelance projects in tech.",
                "FreelanceHub",
                2,
                "handshake",
            ),
            (
                "Salary Insights",
                "Know your worth! Get detailed salary data for tech roles.",
                "PayScale Tech",
                1,
                "currency-usd",
            ),
        ]

        conn = self.get_connection()
        cursor = conn.cursor()

        # درج هر تبلیغ در پایگاه داده
        for ad in ads:
            cursor.execute(
                """
                INSERT INTO advertisements (title, description, company, payment_weight, icon)
                VALUES (?, ?, ?, ?, ?)
            """,
                ad,
            )

        conn.commit()

    # ==================== عملیات مربوط به کاربران ====================

    def create_user(
        self, name: str, email: str, password_hash: str, specialty: str, user_code: str
    ) -> Optional[int]:
        """ایجاد کاربر جدید در پایگاه داده - در صورت موفقیت شناسه کاربر را برمی‌گرداند"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (name, email, password_hash, specialty, user_code)
                VALUES (?, ?, ?, ?, ?)
            """,
                (name, email, password_hash, specialty, user_code),
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # ایمیل یا کد کاربری تکراری است
            return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """دریافت کاربر بر اساس ایمیل"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            # تبدیل ردیف پایگاه داده به شیء User
            return User(
                id=row["id"],
                name=row["name"],
                email=row["email"],
                password_hash=row["password_hash"],
                specialty=row["specialty"],
                user_code=row["user_code"],
                resume_path=row["resume_path"],
                created_at=row["created_at"],
            )
        return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """دریافت کاربر بر اساس شناسه"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            # تبدیل ردیف پایگاه داده به شیء User
            return User(
                id=row["id"],
                name=row["name"],
                email=row["email"],
                password_hash=row["password_hash"],
                specialty=row["specialty"],
                user_code=row["user_code"],
                resume_path=row["resume_path"],
                created_at=row["created_at"],
            )
        return None

    def update_user_resume(self, user_id: int, resume_path: str) -> bool:
        """به‌روزرسانی مسیر رزومه کاربر"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE users SET resume_path = ? WHERE id = ?
            """,
                (resume_path, user_id),
            )
            conn.commit()
            return True
        except Exception:
            return False

    def update_user_profile(self, user_id: int, name: str, specialty: str) -> bool:
        """به‌روزرسانی پروفایل کاربر (نام و تخصص)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE users SET name = ?, specialty = ? WHERE id = ?
            """,
                (name, specialty, user_id),
            )
            conn.commit()
            return True
        except Exception:
            return False

    # ==================== عملیات مربوط به مشاغل ====================

    def get_jobs_count(self) -> int:
        """دریافت تعداد کل مشاغل (کوئری سریع)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM jobs")
        return cursor.fetchone()[0]

    def get_countries_count(self) -> int:
        """دریافت تعداد کشورهای یکتا (کوئری سریع)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(DISTINCT country) FROM jobs")
        return cursor.fetchone()[0]

    def get_all_jobs(self, limit: int = 0, offset: int = 0) -> List[Job]:
        """دریافت همه مشاغل با امکان صفحه‌بندی"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if limit > 0:
            # با محدودیت تعداد
            cursor.execute(
                "SELECT * FROM jobs ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (limit, offset),
            )
        else:
            # همه مشاغل
            cursor.execute("SELECT * FROM jobs ORDER BY created_at DESC")
        rows = cursor.fetchall()
        # تبدیل ردیف‌ها به لیست اشیاء Job
        return [
            Job(
                id=row["id"],
                title=row["title"],
                category=row["category"],
                company=row["company"],
                country=row["country"],
                salary=row["salary"],
                description=row["description"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def search_jobs(self, keyword: str) -> List[Job]:
        """جستجوی مشاغل بر اساس کلمه کلیدی"""
        conn = self.get_connection()
        cursor = conn.cursor()
        # جستجو در همه فیلدهای متنی
        search_term = f"%{keyword}%"
        cursor.execute(
            """
            SELECT * FROM jobs
            WHERE title LIKE ? OR category LIKE ? OR company LIKE ?
                  OR country LIKE ? OR description LIKE ?
            ORDER BY created_at DESC
        """,
            (search_term, search_term, search_term, search_term, search_term),
        )
        rows = cursor.fetchall()
        return [
            Job(
                id=row["id"],
                title=row["title"],
                category=row["category"],
                company=row["company"],
                country=row["country"],
                salary=row["salary"],
                description=row["description"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def get_job_by_id(self, job_id: int) -> Optional[Job]:
        """دریافت شغل بر اساس شناسه"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        row = cursor.fetchone()
        if row:
            return Job(
                id=row["id"],
                title=row["title"],
                category=row["category"],
                company=row["company"],
                country=row["country"],
                salary=row["salary"],
                description=row["description"],
                created_at=row["created_at"],
            )
        return None

    def get_all_categories(self) -> List[str]:
        """دریافت لیست همه دسته‌بندی‌های یکتا"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM jobs ORDER BY category")
        rows = cursor.fetchall()
        return [row["category"] for row in rows]

    def get_jobs_by_category(self, category: str) -> List[Job]:
        """دریافت مشاغل فیلتر شده بر اساس دسته‌بندی"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM jobs WHERE category = ? ORDER BY created_at DESC",
            (category,),
        )
        rows = cursor.fetchall()
        return [
            Job(
                id=row["id"],
                title=row["title"],
                category=row["category"],
                company=row["company"],
                country=row["country"],
                salary=row["salary"],
                description=row["description"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def search_jobs_with_category(
        self, keyword: str, category: str = None
    ) -> List[Job]:
        """جستجوی مشاغل با کلمه کلیدی و فیلتر دسته‌بندی اختیاری"""
        conn = self.get_connection()
        cursor = conn.cursor()
        search_term = f"%{keyword}%"

        if category and category != "All":
            # جستجو با فیلتر دسته‌بندی
            cursor.execute(
                """
                SELECT * FROM jobs
                WHERE category = ? AND (title LIKE ? OR company LIKE ? OR country LIKE ? OR description LIKE ?)
                ORDER BY created_at DESC
                """,
                (category, search_term, search_term, search_term, search_term),
            )
        else:
            # جستجو در همه دسته‌بندی‌ها
            cursor.execute(
                """
                SELECT * FROM jobs
                WHERE title LIKE ? OR category LIKE ? OR company LIKE ?
                      OR country LIKE ? OR description LIKE ?
                ORDER BY created_at DESC
                """,
                (search_term, search_term, search_term, search_term, search_term),
            )

        rows = cursor.fetchall()
        return [
            Job(
                id=row["id"],
                title=row["title"],
                category=row["category"],
                company=row["company"],
                country=row["country"],
                salary=row["salary"],
                description=row["description"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    # ==================== عملیات مربوط به تبلیغات ====================

    def get_active_advertisements(self) -> List[Advertisement]:
        """دریافت همه تبلیغات فعال"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM advertisements WHERE active = 1")
        rows = cursor.fetchall()
        return [
            Advertisement(
                id=row["id"],
                title=row["title"],
                description=row["description"],
                company=row["company"],
                payment_weight=row["payment_weight"],
                icon=row["icon"],
                active=bool(row["active"]),
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def get_weighted_random_ad(self) -> Optional[Advertisement]:
        """دریافت یک تبلیغ تصادفی با وزن‌دهی بر اساس پرداخت"""
        ads = self.get_active_advertisements()
        if not ads:
            return None

        # ایجاد لیست وزن‌دار - تبلیغات با وزن بیشتر، شانس بیشتری دارند
        weighted_ads = []
        for ad in ads:
            weighted_ads.extend([ad] * ad.payment_weight)

        return random.choice(weighted_ads)

    def close(self):
        """بستن اتصال به پایگاه داده"""
        if self.conn:
            self.conn.close()
            self.conn = None
