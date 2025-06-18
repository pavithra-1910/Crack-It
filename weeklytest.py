from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
import webbrowser
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivy.uix.image import AsyncImage

from firebase_admin import credentials, initialize_app, firestore, get_app, App

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase-admin.json")
try:
    app = get_app()  # Try to get the default app
except AppDoesNotExistError:
    app = initialize_app(cred)  # Initialize app if it doesn't exist
db = firestore.client()

# Set window size
from kivy.core.window import Window
Window.size = (350, 640)

class WeeklyTestScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDFloatLayout()

        # Back button
        back_button = MDIconButton(
            icon="arrow-left",
            size_hint=(None, None),
            size=("40dp", "40dp"),
            pos_hint={"top": 0.98, "left": 0.05},
            on_press=self.go_back,
            theme_text_color="Custom",
            icon_color=(0, 0, 1, 0.8)
        )

        # Title label
        test_zone_label = MDLabel(
            text="Test Zone",
            font_style="H5",
            bold=True,
            halign="center",
            size_hint_y=None,
            pos_hint={"center_x": 0.3, "top": 0.999},
            theme_text_color="Custom",
            text_color=(0, 0, 1, 0.8)
        )

        # Scroll view for tests
        scroll = ScrollView(size_hint=(1, 0.8), pos_hint={'y': 0.1})
        self.box = MDBoxLayout(orientation='vertical', spacing=20, size_hint_y=None, padding=10)
        self.box.bind(minimum_height=self.box.setter('height'))

        scroll.add_widget(self.box)

        layout.add_widget(scroll)
        layout.add_widget(back_button)
        layout.add_widget(test_zone_label)
        self.add_widget(layout)

        # Fetch tests after screen created
        self.fetch_tests()

    def fetch_tests(self):
        tests_ref = db.collection('weekly_tests')
        tests = list(tests_ref.stream())

        if len(tests) == 0:
            no_test_image = AsyncImage(
                source="test.webp",
                size_hint=(None, None),
                size=("180dp", "180dp"),
                pos_hint={"center_x": 0.5},
            )
            no_test_label = MDLabel(
                text="No test available",
                font_style="H6",
                halign="center",
                theme_text_color="Custom",
                text_color=(0.9, 0, 0, 1),
                size_hint_y=None,
                height=50,
                pos_hint={"center_x": 0.5, "center_y": 0.3}
            )
            self.box.add_widget(no_test_image)
            self.box.add_widget(no_test_label)
        else:
            for test in tests:
                test_data = test.to_dict()

                test_card = MDCard(
                    orientation='vertical',
                    size_hint=(0.9, None),
                    height=200,
                    pos_hint={'center_x': 0.5},
                    radius=[20],
                    md_bg_color=(0, 0, 1, 0.7),
                    padding=20,
                )

                title = MDLabel(
                    text=f"Weekly Test {test_data.get('week_number', '')}",
                    font_style='H5',
                    halign='center',
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 1)
                )

                subtitle = MDLabel(
                    text=f"Deadline: {test_data.get('deadline', '')}",
                    halign='center',
                    theme_text_color="Custom",
                    text_color=(1, 1, 1, 0.7),
                    font_style='Subtitle1'
                )

                # Passing URL dynamically to the start_test method
                start_button = MDRaisedButton(
                    text="Start Test",
                    pos_hint={'center_x': 0.5},
                    md_bg_color=(1, 1, 1, 1),
                    text_color=(0, 0, 1, 1),
                    on_press=lambda instance, url=test_data.get('form_url', ''): self.start_test(url)
                )

                test_card.add_widget(title)
                test_card.add_widget(subtitle)
                test_card.add_widget(start_button)

                self.box.add_widget(test_card)

    def start_test(self, url):
        if url:
            webbrowser.open(url)
        else:
            print("No form URL provided for this test.")

    def go_back(self, instance):
        self.manager.current = 'homepage'  # Update this if needed
