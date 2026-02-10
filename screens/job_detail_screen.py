"""
صفحه جزئیات شغل - نمایش اطلاعات کامل آگهی شغلی
"""

from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen


# بارگذاری رابط کاربری صفحه جزئیات شغل با زبان KV
Builder.load_string(
    """
<JobDetailScreen>:
    name: "job_detail"

    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.backgroundColor

        # نوار بالای صفحه شامل دکمه برگشت و عنوان
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

        # محتوای قابل اسکرول
        MDScrollView:
            do_scroll_x: False

            MDBoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: dp(16)
                spacing: dp(16)

                # کارت سربرگ شغل شامل عنوان، شرکت، کشور و دسته‌بندی
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

                    # ردیف کشور و دسته‌بندی
                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(30)
                        spacing: dp(20)

                        Widget:

                        # کشور
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

                        # دسته‌بندی
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

                # کارت حقوق و دستمزد
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

                # کارت توضیحات شغل
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

                # دکمه ارسال درخواست شغلی
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

                # فضای خالی پایین
                Widget:
                    size_hint_y: None
                    height: dp(20)
"""
)


# کلاس صفحه جزئیات شغل - نمایش اطلاعات کامل آگهی
class JobDetailScreen(MDScreen):
    """صفحه نمایش اطلاعات کامل آگهی شغلی"""

    # پر کردن اطلاعات شغل هنگام ورود به صفحه
    def on_enter(self):
        """پر کردن جزئیات شغل هنگام ورود به صفحه"""
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

        # اجرای انیمیشن کارت‌ها
        Clock.schedule_once(self._animate_cards, 0.1)

    # انیمیشن ورودی کارت‌ها به ترتیب
    def _animate_cards(self, dt):
        """انیمیشن ورودی کارت‌ها"""
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

    # مدیریت ارسال درخواست شغلی و نمایش دیالوگ تایید
    def apply_for_job(self):
        """مدیریت ارسال درخواست شغلی"""
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

        # ساخت پیام تایید ارسال درخواست
        message = (
            f"Your application for '{job.title}' at {job.company} has been submitted!"
        )

        # بررسی وجود رزومه کاربر و نمایش پیام مناسب
        if app.current_user and app.current_user.resume_path:
            message += "\n\nYour resume has been attached to the application."
        else:
            message += (
                "\n\nTip: Upload a resume in your profile to improve your chances!"
            )

        # ساخت و نمایش دیالوگ تایید ارسال درخواست
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
