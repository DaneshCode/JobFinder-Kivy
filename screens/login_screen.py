"""
Login Screen - User authentication
"""

from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen


# Load login screen UI with KV language
Builder.load_string(
    """
<LoginScreen>:
    name: "login"

    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.backgroundColor
        padding: dp(20)
        spacing: dp(20)

        # Top bar with back button and title
        MDBoxLayout:
            size_hint_y: None
            height: dp(56)
            spacing: dp(10)

            MDIconButton:
                icon: "arrow-left"
                on_release: app.switch_screen("welcome")

            MDLabel:
                text: "Login"
                font_style: "Headline"
                role: "small"
                valign: "center"

        # Top spacing
        Widget:
            size_hint_y: 0.05

        # Login card with email and password form
        MDCard:
            id: login_card
            orientation: "vertical"
            size_hint: 1, None
            height: dp(380)
            padding: dp(24)
            spacing: dp(20)
            style: "elevated"
            opacity: 0

            # User icon
            MDIcon:
                icon: "account-circle"
                halign: "center"
                font_size: dp(64)
                theme_text_color: "Custom"
                text_color: app.theme_cls.primaryColor

            # Welcome title
            MDLabel:
                text: "Welcome Back!"
                halign: "center"
                font_style: "Headline"
                role: "small"

            # Email field
            MDTextField:
                id: email_field
                mode: "outlined"
                size_hint_x: 1

                MDTextFieldLeadingIcon:
                    icon: "email"

                MDTextFieldHintText:
                    text: "Email"

            # Password field row with show/hide button
            MDBoxLayout:
                size_hint_y: None
                height: dp(56)
                spacing: dp(8)

                # Password field
                MDTextField:
                    id: password_field
                    mode: "outlined"
                    size_hint_x: 0.85
                    password: True

                    MDTextFieldLeadingIcon:
                        icon: "lock"

                    MDTextFieldHintText:
                        text: "Password"

                # Password visibility toggle button
                MDIconButton:
                    id: password_visibility_btn
                    icon: "eye-off"
                    pos_hint: {"center_y": 0.5}
                    on_release: root.toggle_password_visibility()

            # Login button
            MDButton:
                style: "filled"
                size_hint_x: 1
                height: dp(50)
                on_release: root.do_login()

                MDButtonText:
                    text: "Login"
                    font_style: "Title"

        # Error message
        MDLabel:
            id: error_label
            text: ""
            halign: "center"
            theme_text_color: "Custom"
            text_color: "red"
            size_hint_y: None
            height: dp(40)

        # Spacing
        Widget:

        # Registration link for new users
        MDBoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(5)

            Widget:

            MDLabel:
                text: "Don't have an account?"
                adaptive_width: True
                theme_text_color: "Secondary"

            MDButton:
                style: "text"
                on_release: app.switch_screen("register")

                MDButtonText:
                    text: "Register"

            Widget:
"""
)


# Login screen class for user authentication
class LoginScreen(MDScreen):
    """Login screen for user authentication"""

    # Run card animation when the screen is displayed
    def on_enter(self):
        """Animate card when the screen is displayed"""
        self.ids.error_label.text = ""
        Clock.schedule_once(self._animate_card, 0.1)

    # Login card entry animation
    def _animate_card(self, dt):
        """Login card entry animation"""
        card = self.ids.login_card
        Animation(opacity=1, duration=0.4).start(card)

    # Toggle password visibility (hidden/visible)
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        pwd_field = self.ids.password_field
        btn = self.ids.password_visibility_btn

        pwd_field.password = not pwd_field.password
        btn.icon = "eye" if not pwd_field.password else "eye-off"

    # Perform login operation and validate user credentials
    def do_login(self):
        """Perform login operation"""
        from kivymd.app import MDApp
        from database import DatabaseManager
        from utils.helpers import verify_password

        app = MDApp.get_running_app()
        db = DatabaseManager()

        email = self.ids.email_field.text.strip()
        password = self.ids.password_field.text

        # Validate inputs
        if not email or not password:
            self.ids.error_label.text = "Please fill in all fields"
            return

        # Search for user in database
        user = db.get_user_by_email(email)

        if not user:
            self.ids.error_label.text = "User not found"
            return

        # Verify password
        if not verify_password(password, user.password_hash):
            self.ids.error_label.text = "Invalid password"
            return

        # Successful login - save user and navigate to main screen
        app.current_user = user
        app.switch_screen("main")

        # Clear fields
        self.ids.email_field.text = ""
        self.ids.password_field.text = ""
        self.ids.error_label.text = ""
