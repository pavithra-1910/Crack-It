from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock  # Import Clock for scheduling UI updates
from firebase_admin import credentials, initialize_app, firestore
import threading

# Set window size
Window.size = (350, 640)

# Initialize Firebase Admin SDK (only once!)
try:
    initialize_app()
except:
    pass
db = firestore.client()

class NotificationScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (0, 0, 1, 0.8)  # background blue

        # Top bar
        top_bar = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(50),
            padding=dp(10),
            spacing=dp(10),
            pos_hint={"top": 1},
        )

        back_button = MDIconButton(
            icon="arrow-left",
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            pos_hint={"center_y": 0.5},
            on_release=self.go_back,
        )

        title_label = MDLabel(
            text="Notifications",
            font_style="H6",
            size_hint_x=0.8,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            halign="left",
            valign="middle",
        )

        top_bar.add_widget(back_button)
        top_bar.add_widget(title_label)
        self.add_widget(top_bar)

        # Scroll area
        self.scroll = ScrollView(
            size_hint=(1, None),
            size=(Window.width, Window.height - dp(50)),
            pos_hint={"top": 0.92},
        )

        self.notifications_container = MDBoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            size_hint_y=None,
        )
        self.notifications_container.bind(minimum_height=self.notifications_container.setter('height'))

        self.scroll.add_widget(self.notifications_container)
        self.add_widget(self.scroll)

        # Listen to notifications collection
        threading.Thread(target=self.listen_to_notifications, daemon=True).start()

    def create_notification_card(self, title, message, time):
        card = MDCard(
            orientation="vertical",
            size_hint_x=1,
            size_hint_y=None,
            height=dp(100),
            padding=dp(10),
            ripple_behavior=True,
        )

        title_label = MDLabel(
            text=title,
            font_style="Subtitle1",
            bold=True,
            theme_text_color="Primary",
        )

        message_label = MDLabel(
            text=message,
            theme_text_color="Secondary",
        )

        time_label = MDLabel(
            text=time,
            font_style="Caption",
            theme_text_color="Hint",
        )

        card.add_widget(title_label)
        card.add_widget(message_label)
        card.add_widget(time_label)

        return card

    def listen_to_notifications(self):
        notifications_ref = db.collection('notifications')
        notifications_ref.on_snapshot(self.on_notification_update)

    def on_notification_update(self, col_snapshot, changes, read_time):
        # Schedule UI update on main thread
        Clock.schedule_once(lambda dt: self.update_ui_with_notifications(col_snapshot))

    def update_ui_with_notifications(self, col_snapshot):
        # Clear existing notifications
        self.notifications_container.clear_widgets()

        if len(col_snapshot) == 0:
            no_notification_label = MDLabel(
                text="No Notifications",
                font_style="H6",
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 0, 0, 1),
                size_hint_y=None,
                height=50,
            )
            self.notifications_container.add_widget(no_notification_label)

        # Process and display each notification
        for doc in col_snapshot:
            data = doc.to_dict()

            # Check if document has 'title', 'message', and 'time' fields
            title = data.get('title', 'No Title')
            message = data.get('message', 'No Message')
            time = data.get('time', 'No Time')

            # Debugging print statements to check what data is fetched
            print(f"Title: {title}, Message: {message}, Time: {time}")

            card = self.create_notification_card(title, message, time)
            self.notifications_container.add_widget(card)

    def go_back(self, instance):
        self.manager.current = "homepage"
