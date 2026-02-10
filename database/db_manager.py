"""
Database Manager for Job Finder application
Handles all database operations using SQLite
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Optional
import random

from .models import User, Job, Advertisement


class DatabaseManager:
    """Singleton Database Manager"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # Get app data directory
        self.db_path = self._get_db_path()
        self.conn = None
        self._initialized = True
        self.initialize_database()

    def _get_db_path(self):
        """Get the database path based on platform"""
        try:
            from android.storage import app_storage_path

            return os.path.join(app_storage_path(), "jobfinder.db")
        except ImportError:
            # Running on desktop
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
            os.makedirs(data_dir, exist_ok=True)
            return os.path.join(data_dir, "jobfinder.db")

    def get_connection(self):
        """Get database connection"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        return self.conn

    def initialize_database(self):
        """Create database tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
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

        # Jobs table
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

        # Advertisements table
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

        conn.commit()

        # Seed initial data if tables are empty
        self._seed_initial_data()

    def _seed_initial_data(self):
        """Seed initial jobs and advertisements"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Check if jobs exist
        cursor.execute("SELECT COUNT(*) FROM jobs")
        if cursor.fetchone()[0] == 0:
            self._seed_jobs()

        # Check if ads exist
        cursor.execute("SELECT COUNT(*) FROM advertisements")
        if cursor.fetchone()[0] == 0:
            self._seed_advertisements()

    def _seed_jobs(self):
        """Seed sample job listings"""
        jobs = [
            # ============ Computer Engineering ============
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
            # ============ Architecture ============
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
            # ============ Civil Engineering ============
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
            # ============ Accounting ============
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
            # ============ Electrical Engineering ============
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
            # ============ Mechanical Engineering ============
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
            # ============ Healthcare ============
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
            # ============ Law ============
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
            # ============ Marketing ============
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
            # ============ Education ============
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
        """Seed sample advertisements"""
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

        for ad in ads:
            cursor.execute(
                """
                INSERT INTO advertisements (title, description, company, payment_weight, icon)
                VALUES (?, ?, ?, ?, ?)
            """,
                ad,
            )

        conn.commit()

    # User operations
    def create_user(
        self, name: str, email: str, password_hash: str, specialty: str, user_code: str
    ) -> Optional[int]:
        """Create a new user"""
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
            return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
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
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
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
        """Update user's resume path"""
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
        """Update user profile"""
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

    # Job operations
    def get_all_jobs(self) -> List[Job]:
        """Get all jobs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs ORDER BY created_at DESC")
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

    def search_jobs(self, keyword: str) -> List[Job]:
        """Search jobs by keyword"""
        conn = self.get_connection()
        cursor = conn.cursor()
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
        """Get job by ID"""
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
        """Get all unique job categories"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM jobs ORDER BY category")
        rows = cursor.fetchall()
        return [row["category"] for row in rows]

    def get_jobs_by_category(self, category: str) -> List[Job]:
        """Get jobs filtered by category"""
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
        """Search jobs by keyword with optional category filter"""
        conn = self.get_connection()
        cursor = conn.cursor()
        search_term = f"%{keyword}%"

        if category and category != "All":
            cursor.execute(
                """
                SELECT * FROM jobs
                WHERE category = ? AND (title LIKE ? OR company LIKE ? OR country LIKE ? OR description LIKE ?)
                ORDER BY created_at DESC
                """,
                (category, search_term, search_term, search_term, search_term),
            )
        else:
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

    # Advertisement operations
    def get_active_advertisements(self) -> List[Advertisement]:
        """Get all active advertisements"""
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
        """Get a random advertisement weighted by payment"""
        ads = self.get_active_advertisements()
        if not ads:
            return None

        # Create weighted list
        weighted_ads = []
        for ad in ads:
            weighted_ads.extend([ad] * ad.payment_weight)

        return random.choice(weighted_ads)

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
