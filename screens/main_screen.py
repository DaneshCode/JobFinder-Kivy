"""
Main Screen - Main application area after login with bottom navigation
"""

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationbar import (
    MDNavigationBar,
    MDNavigationItem,
    MDNavigationItemIcon,
    MDNavigationItemLabel,
)


Builder.load_string(
    """
<MainScreen>:
    name: "main"

    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.backgroundColor

        # Content area
        MDScreenManager:
            id: content_manager

            # Home Tab
            MDScreen:
                name: "home_tab"

                MDBoxLayout:
                    orientation: "vertical"
                    padding: dp(16)
                    spacing: dp(16)

                    # Header
                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(60)
                        spacing: dp(10)

                        MDIcon:
                            icon: "briefcase-search"
                            font_size: dp(40)
                            theme_text_color: "Custom"
                            text_color: app.theme_cls.primaryColor
                            size_hint_x: None
                            width: dp(50)

                        MDBoxLayout:
                            orientation: "vertical"

                            MDLabel:
                                text: "Job Finder"
                                font_style: "Headline"
                                role: "small"

                            MDLabel:
                                id: welcome_label
                                text: "Welcome back!"
                                font_style: "Body"
                                role: "medium"
                                theme_text_color: "Secondary"

                        MDIconButton:
                            icon: "logout"
                            on_release: root.do_logout()

                    MDDivider:

                    # Quick stats cards
                    MDBoxLayout:
                        orientation: "horizontal"
                        size_hint_y: None
                        height: dp(100)
                        spacing: dp(16)

                        MDCard:
                            orientation: "vertical"
                            padding: dp(16)
                            style: "elevated"

                            MDIcon:
                                icon: "briefcase"
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primaryColor

                            MDLabel:
                                id: jobs_count_label
                                text: "0 Jobs"
                                halign: "center"
                                font_style: "Title"
                                role: "medium"

                        MDCard:
                            orientation: "vertical"
                            padding: dp(16)
                            style: "elevated"

                            MDIcon:
                                icon: "earth"
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primaryColor

                            MDLabel:
                                id: countries_count_label
                                text: "0 Countries"
                                halign: "center"
                                font_style: "Title"
                                role: "medium"

                    # Featured jobs section
                    MDLabel:
                        text: "Featured Jobs"
                        font_style: "Title"
                        role: "large"
                        size_hint_y: None
                        height: dp(40)

                    # Featured jobs scroll
                    MDScrollView:
                        do_scroll_x: False

                        MDBoxLayout:
                            id: featured_jobs_list
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: dp(12)
                            padding: dp(0), dp(0), dp(0), dp(80)

            # Search Tab
            MDScreen:
                name: "search_tab"

                MDBoxLayout:
                    orientation: "vertical"
                    padding: dp(16)
                    spacing: dp(12)

                    # Search header
                    MDLabel:
                        text: "Job Search"
                        font_style: "Headline"
                        role: "small"
                        size_hint_y: None
                        height: dp(50)

                    # Category filter chips (horizontal scroll)
                    MDScrollView:
                        do_scroll_x: True
                        do_scroll_y: False
                        size_hint_y: None
                        height: dp(50)

                        MDBoxLayout:
                            id: category_chips
                            orientation: "horizontal"
                            size_hint_x: None
                            width: self.minimum_width
                            spacing: dp(8)
                            padding: dp(4)

                    # Search input
                    MDTextField:
                        id: search_field
                        mode: "outlined"
                        size_hint_y: None
                        height: dp(56)
                        on_text: root.on_search_text(self.text)

                        MDTextFieldLeadingIcon:
                            icon: "magnify"

                        MDTextFieldHintText:
                            text: "Search by title, company, country..."

                    # Results count
                    MDLabel:
                        id: results_label
                        text: ""
                        font_style: "Label"
                        role: "large"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(30)

                    # Jobs list
                    MDScrollView:
                        do_scroll_x: False

                        MDBoxLayout:
                            id: jobs_list
                            orientation: "vertical"
                            size_hint_y: None
                            height: self.minimum_height
                            spacing: dp(12)
                            padding: dp(0), dp(0), dp(0), dp(80)

            # Profile Tab
            MDScreen:
                name: "profile_tab"

                MDScrollView:
                    do_scroll_x: False

                    MDBoxLayout:
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        padding: dp(16)
                        spacing: dp(16)

                        # Profile header
                        MDLabel:
                            text: "My Profile"
                            font_style: "Headline"
                            role: "small"
                            size_hint_y: None
                            height: dp(50)

                        # Profile card
                        MDCard:
                            id: profile_card
                            orientation: "vertical"
                            size_hint_y: None
                            height: dp(320)
                            padding: dp(24)
                            spacing: dp(12)
                            style: "elevated"

                            MDIcon:
                                icon: "account-circle"
                                halign: "center"
                                font_size: dp(80)
                                theme_text_color: "Custom"
                                text_color: app.theme_cls.primaryColor

                            MDLabel:
                                id: profile_name
                                text: "User Name"
                                halign: "center"
                                font_style: "Headline"
                                role: "small"

                            MDLabel:
                                id: profile_email
                                text: "email@example.com"
                                halign: "center"
                                theme_text_color: "Secondary"

                            MDDivider:

                            MDBoxLayout:
                                size_hint_y: None
                                height: dp(30)
                                spacing: dp(10)

                                MDIcon:
                                    icon: "briefcase"
                                    size_hint_x: None
                                    width: dp(30)
                                    theme_text_color: "Custom"
                                    text_color: app.theme_cls.primaryColor

                                MDLabel:
                                    id: profile_specialty
                                    text: "Specialty"

                            MDBoxLayout:
                                size_hint_y: None
                                height: dp(30)
                                spacing: dp(10)

                                MDIcon:
                                    icon: "identifier"
                                    size_hint_x: None
                                    width: dp(30)
                                    theme_text_color: "Custom"
                                    text_color: app.theme_cls.primaryColor

                                MDLabel:
                                    id: profile_code
                                    text: "User Code"

                        # Resume section
                        MDCard:
                            orientation: "vertical"
                            size_hint_y: None
                            height: dp(180)
                            padding: dp(24)
                            spacing: dp(16)
                            style: "elevated"

                            MDBoxLayout:
                                size_hint_y: None
                                height: dp(40)
                                spacing: dp(10)

                                MDIcon:
                                    icon: "file-document"
                                    size_hint_x: None
                                    width: dp(30)
                                    theme_text_color: "Custom"
                                    text_color: app.theme_cls.primaryColor

                                MDLabel:
                                    text: "Resume / CV"
                                    font_style: "Title"
                                    role: "medium"

                            MDLabel:
                                id: resume_status
                                text: "No resume uploaded"
                                theme_text_color: "Secondary"
                                size_hint_y: None
                                height: dp(30)

                            MDButton:
                                style: "outlined"
                                size_hint_x: 1
                                on_release: root.upload_resume()

                                MDButtonIcon:
                                    icon: "upload"

                                MDButtonText:
                                    text: "Upload Resume (PDF)"

                        # Bottom padding for ad banner
                        Widget:
                            size_hint_y: None
                            height: dp(100)

        # Advertisement banner placeholder
        MDBoxLayout:
            id: ad_banner_container
            size_hint_y: None
            height: dp(80)

        # Bottom navigation
        MDNavigationBar:
            id: bottom_nav
            on_switch_tabs: root.on_tab_switch(*args)

            MDNavigationItem:
                icon: "home"
                text: "Home"
                active: True

                MDNavigationItemIcon:
                    icon: "home"

                MDNavigationItemLabel:
                    text: "Home"

            MDNavigationItem:
                icon: "magnify"
                text: "Search"

                MDNavigationItemIcon:
                    icon: "magnify"

                MDNavigationItemLabel:
                    text: "Search"

            MDNavigationItem:
                icon: "account"
                text: "Profile"

                MDNavigationItemIcon:
                    icon: "account"

                MDNavigationItemLabel:
                    text: "Profile"
"""
)


class MainScreen(MDScreen):
    """Main application screen with bottom navigation"""

    def on_enter(self):
        """Initialize screen when entering"""
        from kivymd.app import MDApp
        from components.ad_banner import AdBanner

        app = MDApp.get_running_app()

        # Update welcome message
        if app.current_user:
            self.ids.welcome_label.text = f"Welcome, {app.current_user.name}!"
            self.update_profile()

        # Initialize selected category
        self.selected_category = "All"

        # Load category chips
        self.load_category_chips()

        # Load jobs
        self.load_jobs()
        self.load_featured_jobs()

        # Initialize ad banner
        ad_container = self.ids.ad_banner_container
        ad_container.clear_widgets()
        ad_banner = AdBanner()
        ad_container.add_widget(ad_banner)

    def on_tab_switch(self, bar, item, item_icon, item_text):
        """Handle bottom navigation tab switch"""
        tab_map = {"Home": "home_tab", "Search": "search_tab", "Profile": "profile_tab"}

        if item_text in tab_map:
            self.ids.content_manager.current = tab_map[item_text]

            if item_text == "Search":
                self.load_category_chips()
                self.load_jobs()
            elif item_text == "Profile":
                self.update_profile()

    def load_category_chips(self):
        """Load category filter chips"""
        from database import DatabaseManager
        from kivymd.uix.chip import MDChip, MDChipLeadingIcon, MDChipText

        db = DatabaseManager()
        categories = ["All"] + db.get_all_categories()

        chips_container = self.ids.category_chips
        chips_container.clear_widgets()

        for category in categories:
            chip = MDChip(
                MDChipLeadingIcon(
                    icon="check" if category == self.selected_category else "tag"
                ),
                MDChipText(text=category),
                type="filter",
                active=category == self.selected_category,
                on_release=lambda x, cat=category: self.on_category_select(cat),
            )
            chips_container.add_widget(chip)

    def on_category_select(self, category):
        """Handle category selection"""
        self.selected_category = category
        self.load_category_chips()  # Refresh chips to show selection
        self.load_jobs(self.ids.search_field.text)  # Reload jobs with filter

    def update_profile(self):
        """Update profile information"""
        from kivymd.app import MDApp
        from database import DatabaseManager

        app = MDApp.get_running_app()

        if app.current_user:
            # Refresh user data from database
            db = DatabaseManager()
            user = db.get_user_by_id(app.current_user.id)
            if user:
                app.current_user = user

            self.ids.profile_name.text = app.current_user.name
            self.ids.profile_email.text = app.current_user.email
            self.ids.profile_specialty.text = app.current_user.specialty
            self.ids.profile_code.text = f"Code: {app.current_user.user_code}"

            if app.current_user.resume_path:
                self.ids.resume_status.text = (
                    f"Resume: {app.current_user.resume_path.split('/')[-1]}"
                )
            else:
                self.ids.resume_status.text = "No resume uploaded"

    def load_jobs(self, keyword=""):
        """Load jobs into the search list"""
        from database import DatabaseManager
        from components.job_card import create_job_card

        db = DatabaseManager()

        # Get selected category
        category = getattr(self, "selected_category", "All")

        if keyword or (category and category != "All"):
            jobs = db.search_jobs_with_category(keyword if keyword else "", category)
        else:
            jobs = db.get_all_jobs()

        # Update results label
        category_text = f" in {category}" if category and category != "All" else ""
        self.ids.results_label.text = f"Found {len(jobs)} jobs{category_text}"

        # Clear and populate jobs list
        jobs_list = self.ids.jobs_list
        jobs_list.clear_widgets()

        for job in jobs:
            card = create_job_card(job, self.show_job_detail)
            jobs_list.add_widget(card)

    def load_featured_jobs(self):
        """Load featured jobs on home tab"""
        from database import DatabaseManager
        from components.job_card import create_job_card

        db = DatabaseManager()
        jobs = db.get_all_jobs()[:5]  # Top 5 jobs

        # Update stats
        all_jobs = db.get_all_jobs()
        countries = set(job.country for job in all_jobs)
        self.ids.jobs_count_label.text = f"{len(all_jobs)} Jobs"
        self.ids.countries_count_label.text = f"{len(countries)} Countries"

        # Clear and populate featured jobs
        featured_list = self.ids.featured_jobs_list
        featured_list.clear_widgets()

        for job in jobs:
            card = create_job_card(job, self.show_job_detail)
            featured_list.add_widget(card)

    def on_search_text(self, text):
        """Handle search text change"""
        from kivy.clock import Clock

        # Debounce search
        if hasattr(self, "_search_event"):
            self._search_event.cancel()

        self._search_event = Clock.schedule_once(lambda dt: self.load_jobs(text), 0.3)

    def show_job_detail(self, job):
        """Show job detail screen"""
        from kivymd.app import MDApp

        app = MDApp.get_running_app()
        app.selected_job = job
        app.switch_screen("job_detail")

    def upload_resume(self):
        """Handle resume upload"""
        try:
            from plyer import filechooser

            filechooser.open_file(
                filters=[("PDF files", "*.pdf")],
                on_selection=self._handle_resume_selection,
            )
        except Exception as e:
            # Fallback for platforms without file chooser
            self._show_upload_dialog()

    def _handle_resume_selection(self, selection):
        """Handle file selection"""
        if selection:
            from kivymd.app import MDApp
            from database import DatabaseManager

            app = MDApp.get_running_app()
            db = DatabaseManager()

            file_path = selection[0]
            if db.update_user_resume(app.current_user.id, file_path):
                app.current_user.resume_path = file_path
                self.update_profile()

    def _show_upload_dialog(self):
        """Show manual upload dialog"""
        from kivymd.uix.dialog import (
            MDDialog,
            MDDialogHeadlineText,
            MDDialogSupportingText,
            MDDialogContentContainer,
            MDDialogButtonContainer,
        )
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.button import MDButton, MDButtonText

        path_field = MDTextField(
            mode="outlined",
            size_hint_x=1,
        )

        def save_path(*args):
            if path_field.text:
                self._handle_resume_selection([path_field.text])
            dialog.dismiss()

        dialog = MDDialog(
            MDDialogHeadlineText(text="Enter Resume Path"),
            MDDialogSupportingText(text="Enter the full path to your PDF resume file:"),
            MDDialogContentContainer(path_field),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="Cancel"),
                    style="text",
                    on_release=lambda x: dialog.dismiss(),
                ),
                MDButton(
                    MDButtonText(text="Save"), style="filled", on_release=save_path
                ),
            ),
        )
        dialog.open()

    def do_logout(self):
        """Logout and return to welcome screen"""
        from kivymd.app import MDApp

        app = MDApp.get_running_app()
        app.current_user = None
        app.switch_screen("welcome")
