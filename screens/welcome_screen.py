"""
صفحه خوش‌آمدگویی - اولین صفحه‌ای که هنگام اجرای برنامه نمایش داده می‌شود
"""

from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen


# بارگذاری رابط کاربری صفحه خوش‌آمدگویی با زبان KV
Builder.load_string(
    """
<WelcomeScreen>:
    name: "welcome"

    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.backgroundColor

        # فضای خالی بالا
        Widget:
            size_hint_y: 0.15

        # ناحیه لوگو و عنوان برنامه
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

        # فضای خالی میانی
        Widget:
            size_hint_y: 0.1

        # ناحیه دکمه‌های ورود و ثبت‌نام
        MDBoxLayout:
            id: buttons_box
            orientation: "vertical"
            size_hint_y: 0.3
            padding: dp(40), dp(20)
            spacing: dp(15)
            opacity: 0

            # دکمه ورود به حساب کاربری
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

            # دکمه ساخت حساب کاربری جدید
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

        # فوتر برنامه - نمایش کپی‌رایت
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


# کلاس صفحه خوش‌آمدگویی با انیمیشن‌های ورودی
class WelcomeScreen(MDScreen):
    """صفحه خوش‌آمدگویی با معرفی برنامه"""

    # اجرای انیمیشن‌ها هنگام ورود به صفحه
    def on_enter(self):
        """اجرای انیمیشن‌ها هنگام نمایش صفحه"""
        Clock.schedule_once(self._start_animations, 0.2)

    # شروع انیمیشن‌های ورودی عناصر صفحه
    def _start_animations(self, dt):
        """شروع انیمیشن‌های ورودی"""
        # انیمیشن لوگو
        logo = self.ids.logo_icon
        anim_logo = Animation(opacity=1, duration=0.5)
        anim_logo.start(logo)

        # انیمیشن عنوان با تاخیر
        title = self.ids.title_label
        Clock.schedule_once(
            lambda dt: Animation(opacity=1, duration=0.5).start(title), 0.2
        )

        # انیمیشن زیرعنوان با تاخیر بیشتر
        subtitle = self.ids.subtitle_label
        Clock.schedule_once(
            lambda dt: Animation(opacity=1, duration=0.5).start(subtitle), 0.4
        )

        # انیمیشن دکمه‌ها با تاخیر بیشتر
        buttons = self.ids.buttons_box
        Clock.schedule_once(
            lambda dt: Animation(opacity=1, duration=0.5).start(buttons), 0.6
        )
