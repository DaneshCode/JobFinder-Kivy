"""
Welcome Screen - First screen shown on app launch
"""

from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen


Builder.load_string(
    """
<WelcomeScreen>:
    name: "welcome"

    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.backgroundColor

        # Spacer
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

        # Spacer
        Widget:
            size_hint_y: 0.1

        # Buttons area
        MDBoxLayout:
            id: buttons_box
            orientation: "vertical"
            size_hint_y: 0.3
            padding: dp(40), dp(20)
            spacing: dp(15)
            opacity: 0

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

        # Footer
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


class WelcomeScreen(MDScreen):
    """Welcome/Home screen with app introduction"""

    def on_enter(self):
        """Animate elements when screen is shown"""
        Clock.schedule_once(self._start_animations, 0.2)

    def _start_animations(self, dt):
        """Start entrance animations"""
        # Animate logo
        logo = self.ids.logo_icon
        anim_logo = Animation(opacity=1, duration=0.5)
        anim_logo.start(logo)

        # Animate title with delay
        title = self.ids.title_label
        Clock.schedule_once(
            lambda dt: Animation(opacity=1, duration=0.5).start(title), 0.2
        )

        # Animate subtitle with delay
        subtitle = self.ids.subtitle_label
        Clock.schedule_once(
            lambda dt: Animation(opacity=1, duration=0.5).start(subtitle), 0.4
        )

        # Animate buttons with delay
        buttons = self.ids.buttons_box
        Clock.schedule_once(
            lambda dt: Animation(opacity=1, duration=0.5).start(buttons), 0.6
        )
