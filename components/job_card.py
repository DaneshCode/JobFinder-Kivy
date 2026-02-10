"""
Job Card Component
Reusable job listing card
"""

from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout

from utils.helpers import format_salary


Builder.load_string(
    """
<JobCard>:
    orientation: "vertical"
    size_hint_y: None
    height: dp(160)
    padding: dp(16)
    spacing: dp(8)
    style: "elevated"
    on_release: root.on_card_click()

    # Header with title and company
    MDBoxLayout:
        size_hint_y: None
        height: dp(50)
        spacing: dp(12)

        MDIcon:
            icon: "briefcase"
            size_hint_x: None
            width: dp(40)
            font_size: dp(32)
            theme_text_color: "Custom"
            text_color: app.theme_cls.primaryColor

        MDBoxLayout:
            orientation: "vertical"

            MDLabel:
                text: root.job_title
                font_style: "Title"
                role: "medium"
                shorten: True
                shorten_from: "right"
                text_size: self.width, None

            MDLabel:
                text: root.company
                font_style: "Body"
                role: "medium"
                theme_text_color: "Secondary"
                shorten: True
                shorten_from: "right"

    MDDivider:

    # Details row
    MDBoxLayout:
        size_hint_y: None
        height: dp(30)
        spacing: dp(20)

        # Country
        MDBoxLayout:
            size_hint_x: None
            width: self.minimum_width
            spacing: dp(5)

            MDIcon:
                icon: "earth"
                size_hint_x: None
                width: dp(20)
                font_size: dp(18)
                theme_text_color: "Custom"
                text_color: app.theme_cls.primaryColor

            MDLabel:
                text: root.country
                adaptive_width: True
                shorten: True
                font_style: "Label"
                role: "large"

        # Category
        MDBoxLayout:
            size_hint_x: None
            width: self.minimum_width
            spacing: dp(5)

            MDIcon:
                icon: "tag"
                size_hint_x: None
                width: dp(20)
                font_size: dp(18)
                theme_text_color: "Custom"
                text_color: app.theme_cls.primaryColor

            MDLabel:
                text: root.category
                adaptive_width: True
                shorten: True
                font_style: "Label"
                role: "large"

        Widget:

    # Salary row
    MDBoxLayout:
        size_hint_y: None
        height: dp(30)
        spacing: dp(5)

        MDIcon:
            icon: "currency-usd"
            size_hint_x: None
            width: dp(20)
            font_size: dp(18)
            theme_text_color: "Custom"
            text_color: app.theme_cls.primaryColor

        MDLabel:
            text: root.salary_text
            font_style: "Title"
            role: "small"
            theme_text_color: "Primary"
"""
)


class JobCard(MDCard):
    """Reusable job card component"""

    job_title = StringProperty("")
    company = StringProperty("")
    country = StringProperty("")
    category = StringProperty("")
    salary_text = StringProperty("")
    job_id = NumericProperty(0)
    job_data = ObjectProperty(None, allownone=True)
    callback = ObjectProperty(None, allownone=True)

    def on_card_click(self):
        """Handle card click"""
        if self.callback and self.job_data:
            self.callback(self.job_data)


def create_job_card(job, callback=None):
    """Factory function to create a job card from a Job object"""
    return JobCard(
        job_title=job.title,
        company=job.company,
        country=job.country,
        category=job.category,
        salary_text=format_salary(job.salary),
        job_id=job.id,
        job_data=job,
        callback=callback,
    )
