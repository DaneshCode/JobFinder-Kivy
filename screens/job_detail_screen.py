"""
Job Detail Screen - Display complete job listing information
"""

from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen


# Load job detail screen UI with KV language
Builder.load_string(
    """
<JobDetailScreen>:
    name: "job_detail"

    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.backgroundColor

        # Top bar with back button and title
        MDBoxLayout:
            size_hint_y: None
            height: dp(56)
            padding: dp(10)
            spacing: dp(10)

            MDIconButton:
                icon: "arrow-left"
                on_release: app.switch_screen("main")

            MDLabel:
                text: "Job Details"
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
                padding: dp(16)
                spacing: dp(16)

                # Job header card with title, company, country and category
                MDCard:
                    id: header_card
                    orientation: "vertical"
                    size_hint_y: None
                    height: dp(200)
                    padding: dp(24)
                    spacing: dp(12)
                    style: "elevated"
                    opacity: 0

                    MDIcon:
                        icon: "briefcase-variant"
                        halign: "center"
                        font_size: dp(48)
                        theme_text_color: "Custom"
                        text_color: app.theme_cls.primaryColor

                    MDLabel:
                        id: job_title
                        text: "Job Title"
                        halign: "center"
                        font_style: "Headline"
                        role: "small"

                    MDLabel:
                        id: job_company
                        text: "Company Name"
                        halign: "center"
                        font_style: "Title"
                        role: "medium"
                        theme_text_color: "Secondary"

                    # Country and category row
                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(30)
                        spacing: dp(20)

                        Widget:

                        # Country
                        MDBoxLayout:
                            size_hint_x: None
                            width: self.minimum_width
                            spacing: dp(5)

                            MDIcon:
                                icon: "earth"
                                size_hint_x: None
                                width: dp(24)
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primaryColor

                            MDLabel:
                                id: job_country
                                text: "Country"
                                adaptive_width: True

                        # Category
                        MDBoxLayout:
                            size_hint_x: None
                            width: self.minimum_width
                            spacing: dp(5)

                            MDIcon:
                                icon: "tag"
                                size_hint_x: None
                                width: dp(24)
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primaryColor

                            MDLabel:
                                id: job_category
                                text: "Category"
                                adaptive_width: True

                        Widget:

                # Salary card
                MDCard:
                    id: salary_card
                    orientation: "vertical"
                    size_hint_y: None
                    height: dp(100)
                    padding: dp(20)
                    style: "elevated"
                    opacity: 0

                    MDBoxLayout:
                        spacing: dp(15)

                        MDIcon:
                            icon: "currency-usd"
                            size_hint_x: None
                            width: dp(40)
                            font_size: dp(36)
                            theme_text_color: "Custom"
                            text_color: app.theme_cls.primaryColor

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                text: "Salary"
                                font_style: "Label"
                                role: "large"
                                theme_text_color: "Secondary"

                            MDLabel:
                                id: job_salary
                                text: "$0/year"
                                font_style: "Headline"
                                role: "small"

                # Job description card
                MDCard:
                    id: desc_card
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    padding: dp(20)
                    style: "elevated"
                    opacity: 0

                    MDLabel:
                        text: "Job Description"
                        font_style: "Title"
                        role: "large"
                        size_hint_y: None
                        height: dp(40)

                    MDDivider:
                        size_hint_y: None
                        height: dp(1)

                    Widget:
                        size_hint_y: None
                        height: dp(10)

                    MDLabel:
                        id: job_description
                        text: "Description"
                        size_hint_y: None
                        height: self.texture_size[1]
                        text_size: self.width, None

                # Apply for job button
                MDButton:
                    id: apply_btn
                    style: "filled"
                    size_hint_x: 1
                    height: dp(56)
                    opacity: 0
                    on_release: root.apply_for_job()

                    MDButtonIcon:
                        icon: "send"

                    MDButtonText:
                        text: "Apply Now"
                        font_style: "Title"

                # Bottom spacing
                Widget:
                    size_hint_y: None
                    height: dp(20)
"""
)


# Job detail screen class - display complete listing information
class JobDetailScreen(MDScreen):
    """Screen for displaying complete job listing information"""

    # Populate job information when entering the screen
    def on_enter(self):
        """Populate job details when entering the screen"""
        from kivymd.app import MDApp
        from utils.helpers import format_salary

        app = MDApp.get_running_app()
        job = app.selected_job

        if job:
            self.ids.job_title.text = job.title
            self.ids.job_company.text = job.company
            self.ids.job_country.text = job.country
            self.ids.job_category.text = job.category
            self.ids.job_salary.text = format_salary(job.salary)
            self.ids.job_description.text = job.description

        # Run card animations
        Clock.schedule_once(self._animate_cards, 0.1)

    # Sequential card entry animations
    def _animate_cards(self, dt):
        """Card entry animations"""
        cards = [
            self.ids.header_card,
            self.ids.salary_card,
            self.ids.desc_card,
            self.ids.apply_btn,
        ]

        for i, card in enumerate(cards):
            Clock.schedule_once(
                lambda dt, c=card: Animation(opacity=1, duration=0.3).start(c), i * 0.1
            )

    # Handle job application submission and show confirmation dialog
    def apply_for_job(self):
        """Handle job application submission"""
        from kivymd.app import MDApp
        from kivymd.uix.dialog import (
            MDDialog,
            MDDialogHeadlineText,
            MDDialogSupportingText,
            MDDialogButtonContainer,
        )
        from kivymd.uix.button import MDButton, MDButtonText

        app = MDApp.get_running_app()
        job = app.selected_job

        # Build submission confirmation message
        message = (
            f"Your application for '{job.title}' at {job.company} has been submitted!"
        )

        # Check for user resume and show appropriate message
        if app.current_user and app.current_user.resume_path:
            message += "\n\nYour resume has been attached to the application."
        else:
            message += (
                "\n\nTip: Upload a resume in your profile to improve your chances!"
            )

        # Build and show submission confirmation dialog
        dialog = MDDialog(
            MDDialogHeadlineText(text="Application Submitted!"),
            MDDialogSupportingText(text=message),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="OK"),
                    style="filled",
                    on_release=lambda x: dialog.dismiss(),
                ),
            ),
        )
        dialog.open()
