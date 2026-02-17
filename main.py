"""
Job Finder Application
A modern, professional job search application built with KivyMD

Author: Job Finder Team
Version: 1.0.0
"""

import os
import sys

# Set environment variables before importing Kivy
os.environ["KIVY_LOG_LEVEL"] = "info"

from kivy.core.window import Window
from kivy.animation import Animation
from kivy.lang import Builder
from kivymd.app import MDApp


# Set window size for desktop (ignored on mobile)
if sys.platform in ("win32", "linux", "darwin"):
    Window.size = (400, 750)
    Window.minimum_width = 350
    Window.minimum_height = 600


# Main Job Finder application class
class JobFinderApp(MDApp):
    """Main Job Finder application class"""

    # Currently logged-in user
    current_user = None
    # Selected job for detail view
    selected_job = None

    # Build the application UI
    def build(self):
        """Build the application"""
        # Set application theme
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"

        # Import and register application screens
        from screens.welcome_screen import WelcomeScreen
        from screens.login_screen import LoginScreen
        from screens.register_screen import RegisterScreen
        from screens.main_screen import MainScreen
        from screens.job_detail_screen import JobDetailScreen

        # Build the main application layout with screen manager
        root = Builder.load_string(
            """
MDScreenManager:
    id: screen_manager

    WelcomeScreen:

    LoginScreen:

    RegisterScreen:

    MainScreen:

    JobDetailScreen:
"""
        )

        return root

    # Called after application start
    def on_start(self):
        """Called when the application starts"""
        # Initialize database
        from database import DatabaseManager

        db = DatabaseManager()

    # Switch screen with animation
    def switch_screen(self, screen_name, direction="left"):
        """Switch current screen with animation"""
        screen_manager = self.root

        # Determine animation direction based on navigation path
        if screen_name in ("welcome", "login"):
            if screen_manager.current in ("main", "job_detail", "register"):
                direction = "right"
        elif screen_name == "main":
            if screen_manager.current == "job_detail":
                direction = "right"

        screen_manager.transition.direction = direction
        screen_manager.current = screen_name

    # Clean up resources when the application closes
    def on_stop(self):
        """Called when the application closes"""
        from database import DatabaseManager

        db = DatabaseManager()
        db.close()


# Main entry point
def main():
    """Main entry point"""
    JobFinderApp().run()


if __name__ == "__main__":
    main()
