"""
Main Screen - Main application section after login with bottom navigation bar
"""

# Import Kivy libraries
from kivy.lang import Builder
from kivy.properties import StringProperty

# Import KivyMD components
from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationbar import (
    MDNavigationBar,
    MDNavigationItem,
    MDNavigationItemIcon,
    MDNavigationItemLabel,
)


# Define UI with KV language
Builder.load_string(
    """
<MainScreen>:
    name: "main"

    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: app.theme_cls.backgroundColor

        # Content section
        MDScreenManager:
            id: content_manager

            # Home tab
            MDScreen:
                name: "home_tab"

                MDBoxLayout:
                    orientation: "vertical"
                    padding: dp(16)
                    spacing: dp(16)

                    # Page header
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

            # Search tab
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

                    # Search input field
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

                    # Results count display
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

            # Profile tab
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

                        # Bottom spacing for ad banner
                        Widget:
                            size_hint_y: None
                            height: dp(100)

        # Ad banner container
        MDBoxLayout:
            id: ad_banner_container
            size_hint_y: None
            height: dp(80)

        # Bottom navigation bar
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
    """Main application screen with bottom navigation bar"""

    # Loading control flags to prevent unnecessary reloading
    _initialized = False
    _search_loaded = False
    _categories_cache = None
    _batch_event = None

    # Number of cards added per frame (to prevent freezing)
    BATCH_SIZE = 5

    def on_enter(self):
        """Initialize screen on enter - only once"""
        from kivymd.app import MDApp
        from kivy.clock import Clock

        app = MDApp.get_running_app()

        # Update welcome message
        if app.current_user:
            self.ids.welcome_label.text = f"Welcome, {app.current_user.name}!"

        if not self._initialized:
            self._initialized = True
            self.selected_category = "All"
            self._pending_jobs = []
            self._pending_featured = []

            # Load with delay to prevent hang on screen entry
            Clock.schedule_once(self._deferred_init, 0)
        else:
            # Only update stats
            Clock.schedule_once(lambda dt: self._update_stats(), 0)

    def _deferred_init(self, dt):
        """Lazy loading after screen render"""
        from kivy.clock import Clock
        from components.ad_banner import AdBanner

        # Load immediate stats (lightweight)
        self._update_stats()

        # Load featured jobs in batches
        self._load_featured_jobs_async()

        # Add ad banner
        ad_container = self.ids.ad_banner_container
        if not ad_container.children:
            ad_banner = AdBanner()
            ad_container.add_widget(ad_banner)

    def on_tab_switch(self, bar, item, item_icon, item_text):
        """Handle tab switch in the bottom navigation bar"""
        # Map tab name to screen name
        tab_map = {"Home": "home_tab", "Search": "search_tab", "Profile": "profile_tab"}

        if item_text in tab_map:
            self.ids.content_manager.current = tab_map[item_text]

            if item_text == "Search":
                # Only load chips and jobs on first visit
                if not self._search_loaded:
                    self._search_loaded = True
                    from kivy.clock import Clock

                    Clock.schedule_once(lambda dt: self._load_search_tab(), 0)
            elif item_text == "Profile":
                self.update_profile()

    def _load_search_tab(self):
        """Lazy load search tab"""
        self.load_category_chips()
        self.load_jobs()

    def load_category_chips(self):
        """Load category filter chips - with caching"""
        from database import DatabaseManager
        from kivymd.uix.chip import MDChip, MDChipLeadingIcon, MDChipText

        # Cache categories to avoid re-querying
        if self._categories_cache is None:
            db = DatabaseManager()
            self._categories_cache = ["All"] + db.get_all_categories()

        chips_container = self.ids.category_chips
        chips_container.clear_widgets()

        # Create a chip for each category
        for category in self._categories_cache:
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
        # Only update chip states without rebuilding
        self._update_chip_states()
        self.load_jobs(self.ids.search_field.text)

    def _update_chip_states(self):
        """Update chip states without rebuilding"""
        chips_container = self.ids.category_chips
        for chip in chips_container.children:
            # Extract category name from chip
            chip_text = ""
            for child in chip.children:
                from kivymd.uix.chip import MDChipText

                if isinstance(child, MDChipText):
                    chip_text = child.text
                    break
            is_active = chip_text == self.selected_category
            chip.active = is_active
            # Update icon
            for child in chip.children:
                from kivymd.uix.chip import MDChipLeadingIcon

                if isinstance(child, MDChipLeadingIcon):
                    child.icon = "check" if is_active else "tag"
                    break

    def update_profile(self):
        """Update user profile information"""
        from kivymd.app import MDApp
        from database import DatabaseManager

        app = MDApp.get_running_app()

        if app.current_user:
            # Refresh user data from database
            db = DatabaseManager()
            user = db.get_user_by_id(app.current_user.id)
            if user:
                app.current_user = user

            # Display information in UI
            self.ids.profile_name.text = app.current_user.name
            self.ids.profile_email.text = app.current_user.email
            self.ids.profile_specialty.text = app.current_user.specialty
            self.ids.profile_code.text = f"Code: {app.current_user.user_code}"

            # Display resume status
            if app.current_user.resume_path:
                self.ids.resume_status.text = (
                    f"Resume: {app.current_user.resume_path.split('/')[-1]}"
                )
            else:
                self.ids.resume_status.text = "No resume uploaded"

    def load_jobs(self, keyword=""):
        """Load jobs in search list - batch loading"""
        from database import DatabaseManager

        # Cancel previous batch loading
        self._cancel_batch_loading()

        db = DatabaseManager()
        category = getattr(self, "selected_category", "All")

        # Search by keyword and category
        if keyword or (category and category != "All"):
            jobs = db.search_jobs_with_category(keyword if keyword else "", category)
        else:
            jobs = db.get_all_jobs()

        # Update results label
        category_text = f" in {category}" if category and category != "All" else ""
        self.ids.results_label.text = f"Found {len(jobs)} jobs{category_text}"

        # Clear current list
        jobs_list = self.ids.jobs_list
        jobs_list.clear_widgets()

        # Batch loading to prevent UI freeze
        self._pending_jobs = list(jobs)
        self._add_jobs_batch()

    def _cancel_batch_loading(self):
        """Cancel ongoing batch loading"""
        if self._batch_event:
            self._batch_event.cancel()
            self._batch_event = None

    def _add_jobs_batch(self, dt=None):
        """Add cards in batches - multiple cards per frame"""
        from components.job_card import create_job_card
        from kivy.clock import Clock

        if not self._pending_jobs:
            self._batch_event = None
            return

        jobs_list = self.ids.jobs_list
        # Take a batch of jobs
        batch = self._pending_jobs[: self.BATCH_SIZE]
        self._pending_jobs = self._pending_jobs[self.BATCH_SIZE :]

        # Create a card for each job
        for job in batch:
            card = create_job_card(job, self.show_job_detail)
            jobs_list.add_widget(card)

        # Continue loading in next frame
        if self._pending_jobs:
            self._batch_event = Clock.schedule_once(self._add_jobs_batch, 0)

    def _update_stats(self):
        """Update stats with lightweight queries"""
        from database import DatabaseManager

        db = DatabaseManager()
        # Get jobs and countries count
        jobs_count = db.get_jobs_count()
        countries_count = db.get_countries_count()
        # Display in UI
        self.ids.jobs_count_label.text = f"{jobs_count} Jobs"
        self.ids.countries_count_label.text = f"{countries_count} Countries"

    def _load_featured_jobs_async(self):
        """Load featured jobs in batches"""
        from database import DatabaseManager
        from kivy.clock import Clock

        db = DatabaseManager()
        # Get 5 recent jobs as featured
        jobs = db.get_all_jobs(limit=5)

        featured_list = self.ids.featured_jobs_list
        featured_list.clear_widgets()

        self._pending_featured = list(jobs)
        self._add_featured_batch()

    def _add_featured_batch(self, dt=None):
        """Add featured jobs in batches"""
        from components.job_card import create_job_card
        from kivy.clock import Clock

        if not self._pending_featured:
            return

        featured_list = self.ids.featured_jobs_list
        # Take a batch
        batch = self._pending_featured[: self.BATCH_SIZE]
        self._pending_featured = self._pending_featured[self.BATCH_SIZE :]

        # Create a card for each job
        for job in batch:
            card = create_job_card(job, self.show_job_detail)
            featured_list.add_widget(card)

        # Continue in next frame
        if self._pending_featured:
            Clock.schedule_once(self._add_featured_batch, 0)

    def on_search_text(self, text):
        """Handle search text change with debounce"""
        from kivy.clock import Clock

        # Debounce search - increase debounce time for fast typing
        if hasattr(self, "_search_event") and self._search_event:
            self._search_event.cancel()

        self._search_event = Clock.schedule_once(lambda dt: self.load_jobs(text), 0.5)

    def show_job_detail(self, job):
        """Show job detail screen"""
        from kivymd.app import MDApp

        app = MDApp.get_running_app()
        app.selected_job = job
        app.switch_screen("job_detail")

    def upload_resume(self):
        """Handle resume upload"""
        try:
            # Use system file chooser
            from plyer import filechooser

            filechooser.open_file(
                filters=[("PDF files", "*.pdf")],
                on_selection=self._handle_resume_selection,
            )
        except Exception as e:
            # Platforms without file chooser
            self._show_upload_dialog()

    def _handle_resume_selection(self, selection):
        """Handle resume file selection"""
        if selection:
            from kivymd.app import MDApp
            from database import DatabaseManager

            app = MDApp.get_running_app()
            db = DatabaseManager()

            # Save resume path in database
            file_path = selection[0]
            if db.update_user_resume(app.current_user.id, file_path):
                app.current_user.resume_path = file_path
                self.update_profile()

    def _show_upload_dialog(self):
        """Show manual resume path upload dialog"""
        from kivymd.uix.dialog import (
            MDDialog,
            MDDialogHeadlineText,
            MDDialogSupportingText,
            MDDialogContentContainer,
            MDDialogButtonContainer,
        )
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.button import MDButton, MDButtonText

        # Path input field
        path_field = MDTextField(
            mode="outlined",
            size_hint_x=1,
        )

        def save_path(*args):
            """Save the entered path"""
            if path_field.text:
                self._handle_resume_selection([path_field.text])
            dialog.dismiss()

        # Create and show dialog
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
        # Clear current user data
        app.current_user = None

        # Reset flags for re-entry
        self._initialized = False
        self._search_loaded = False
        self._categories_cache = None
        self._cancel_batch_loading()

        # Navigate to welcome screen
        app.switch_screen("welcome")
