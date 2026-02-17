"""
Ad Banner Component
Displays rotating advertisements at the bottom of screens with weighted randomization
"""

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout


# Load ad banner UI with KV language
Builder.load_string(
    """
<AdBanner>:
    size_hint_y: None
    height: dp(80)
    padding: dp(8)
    md_bg_color: app.theme_cls.surfaceContainerHighColor

    MDCard:
        id: ad_card
        orientation: "horizontal"
        padding: dp(12)
        spacing: dp(12)
        style: "filled"
        md_bg_color: app.theme_cls.surfaceContainerColor
        on_release: root.on_ad_click()

        MDIcon:
            id: ad_icon
            icon: root.current_icon
            size_hint_x: None
            width: dp(40)
            font_size: dp(32)
            theme_text_color: "Custom"
            text_color: app.theme_cls.primaryColor

        MDBoxLayout:
            orientation: "vertical"
            spacing: dp(2)

            MDLabel:
                id: ad_title
                text: root.current_title
                font_style: "Title"
                role: "small"
                shorten: True
                shorten_from: "right"
                text_size: self.width, None

            MDLabel:
                id: ad_description
                text: root.current_description
                font_style: "Body"
                role: "small"
                theme_text_color: "Secondary"
                shorten: True
                shorten_from: "right"
                text_size: self.width, None

        MDBoxLayout:
            size_hint_x: None
            width: dp(50)

            MDLabel:
                text: "AD"
                halign: "center"
                font_style: "Label"
                role: "small"
                theme_text_color: "Custom"
                text_color: app.theme_cls.primaryColor
                size_hint_y: None
                height: dp(20)
                pos_hint: {"center_y": 0.5}
"""
)


# Ad banner class with automatic ad rotation
class AdBanner(MDBoxLayout):
    """Ad banner with automatic rotation"""

    # UI-visible properties
    current_title = StringProperty("Advertisement")
    current_description = StringProperty("Loading...")
    current_icon = StringProperty("bullhorn")
    current_ad = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ad rotation interval in seconds
        self.rotation_interval = 10
        self._rotation_event = None
        # Initialize ads with a short delay
        Clock.schedule_once(self._init_ads, 0.5)

    # Initialize and start ad rotation
    def _init_ads(self, dt):
        """Initialize ad rotation"""
        self.load_next_ad()
        self.start_rotation()

    # Start ad rotation timer
    def start_rotation(self):
        """Start ad rotation timer"""
        if self._rotation_event:
            self._rotation_event.cancel()

        self._rotation_event = Clock.schedule_interval(
            self._rotate_ad, self.rotation_interval
        )

    # Stop ad rotation
    def stop_rotation(self):
        """Stop ad rotation"""
        if self._rotation_event:
            self._rotation_event.cancel()
            self._rotation_event = None

    # Rotate to next ad with fade animation
    def _rotate_ad(self, dt):
        """Rotate to next ad with animation"""
        # Fade out current ad
        card = self.ids.ad_card
        anim_out = Animation(opacity=0, duration=0.3)
        anim_out.bind(on_complete=lambda *args: self._load_and_fade_in())
        anim_out.start(card)

    # Load next ad and show with fade-in animation
    def _load_and_fade_in(self):
        """Load next ad and show with animation"""
        self.load_next_ad()
        card = self.ids.ad_card
        Animation(opacity=1, duration=0.3).start(card)

    # Load weighted random ad from database
    def load_next_ad(self):
        """Load next weighted random ad"""
        from database import DatabaseManager

        db = DatabaseManager()
        ad = db.get_weighted_random_ad()

        if ad:
            self.current_ad = ad
            self.current_title = ad.title
            self.current_description = ad.description
            self.current_icon = ad.icon
        else:
            # Show default ad if no ads in database
            self.current_title = "Job Finder"
            self.current_description = "Find your dream job today!"
            self.current_icon = "briefcase-search"

    # Handle ad click and show details in dialog
    def on_ad_click(self):
        """Handle ad click"""
        from kivymd.uix.dialog import (
            MDDialog,
            MDDialogHeadlineText,
            MDDialogSupportingText,
            MDDialogButtonContainer,
        )
        from kivymd.uix.button import MDButton, MDButtonText

        # Set dialog content based on current ad
        if self.current_ad:
            message = (
                f"Company: {self.current_ad.company}\n\n{self.current_ad.description}"
            )
            title = self.current_ad.title
        else:
            message = "Check out our latest job listings!"
            title = "Job Finder"

        # Build and show ad detail dialog
        dialog = MDDialog(
            MDDialogHeadlineText(text=title),
            MDDialogSupportingText(text=message),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="Close"),
                    style="text",
                    on_release=lambda x: dialog.dismiss(),
                ),
                MDButton(
                    MDButtonText(text="Learn More"),
                    style="filled",
                    on_release=lambda x: dialog.dismiss(),
                ),
            ),
        )
        dialog.open()
