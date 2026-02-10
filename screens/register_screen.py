"""
صفحه ثبت‌نام - ایجاد حساب کاربری جدید
"""

from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen


# بارگذاری رابط کاربری صفحه ثبت‌نام با زبان KV
Builder.load_string(
    """
<RegisterScreen>:
    name: "register"

    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.backgroundColor
        padding: dp(20)
        spacing: dp(10)

        # نوار بالای صفحه شامل دکمه برگشت و عنوان
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

        # محتوای قابل اسکرول
        MDScrollView:
            do_scroll_x: False

            MDBoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: dp(0), dp(20)
                spacing: dp(20)

                # کارت ثبت‌نام شامل فرم اطلاعات کاربر
                MDCard:
                    id: register_card
                    orientation: "vertical"
                    size_hint: 1, None
                    height: dp(600)
                    padding: dp(24)
                    spacing: dp(16)
                    style: "elevated"
                    opacity: 0

                    # آیکون ثبت‌نام
                    MDIcon:
                        icon: "account-plus"
                        halign: "center"
                        font_size: dp(48)
                        theme_text_color: "Custom"
                        text_color: app.theme_cls.primaryColor

                    # عنوان صفحه ثبت‌نام
                    MDLabel:
                        text: "Join Job Finder"
                        halign: "center"
                        font_style: "Headline"
                        role: "small"

                    # فیلد نام کامل
                    MDTextField:
                        id: name_field
                        mode: "outlined"
                        size_hint_x: 1

                        MDTextFieldLeadingIcon:
                            icon: "account"

                        MDTextFieldHintText:
                            text: "Full Name"

                    # فیلد ایمیل
                    MDTextField:
                        id: email_field
                        mode: "outlined"
                        size_hint_x: 1

                        MDTextFieldLeadingIcon:
                            icon: "email"

                        MDTextFieldHintText:
                            text: "Email"

                    # فیلد رمز عبور
                    MDTextField:
                        id: password_field
                        mode: "outlined"
                        size_hint_x: 1
                        password: True

                        MDTextFieldLeadingIcon:
                            icon: "lock"

                        MDTextFieldHintText:
                            text: "Password"

                    # فیلد تکرار رمز عبور
                    MDTextField:
                        id: confirm_password_field
                        mode: "outlined"
                        size_hint_x: 1
                        password: True

                        MDTextFieldLeadingIcon:
                            icon: "lock-check"

                        MDTextFieldHintText:
                            text: "Confirm Password"

                    # فیلد تخصص شغلی
                    MDTextField:
                        id: specialty_field
                        mode: "outlined"
                        size_hint_x: 1

                        MDTextFieldLeadingIcon:
                            icon: "briefcase"

                        MDTextFieldHintText:
                            text: "Job Specialty (e.g., Python Developer)"

                    # دکمه ساخت حساب کاربری
                    MDButton:
                        style: "filled"
                        size_hint_x: 1
                        height: dp(50)
                        on_release: root.do_register()

                        MDButtonText:
                            text: "Create Account"
                            font_style: "Title"

                # پیام خطا یا موفقیت
                MDLabel:
                    id: message_label
                    text: ""
                    halign: "center"
                    size_hint_y: None
                    height: dp(40)

                # لینک ورود برای کاربرانی که قبلا حساب دارند
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

                # فضای خالی پایین
                Widget:
                    size_hint_y: None
                    height: dp(20)
"""
)


# کلاس صفحه ثبت‌نام برای ایجاد حساب کاربری جدید
class RegisterScreen(MDScreen):
    """صفحه ثبت‌نام برای کاربران جدید"""

    # اجرای انیمیشن کارت هنگام نمایش صفحه
    def on_enter(self):
        """انیمیشن کارت هنگام نمایش صفحه"""
        self.ids.message_label.text = ""
        self.ids.message_label.theme_text_color = "Primary"
        Clock.schedule_once(self._animate_card, 0.1)

    # انیمیشن ورودی کارت ثبت‌نام
    def _animate_card(self, dt):
        """انیمیشن ورودی کارت ثبت‌نام"""
        card = self.ids.register_card
        Animation(opacity=1, duration=0.4).start(card)

    # نمایش پیام به کاربر (خطا یا موفقیت)
    def show_message(self, text, is_error=True):
        """نمایش پیام به کاربر"""
        label = self.ids.message_label
        label.text = text
        label.theme_text_color = "Custom"
        label.text_color = "red" if is_error else "green"

    # انجام عملیات ثبت‌نام و ذخیره اطلاعات کاربر در دیتابیس
    def do_register(self):
        """انجام عملیات ثبت‌نام"""
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

        # اعتبارسنجی ورودی‌ها - بررسی پر بودن تمام فیلدها
        if not all([name, email, password, confirm_password, specialty]):
            self.show_message("Please fill in all fields")
            return

        # بررسی صحت فرمت ایمیل
        if not validate_email(email):
            self.show_message("Please enter a valid email")
            return

        # بررسی قدرت رمز عبور
        is_valid, msg = validate_password(password)
        if not is_valid:
            self.show_message(msg)
            return

        # بررسی تطابق رمز عبور و تکرار آن
        if password != confirm_password:
            self.show_message("Passwords do not match")
            return

        # بررسی تکراری نبودن ایمیل
        if db.get_user_by_email(email):
            self.show_message("Email already registered")
            return

        # تولید کد کاربری و ساخت حساب کاربری
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
            # پاک کردن فیلدها
            self.ids.name_field.text = ""
            self.ids.email_field.text = ""
            self.ids.password_field.text = ""
            self.ids.confirm_password_field.text = ""
            self.ids.specialty_field.text = ""

            # انتقال به صفحه ورود بعد از ۲ ثانیه
            Clock.schedule_once(lambda dt: app.switch_screen("login"), 2)
        else:
            self.show_message("Registration failed. Please try again.")
