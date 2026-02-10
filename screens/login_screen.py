"""
صفحه ورود - احراز هویت کاربران
"""

from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen


# بارگذاری رابط کاربری صفحه ورود با زبان KV
Builder.load_string(
    """
<LoginScreen>:
    name: "login"

    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.backgroundColor
        padding: dp(20)
        spacing: dp(20)

        # نوار بالای صفحه شامل دکمه برگشت و عنوان
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

        # فضای خالی بالا
        Widget:
            size_hint_y: 0.05

        # کارت ورود شامل فرم ایمیل و رمز عبور
        MDCard:
            id: login_card
            orientation: "vertical"
            size_hint: 1, None
            height: dp(380)
            padding: dp(24)
            spacing: dp(20)
            style: "elevated"
            opacity: 0

            # آیکون کاربر
            MDIcon:
                icon: "account-circle"
                halign: "center"
                font_size: dp(64)
                theme_text_color: "Custom"
                text_color: app.theme_cls.primaryColor

            # عنوان خوش‌آمدگویی
            MDLabel:
                text: "Welcome Back!"
                halign: "center"
                font_style: "Headline"
                role: "small"

            # فیلد ایمیل
            MDTextField:
                id: email_field
                mode: "outlined"
                size_hint_x: 1

                MDTextFieldLeadingIcon:
                    icon: "email"

                MDTextFieldHintText:
                    text: "Email"

            # ردیف فیلد رمز عبور و دکمه نمایش/مخفی کردن
            MDBoxLayout:
                size_hint_y: None
                height: dp(56)
                spacing: dp(8)

                # فیلد رمز عبور
                MDTextField:
                    id: password_field
                    mode: "outlined"
                    size_hint_x: 0.85
                    password: True

                    MDTextFieldLeadingIcon:
                        icon: "lock"

                    MDTextFieldHintText:
                        text: "Password"

                # دکمه نمایش/مخفی کردن رمز عبور
                MDIconButton:
                    id: password_visibility_btn
                    icon: "eye-off"
                    pos_hint: {"center_y": 0.5}
                    on_release: root.toggle_password_visibility()

            # دکمه ورود
            MDButton:
                style: "filled"
                size_hint_x: 1
                height: dp(50)
                on_release: root.do_login()

                MDButtonText:
                    text: "Login"
                    font_style: "Title"

        # پیام خطا
        MDLabel:
            id: error_label
            text: ""
            halign: "center"
            theme_text_color: "Custom"
            text_color: "red"
            size_hint_y: None
            height: dp(40)

        # فضای خالی
        Widget:

        # لینک ثبت‌نام برای کاربران جدید
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


# کلاس صفحه ورود برای احراز هویت کاربران
class LoginScreen(MDScreen):
    """صفحه ورود برای احراز هویت کاربران"""

    # اجرای انیمیشن کارت هنگام نمایش صفحه
    def on_enter(self):
        """انیمیشن کارت هنگام نمایش صفحه"""
        self.ids.error_label.text = ""
        Clock.schedule_once(self._animate_card, 0.1)

    # انیمیشن ورودی کارت لاگین
    def _animate_card(self, dt):
        """انیمیشن ورودی کارت لاگین"""
        card = self.ids.login_card
        Animation(opacity=1, duration=0.4).start(card)

    # تغییر وضعیت نمایش رمز عبور (مخفی/آشکار)
    def toggle_password_visibility(self):
        """تغییر وضعیت نمایش رمز عبور"""
        pwd_field = self.ids.password_field
        btn = self.ids.password_visibility_btn

        pwd_field.password = not pwd_field.password
        btn.icon = "eye" if not pwd_field.password else "eye-off"

    # انجام عملیات ورود و بررسی اطلاعات کاربر
    def do_login(self):
        """انجام عملیات ورود"""
        from kivymd.app import MDApp
        from database import DatabaseManager
        from utils.helpers import verify_password

        app = MDApp.get_running_app()
        db = DatabaseManager()

        email = self.ids.email_field.text.strip()
        password = self.ids.password_field.text

        # اعتبارسنجی ورودی‌ها
        if not email or not password:
            self.ids.error_label.text = "Please fill in all fields"
            return

        # جستجوی کاربر در دیتابیس
        user = db.get_user_by_email(email)

        if not user:
            self.ids.error_label.text = "User not found"
            return

        # بررسی صحت رمز عبور
        if not verify_password(password, user.password_hash):
            self.ids.error_label.text = "Invalid password"
            return

        # ورود موفقیت‌آمیز - ذخیره کاربر و انتقال به صفحه اصلی
        app.current_user = user
        app.switch_screen("main")

        # پاک کردن فیلدها
        self.ids.email_field.text = ""
        self.ids.password_field.text = ""
        self.ids.error_label.text = ""
