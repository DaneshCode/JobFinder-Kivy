"""
برنامه جاب فایندر
یک اپلیکیشن مدرن و حرفه‌ای برای جستجوی شغل ساخته شده با KivyMD

نویسنده: تیم جاب فایندر
نسخه: 1.0.0
"""

import os
import sys

# تنظیم متغیرهای محیطی قبل از ایمپورت کیوی
os.environ["KIVY_LOG_LEVEL"] = "info"

from kivy.core.window import Window
from kivy.animation import Animation
from kivy.lang import Builder
from kivymd.app import MDApp


# تنظیم اندازه پنجره برای دسکتاپ (در موبایل نادیده گرفته می‌شود)
if sys.platform in ("win32", "linux", "darwin"):
    Window.size = (400, 750)
    Window.minimum_width = 350
    Window.minimum_height = 600


# کلاس اصلی اپلیکیشن جاب فایندر
class JobFinderApp(MDApp):
    """کلاس اصلی برنامه جاب فایندر"""

    # کاربر فعلی که وارد شده
    current_user = None
    # شغل انتخاب شده برای نمایش جزئیات
    selected_job = None

    # ساخت رابط کاربری اپلیکیشن
    def build(self):
        """ساخت اپلیکیشن"""
        # تنظیم تم برنامه
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"

        # ایمپورت و ثبت صفحات مختلف برنامه
        from screens.welcome_screen import WelcomeScreen
        from screens.login_screen import LoginScreen
        from screens.register_screen import RegisterScreen
        from screens.main_screen import MainScreen
        from screens.job_detail_screen import JobDetailScreen

        # ساخت لایه اصلی برنامه با مدیر صفحات
        root = Builder.load_string(
            """
MDScreenManager:
    id: screen_manager

    WelcomeScreen:

    LoginScreen:

    RegisterScreen:

    MainScreen:

    JobDetailScreen:
"""
        )

        return root

    # اجرا شدن بعد از شروع برنامه
    def on_start(self):
        """فراخوانی هنگام شروع برنامه"""
        # راه‌اندازی دیتابیس
        from database import DatabaseManager

        db = DatabaseManager()

    # تغییر صفحه با انیمیشن
    def switch_screen(self, screen_name, direction="left"):
        """تغییر صفحه فعلی با انیمیشن"""
        screen_manager = self.root

        # تعیین جهت انیمیشن بر اساس مسیر ناوبری
        if screen_name in ("welcome", "login"):
            if screen_manager.current in ("main", "job_detail", "register"):
                direction = "right"
        elif screen_name == "main":
            if screen_manager.current == "job_detail":
                direction = "right"

        screen_manager.transition.direction = direction
        screen_manager.current = screen_name

    # پاکسازی منابع هنگام بسته شدن برنامه
    def on_stop(self):
        """فراخوانی هنگام بسته شدن برنامه"""
        from database import DatabaseManager

        db = DatabaseManager()
        db.close()


# نقطه ورود اصلی برنامه
def main():
    """نقطه ورود اصلی برنامه"""
    JobFinderApp().run()


if __name__ == "__main__":
    main()
