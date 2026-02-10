# Job Finder Application

A modern, professional job-finding application built with Python and KivyMD.

![Platform](https://img.shields.io/badge/Platform-Android%20%7C%20Windows-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![KivyMD](https://img.shields.io/badge/KivyMD-1.2.0-orange)

## Features

- 🎨 **Modern Dark Theme** - Professional UI with Teal color palette
- 👤 **User Authentication** - Register and login with secure password hashing
- 🔍 **Job Search** - Search through 20+ job listings by keyword
- 📋 **Job Details** - View complete job information with salary and description
- 👨‍💼 **User Profile** - Manage your profile and upload resume
- 📢 **Advertisement System** - Weighted rotating ads at the bottom of screens
- 🌍 **Multiple Countries** - Jobs from USA, Canada, UK, Germany, and more

## Project Structure

```
JobFinder-Kivy/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── buildozer.spec            # Android build configuration
├── jobfinder.spec            # Windows build configuration
├── README.md                 # This file
│
├── database/                 # Database layer
│   ├── __init__.py
│   ├── db_manager.py         # SQLite database operations
│   └── models.py             # Data models (User, Job, Advertisement)
│
├── screens/                  # Application screens
│   ├── __init__.py
│   ├── welcome_screen.py     # Welcome/landing screen
│   ├── login_screen.py       # User login
│   ├── register_screen.py    # User registration
│   ├── main_screen.py        # Main app with navigation
│   └── job_detail_screen.py  # Job details view
│
├── components/               # Reusable UI components
│   ├── __init__.py
│   ├── ad_banner.py          # Advertisement banner
│   └── job_card.py           # Job listing card
│
├── utils/                    # Utility functions
│   ├── __init__.py
│   └── helpers.py            # Helper functions
│
└── data/                     # Database storage (auto-created)
    └── jobfinder.db          # SQLite database
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Setup

1. **Clone or download the project**

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

## Building for Distribution

### Building Windows Executable (EXE)

1. **Install PyInstaller and Kivy dependencies**:

   ```bash
   pip install pyinstaller
   pip install kivy[base] kivymd
   pip install pyinstaller-hooks-contrib
   ```

2. **Install Kivy dependencies for Windows**:

   ```bash
   pip install kivy_deps.sdl2 kivy_deps.glew
   ```

3. **Build the executable**:

   ```bash
   pyinstaller jobfinder.spec
   ```

4. **Find the executable** in `dist/JobFinder/JobFinder.exe`

#### Alternative: One-file executable

```bash
pyinstaller --onefile --windowed --name JobFinder main.py
```

### Building Android APK

#### Prerequisites

- Linux or WSL (Windows Subsystem for Linux)
- Java JDK 11
- Android SDK and NDK (auto-downloaded by buildozer)

#### Build Steps

1. **Install Buildozer**:

   ```bash
   pip install buildozer
   ```

2. **Install system dependencies** (Ubuntu/Debian):

   ```bash
   sudo apt-get update
   sudo apt-get install -y \
       python3-pip \
       build-essential \
       git \
       python3 \
       python3-dev \
       ffmpeg \
       libsdl2-dev \
       libsdl2-image-dev \
       libsdl2-mixer-dev \
       libsdl2-ttf-dev \
       libportmidi-dev \
       libswscale-dev \
       libavformat-dev \
       libavcodec-dev \
       zlib1g-dev \
       libgstreamer1.0 \
       gstreamer1.0-plugins-base \
       gstreamer1.0-plugins-good \
       libgstreamer-plugins-base1.0-dev \
       openjdk-11-jdk \
       unzip \
       zip \
       autoconf \
       automake \
       libtool \
       pkg-config \
       cmake
   ```

3. **Build the APK**:

   ```bash
   # Debug build
   buildozer android debug

   # Release build (requires signing key)
   buildozer android release
   ```

4. **Find the APK** in `bin/jobfinder-1.0.0-arm64-v8a-debug.apk`

5. **Deploy to connected device**:
   ```bash
   buildozer android deploy run
   ```

#### Using WSL on Windows

If using Windows, you can use WSL:

1. Install WSL2 with Ubuntu
2. Follow the Linux build steps above
3. Copy the APK from WSL to Windows:
   ```bash
   cp bin/*.apk /mnt/c/Users/YourUsername/Desktop/
   ```

## Usage

### Registration

1. Open the app and tap "Create Account"
2. Fill in your name, email, password, and job specialty
3. You'll receive a unique user code (e.g., JF-ABC12345)
4. Tap "Login" to sign in

### Finding Jobs

1. After login, use the Search tab to browse jobs
2. Use the search bar to filter by title, company, or country
3. Tap a job card to see full details
4. Tap "Apply Now" to submit your application

### Profile Management

1. Go to the Profile tab to view your information
2. Upload your resume (PDF) for job applications
3. Your unique user code is displayed for reference

### Advertisements

- Ads rotate every 10 seconds at the bottom of screens
- Higher-paying ads appear more frequently
- Tap an ad to see more details

## Technical Details

### Database

- SQLite database with 3 tables: users, jobs, advertisements
- Pre-seeded with 22 sample jobs and 8 advertisements
- Weighted random selection for ad display

### Security

- Passwords hashed using SHA-256
- Email validation
- Password strength requirements (minimum 6 characters)

### Theme

- Dark theme with Teal primary color
- Material Design 3 components
- Smooth animations and transitions

## Troubleshooting

### App won't start

- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.9+)

### Database errors

- Delete `data/jobfinder.db` and restart the app to recreate

### Build errors (Windows)

- Ensure Visual C++ Build Tools are installed
- Try: `pip install --upgrade kivy kivymd`

### Build errors (Android)

- Ensure you're using Linux or WSL
- Check Java version: `java -version` (should be 11)
- Clear buildozer cache: `buildozer android clean`

## License

This project is open source and available under the MIT License.

## Credits

Built with:

- [Kivy](https://kivy.org/) - Cross-platform Python framework
- [KivyMD](https://kivymd.readthedocs.io/) - Material Design components
- [Buildozer](https://buildozer.readthedocs.io/) - Android packaging tool
- [PyInstaller](https://pyinstaller.org/) - Windows packaging tool
