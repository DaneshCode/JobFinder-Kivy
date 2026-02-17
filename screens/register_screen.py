"""
Register Screen - Create a new user account
"""

from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen


# Load register screen UI with KV language
Builder.load_string(
    """
<RegisterScreen>:
    name: "register"

    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.backgroundColor
        padding: dp(20)
        spacing: dp(10)

        # Top bar with back button and title
        MDBoxLayout:
            size_hint_y: None
            height: dp(56)
            spacing: dp(10)

            MDIconButton:
                icon: "arrow-left"
                on_release: app.switch_screen("welcome")

            MDLabel:
                text: "Create Account"
                font_style: "Headline"
                role: "small"
                valign: "center"

        # Scrollable content
        MDScrollView:
            do_scroll_x: False

            MDBoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: dp(0), dp(20)
                spacing: dp(20)

                # Registration card with user information form
                MDCard:
                    id: register_card
                    orientation: "vertical"
                    size_hint: 1, None
                    height: dp(600)
                    padding: dp(24)
                    spacing: dp(16)
                    style: "elevated"
                    opacity: 0

                    # Registration icon
                    MDIcon:
                        icon: "account-plus"
                        halign: "center"
                        font_size: dp(48)
                        theme_text_color: "Custom"
                        text_color: app.theme_cls.primaryColor

                    # Registration page title
                    MDLabel:
                        text: "Join Job Finder"
                        halign: "center"
                        font_style: "Headline"
                        role: "small"

                    # Full name field
                    MDTextField:
                        id: name_field
                        mode: "outlined"
                        size_hint_x: 1

                        MDTextFieldLeadingIcon:
                            icon: "account"

                        MDTextFieldHintText:
                            text: "Full Name"

                    # Email field
                    MDTextField:
                        id: email_field
                        mode: "outlined"
                        size_hint_x: 1

                        MDTextFieldLeadingIcon:
                            icon: "email"

                        MDTextFieldHintText:
                            text: "Email"

                    # Password field
                    MDTextField:
                        id: password_field
                        mode: "outlined"
                        size_hint_x: 1
                        password: True

                        MDTextFieldLeadingIcon:
                            icon: "lock"

                        MDTextFieldHintText:
                            text: "Password"

                    # Confirm password field
                    MDTextField:
                        id: confirm_password_field
                        mode: "outlined"
                        size_hint_x: 1
                        password: True

                        MDTextFieldLeadingIcon:
                            icon: "lock-check"

                        MDTextFieldHintText:
                            text: "Confirm Password"

                    # Job specialty field
                    MDTextField:
                        id: specialty_field
                        mode: "outlined"
                        size_hint_x: 1

                        MDTextFieldLeadingIcon:
                            icon: "briefcase"

                        MDTextFieldHintText:
                            text: "Job Specialty (e.g., Python Developer)"

                    # Create account button
                    MDButton:
                        style: "filled"
                        size_hint_x: 1
                        height: dp(50)
                        on_release: root.do_register()

                        MDButtonText:
                            text: "Create Account"
                            font_style: "Title"

                # Error or success message
                MDLabel:
                    id: message_label
                    text: ""
                    halign: "center"
                    size_hint_y: None
                    height: dp(40)

                # Login link for users who already have an account
                MDBoxLayout:
                    size_hint_y: None
                    height: dp(50)
                    spacing: dp(5)

                    Widget:

                    MDLabel:
                        text: "Already have an account?"
                        adaptive_width: True
                        theme_text_color: "Secondary"

                    MDButton:
                        style: "text"
                        on_release: app.switch_screen("login")

                        MDButtonText:
                            text: "Login"

                    Widget:

                # Bottom spacing
                Widget:
                    size_hint_y: None
                    height: dp(20)
"""
)


# Registration screen class for creating new user accounts
class RegisterScreen(MDScreen):
    """Registration screen for new users"""

    # Run card animation when the screen is displayed
    def on_enter(self):
        """Animate card when the screen is displayed"""
        self.ids.message_label.text = ""
        self.ids.message_label.theme_text_color = "Primary"
        Clock.schedule_once(self._animate_card, 0.1)

    # Registration card entry animation
    def _animate_card(self, dt):
        """Registration card entry animation"""
        card = self.ids.register_card
        Animation(opacity=1, duration=0.4).start(card)

    # Show message to user (error or success)
    def show_message(self, text, is_error=True):
        """Show message to user"""
        label = self.ids.message_label
        label.text = text
        label.theme_text_color = "Custom"
        label.text_color = "red" if is_error else "green"

    # Perform registration and save user data to database
    def do_register(self):
        """Perform registration"""
        from kivymd.app import MDApp
        from database import DatabaseManager
        from utils.helpers import (
            generate_user_code,
            hash_password,
            validate_email,
            validate_password,
        )

        app = MDApp.get_running_app()
        db = DatabaseManager()

        name = self.ids.name_field.text.strip()
        email = self.ids.email_field.text.strip()
        password = self.ids.password_field.text
        confirm_password = self.ids.confirm_password_field.text
        specialty = self.ids.specialty_field.text.strip()

        # Validate inputs - check all fields are filled
        if not all([name, email, password, confirm_password, specialty]):
            self.show_message("Please fill in all fields")
            return

        # Validate email format
        if not validate_email(email):
            self.show_message("Please enter a valid email")
            return

        # Check password strength
        is_valid, msg = validate_password(password)
        if not is_valid:
            self.show_message(msg)
            return

        # Check password and confirmation match
        if password != confirm_password:
            self.show_message("Passwords do not match")
            return

        # Check email is not already registered
        if db.get_user_by_email(email):
            self.show_message("Email already registered")
            return

        # Generate user code and create account
        user_code = generate_user_code()
        password_hash = hash_password(password)

        user_id = db.create_user(
            name=name,
            email=email,
            password_hash=password_hash,
            specialty=specialty,
            user_code=user_code,
        )

        if user_id:
            self.show_message(
                f"Account created! Your code: {user_code}", is_error=False
            )
            # Clear fields
            self.ids.name_field.text = ""
            self.ids.email_field.text = ""
            self.ids.password_field.text = ""
            self.ids.confirm_password_field.text = ""
            self.ids.specialty_field.text = ""

            # Navigate to login screen after 2 seconds
            Clock.schedule_once(lambda dt: app.switch_screen("login"), 2)
        else:
            self.show_message("Registration failed. Please try again.")
