"""
Welcome Screen - The first screen displayed when the app launches
"""

from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen


# Load welcome screen UI with KV language
Builder.load_string(
    """
<WelcomeScreen>:
    name: "welcome"

    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.backgroundColor

        # Top spacing
        Widget:
            size_hint_y: 0.15

        # Logo and title area
        MDBoxLayout:
            orientation: "vertical"
            size_hint_y: 0.35
            padding: dp(20)
            spacing: dp(10)

            MDIcon:
                id: logo_icon
                icon: "briefcase-search"
                halign: "center"
                font_size: dp(100)
                theme_text_color: "Custom"
                text_color: app.theme_cls.primaryColor
                opacity: 0

            MDLabel:
                id: title_label
                text: "Job Finder"
                halign: "center"
                font_style: "Display"
                role: "medium"
                theme_text_color: "Primary"
                opacity: 0

            MDLabel:
                id: subtitle_label
                text: "Find your dream job today"
                halign: "center"
                font_style: "Title"
                role: "large"
                theme_text_color: "Secondary"
                opacity: 0

        # Middle spacing
        Widget:
            size_hint_y: 0.1

        # Login and register buttons area
        MDBoxLayout:
            id: buttons_box
            orientation: "vertical"
            size_hint_y: 0.3
            padding: dp(40), dp(20)
            spacing: dp(15)
            opacity: 0

            # Login button
            MDButton:
                style: "filled"
                size_hint_x: 1
                height: dp(56)
                on_release: app.switch_screen("login")

                MDButtonIcon:
                    icon: "login"

                MDButtonText:
                    text: "Login"
                    font_style: "Title"

            # Create new account button
            MDButton:
                style: "outlined"
                size_hint_x: 1
                height: dp(56)
                on_release: app.switch_screen("register")

                MDButtonIcon:
                    icon: "account-plus"

                MDButtonText:
                    text: "Create Account"
                    font_style: "Title"

        # App footer - copyright notice
        MDBoxLayout:
            size_hint_y: 0.1
            padding: dp(20)

            MDLabel:
                text: "© 2026 Job Finder App"
                halign: "center"
                font_style: "Label"
                role: "small"
                theme_text_color: "Hint"
"""
)


# Welcome screen class with entry animations
class WelcomeScreen(MDScreen):
    """Welcome screen with app introduction"""

    # Run animations when entering the screen
    def on_enter(self):
        """Run animations when the screen is displayed"""
        Clock.schedule_once(self._start_animations, 0.2)

    # Start entry animations for screen elements
    def _start_animations(self, dt):
        """Start entry animations"""
        # Logo animation
        logo = self.ids.logo_icon
        anim_logo = Animation(opacity=1, duration=0.5)
        anim_logo.start(logo)

        # Title animation with delay
        title = self.ids.title_label
        Clock.schedule_once(
            lambda dt: Animation(opacity=1, duration=0.5).start(title), 0.2
        )

        # Subtitle animation with more delay
        subtitle = self.ids.subtitle_label
        Clock.schedule_once(
            lambda dt: Animation(opacity=1, duration=0.5).start(subtitle), 0.4
        )

        # Buttons animation with more delay
        buttons = self.ids.buttons_box
        Clock.schedule_once(
            lambda dt: Animation(opacity=1, duration=0.5).start(buttons), 0.6
        )
