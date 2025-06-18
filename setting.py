from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivy.uix.switch import Switch
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton
from kivy.core.window import Window
import webbrowser

from kivy.graphics import Color, Rectangle
from kivy.utils import platform

Window.size = (350, 640)

# --- Settings Page Screen ---
class SettingsPage(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # --- Background color ---
        with self.canvas.before:
            Color(0, 0, 1, 0.8)  # Semi-transparent Blue
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        main_layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        # --- Top Bar: Back icon + "Settings" Text ---
        top_bar = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=50,
            spacing=5,
            padding=[0, 2, 0, 0],
        )

        back_icon = MDIconButton(
            icon="arrow-left",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=("24dp", "24dp"),
            pos_hint={"center_y": 0.5, "center_x": 0.9},
            on_press=self.go_back  # Go back when pressed
        )

        settings_label = MDLabel(
            text="Settings",
            font_style="H6",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            valign="middle",
            halign="left",
            size_hint_x=None,
            width=150,
        )

        top_bar.add_widget(back_icon)
        top_bar.add_widget(settings_label)
        main_layout.add_widget(top_bar)

        # --- Scrollable Content ---
        scroll = MDScrollView()
        content_layout = MDBoxLayout(orientation='vertical', padding=(0, 20), spacing=20, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))

        # Notifications card
        notif_card = MDCard(
            size_hint_y=None,
            height=70,
            radius=[15],
            md_bg_color="white",
            padding=(15, 10),
            style="elevated"
        )

        row = MDBoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint=(1, 1),
        )

        notif_label = MDLabel(
            text="  Notifications",
            font_style="Subtitle1",
            halign="left",
            valign="middle",
            size_hint_x=0.8
        )
        notif_label.bind(size=notif_label.setter('text_size'))

        self.notif_switch = Switch(
            active=True,
            size_hint=(None, None),
            size=("40dp", "24dp"),
            pos_hint={"center_y": 0.5}
        )

        switch_container = MDBoxLayout(
            size_hint_x=0.2,
            orientation='horizontal',
            padding=[0, 28, 0, 0],
        )
        switch_container.add_widget(self.notif_switch)

        row.add_widget(notif_label)
        row.add_widget(switch_container)
        notif_card.add_widget(row)
        content_layout.add_widget(notif_card)

        # Section Header
        content_layout.add_widget(MDLabel(
            text="Support & Info",
            font_style="H6",
            bold=True,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=40
        ))

        # --- List items inside cards ---
        content_layout.add_widget(
            self.create_card_item("FAQs", "help-circle-outline", self.open_faqs))
        content_layout.add_widget(self.create_card_item("Contact Support", "email-outline", self.contact_support))
        content_layout.add_widget(
            self.create_card_item("Privacy Policy & Terms", "shield-check-outline", self.open_privacy_policy))
        content_layout.add_widget(self.create_card_item("App Version: 1.0.0", "information-outline"))

        scroll.add_widget(content_layout)
        main_layout.add_widget(scroll)

        self.add_widget(main_layout)

    def create_card_item(self, text, icon_name, on_click=None):
        card = MDCard(
            size_hint_y=None,
            height=70,
            radius=[15],
            md_bg_color="white",
            padding=(5, 5),
            style="elevated"
        )

        item = OneLineIconListItem(text=text)

        if on_click:
            item.bind(on_release=on_click)

        item.add_widget(IconLeftWidget(icon=icon_name))
        card.add_widget(item)
        return card

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def contact_support(self, *args):
        recipient_email = "crackitedu777@example.com"
        subject = "Support Request"
        body = "Hello, I need assistance with..."
        mailto_link = f"mailto:{recipient_email}?subject={subject}&body={body}"

        webbrowser.open(mailto_link)

    def open_privacy_policy(self, *args):
        webbrowser.open("https://pavithra-1910.github.io/privacy/")

    def open_faqs(self, *args):
        webbrowser.open("https://pavithra-1910.github.io/faq1/")

    def go_back(self, instance):
        self.manager.current = 'homepage'
