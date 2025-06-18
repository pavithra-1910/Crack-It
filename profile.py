import firebase_admin
from firebase_admin import credentials, db
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.uix.floatlayout import FloatLayout

# Initialize Firebase only if it hasn't been initialized yet
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-admin.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://crackit-8371d-default-rtdb.firebaseio.com/'
    })

class ProfilePage(Screen):
    def __init__(self, email="", **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.regno = self.extract_regno(email)

        # Outer layout with blue background
        outer_layout = MDBoxLayout(orientation='vertical')
        outer_layout.md_bg_color = (0, 0, 1, 0.8)

        # Inner layout to position widgets
        self.layout = FloatLayout()
        outer_layout.add_widget(self.layout)

        self.build_ui()

        # Add outer layout to screen
        self.add_widget(outer_layout)

    def build_ui(self):
        # Top Bar with back button and title
        top_layout = MDBoxLayout(
            size_hint=(1, None),
            height=80,
            padding=(10, 30, 10, 10),
            orientation='horizontal',
            pos_hint={'top': 1}
        )

        back_button = MDIconButton(
            icon="arrow-left",
            on_release=self.go_back,
            size_hint=(None, None),
            size=(30, 30),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )

        profile_name_label = MDLabel(
            text="Profile",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H5",
            bold=True,
            halign='left',
            valign='middle',
            size_hint=(1, 1),
            pos_hint={'center_y':0.8}
        )

        top_layout.add_widget(back_button)
        top_layout.add_widget(profile_name_label)

        # Profile Card
        profile_card = MDCard(
            orientation='vertical',
            size_hint=(None, None),
            width=390,
            height=300,
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            radius=[30],
            md_bg_color=(1, 1, 1, 0.5),
            padding=(5, 6),
            spacing=5,
            elevation=10
        )

        # Card layout for text and circular initial
        card_layout = MDBoxLayout(
            orientation='vertical',
            spacing=2,  # Reduced spacing
            padding=(10, 5),  # Reduced padding
        )

        # Circular card for profile initial
        self.profile_initial_card = MDCard(
            size_hint=(None, None),
            size=(100, 100),
            radius=[50],
            md_bg_color=(0.2, 0.4, 0.8, 1),  # Dark blue
            pos_hint={'center_x': 0.5, 'center_y': 0.99},
            elevation=6
        )

        # Initial label inside the circular card
        self.profile_initial = MDLabel(
            text="",  # Will be set later
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # White text
            bold=True,
            font_style="H4",
            halign="center",
            valign="middle"
        )
        self.profile_initial.bind(size=self.profile_initial.setter('text_size'))
        self.profile_initial_card.add_widget(self.profile_initial)

        # Add circular card to layout
        card_layout.add_widget(self.profile_initial_card)

        # Labels for name, regno, email with reduced space
        self.username_label = MDLabel(
            text="Name: Loading...",
            theme_text_color="Custom",
            bold=True,
            halign="center",
            line_height=1.0,
            text_color=(0, 0, 0, 1),
        )
        self.regno_label = MDLabel(
            text=f"Reg No: {self.regno}",
            theme_text_color="Custom",
            bold=True,
            halign="center",
            line_height=1.0,
            text_color=(0, 0, 0, 1),
        )
        self.email_label = MDLabel(
            text=f"Email: {self.email}",
            theme_text_color="Custom",
            bold=True,
            halign="center",
            line_height=1.0,
            text_color=(0, 0, 0, 1),
        )

        card_layout.add_widget(self.username_label)
        card_layout.add_widget(self.regno_label)
        card_layout.add_widget(self.email_label)

        profile_card.add_widget(card_layout)

        sign_out_button = MDRaisedButton(
            text="Sign Out",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5, "y": 0.05},
            md_bg_color=(1, 0, 0, 1)
        )
        sign_out_button.bind(on_release=self.sign_out)

        # Add widgets to the screen layout
        self.layout.add_widget(top_layout)
        self.layout.add_widget(profile_card)
        self.layout.add_widget(sign_out_button)

    def extract_regno(self, email):
        return email.split('@')[0] if email else "Not Found"

    def fetch_user_data(self):
        try:
            ref = db.reference('user')
            all_users = ref.get()

            matched_regno = None

            for regno, user_data in all_users.items():
                email_in_db = user_data.get('username', {}).get('email')
                if email_in_db == self.email:
                    matched_regno = regno
                    break

            if matched_regno:
                self.regno = matched_regno
                user_info = all_users[matched_regno]['username']
                user_name = user_info.get('name', 'N/A')
                self.username_label.text = f"Name: {user_name}"
                self.email_label.text = f"Email: {user_info.get('email', 'N/A')}"
                self.regno_label.text = f"Reg No: {matched_regno}"

                # Set initial in circular profile card
                if user_name:
                    self.profile_initial.text = user_name[0].upper()
            else:
                self.username_label.text = "Name: Not found"
                self.email_label.text = f"Email: {self.email}"
                self.regno_label.text = "Reg No: Not found"

        except Exception as e:
            self.username_label.text = "Name: Error"
            self.regno_label.text = "Reg No: Error"
            self.email_label.text = "Email: Error"
            print(f"Error fetching user data: {e}")

    def sign_out(self, instance):
        with open("user_token.txt", "w") as f:
            f.write("")
        self.manager.current = 'login'

    def go_back(self, instance):
        self.manager.current = 'homepage'

    def on_enter(self):
        """Called when the screen is entered."""
        self.fetch_user_data()
