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
            (
                "Senior Python Developer",
                "Software Development",
                "TechCorp Inc.",
                "United States",
                120000,
                "We are looking for an experienced Python developer to join our team. You will work on cutting-edge projects using Django, FastAPI, and machine learning technologies.",
            ),
            (
                "Frontend React Developer",
                "Software Development",
                "WebSolutions Ltd.",
                "Canada",
                95000,
                "Join our frontend team to build beautiful user interfaces using React, TypeScript, and modern CSS frameworks.",
            ),
            (
                "Data Scientist",
                "Data Science",
                "Analytics Pro",
                "United Kingdom",
                110000,
                "Analyze large datasets and build predictive models using Python, TensorFlow, and scikit-learn.",
            ),
            (
                "DevOps Engineer",
                "Operations",
                "CloudFirst Systems",
                "Germany",
                100000,
                "Manage cloud infrastructure on AWS/Azure, implement CI/CD pipelines, and ensure system reliability.",
            ),
            (
                "Mobile App Developer",
                "Mobile Development",
                "AppMakers Inc.",
                "Australia",
                90000,
                "Develop cross-platform mobile applications using Flutter or React Native for iOS and Android.",
            ),
            (
                "UI/UX Designer",
                "Design",
                "Creative Studio",
                "Netherlands",
                75000,
                "Create stunning user experiences and interfaces for web and mobile applications.",
            ),
            (
                "Backend Java Developer",
                "Software Development",
                "Enterprise Solutions",
                "United States",
                115000,
                "Build scalable backend services using Java, Spring Boot, and microservices architecture.",
            ),
            (
                "Machine Learning Engineer",
                "AI/ML",
                "AI Innovations",
                "Canada",
                130000,
                "Develop and deploy machine learning models for production systems using PyTorch and MLOps tools.",
            ),
            (
                "Full Stack Developer",
                "Software Development",
                "StartupX",
                "Israel",
                85000,
                "Work on both frontend and backend using Node.js, React, and PostgreSQL in a fast-paced startup environment.",
            ),
            (
                "Cloud Architect",
                "Cloud Computing",
                "CloudScale Corp.",
                "United States",
                150000,
                "Design and implement cloud-native solutions on AWS, with focus on security and scalability.",
            ),
            (
                "Cybersecurity Analyst",
                "Security",
                "SecureNet Ltd.",
                "United Kingdom",
                95000,
                "Monitor and protect company systems from cyber threats, conduct security audits and penetration testing.",
            ),
            (
                "Product Manager",
                "Product",
                "ProductHub",
                "Germany",
                100000,
                "Lead product development from ideation to launch, work with cross-functional teams.",
            ),
            (
                "iOS Developer",
                "Mobile Development",
                "AppleTech Solutions",
                "United States",
                125000,
                "Build native iOS applications using Swift and SwiftUI for iPhone and iPad.",
            ),
            (
                "Android Developer",
                "Mobile Development",
                "DroidWorks",
                "India",
                45000,
                "Develop Android applications using Kotlin and Jetpack Compose.",
            ),
            (
                "Database Administrator",
                "Database",
                "DataCore Systems",
                "Canada",
                90000,
                "Manage and optimize PostgreSQL and MongoDB databases for high-performance applications.",
            ),
            (
                "QA Engineer",
                "Quality Assurance",
                "QualityFirst",
                "Poland",
                55000,
                "Design and execute test plans, automate testing using Selenium and pytest.",
            ),
            (
                "Technical Writer",
                "Documentation",
                "DocuTech",
                "Remote",
                65000,
                "Create technical documentation, API guides, and user manuals for software products.",
            ),
            (
                "Blockchain Developer",
                "Blockchain",
                "CryptoTech",
                "Singapore",
                140000,
                "Develop smart contracts and DeFi applications using Solidity and Web3 technologies.",
            ),
            (
                "Game Developer",
                "Game Development",
                "GameStudio Pro",
                "Japan",
                80000,
                "Create engaging games using Unity or Unreal Engine with C# or C++.",
            ),
            (
                "Site Reliability Engineer",
                "Operations",
                "ReliableTech",
                "United States",
                135000,
                "Ensure system reliability, implement monitoring solutions, and manage incident response.",
            ),
            (
                "Embedded Systems Engineer",
                "Embedded",
                "IoT Solutions",
                "Germany",
                95000,
                "Develop firmware for IoT devices using C/C++ and embedded Linux.",
            ),
            (
                "Network Engineer",
                "Networking",
                "NetConnect",
                "Australia",
                85000,
                "Design and maintain network infrastructure, implement security protocols.",
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
