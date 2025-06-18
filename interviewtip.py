from firebase_admin import credentials, db
import firebase_admin
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.fitimage import FitImage
from kivy.graphics import Color, Rectangle

# Firebase Initialization
cred = credentials.Certificate("firebase-admin.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://crackit-8371d-default-rtdb.firebaseio.com'
    })

# Fetching Interview Tips from Firebase
ref = db.reference('interview_tips')
interview_tips = ref.get()
interview_tips = interview_tips if interview_tips else {}


class InterviewTipsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set background color using Canvas
        with self.canvas.before:
            Color(0, 0, 1, 0.8)  # Blue with 80% opacity
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Update rectangle size on window resize
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Create a main layout
        main_layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        # Custom toolbar with back button
        toolbar = MDBoxLayout(size_hint_y=None, height="50dp", orientation='horizontal')

        back_button = MDIconButton(
            icon="arrow-left",
            size_hint_x=None,
            width="50dp",
            theme_icon_color="Custom",
            icon_color=(1,1,1,1),
            on_press=self.back_button
        )
        toolbar.add_widget(back_button)

        title_label = MDLabel(
            text="Interview Tips",
            theme_text_color="Custom",
            text_color=(1,1,1,1),
            halign="left",
            font_style="H6"
        )
        toolbar.add_widget(title_label)

        main_layout.add_widget(toolbar)

        # Create the MDCard
        card = MDCard(
            orientation='vertical',
            size_hint=(None, None),
            size=("320dp", "580dp"),
            pos_hint={"center_x": 0.5},
            radius=[25],
            md_bg_color=(1, 1, 1, 1),  # White card
            padding=15,
            spacing=15,
            elevation=8,
        )

        # Add the Image
        fit_image = FitImage(
            source="n2.jpg",
            pos_hint={"center_x": 0.5},
            height="100dp",
            radius=[20]
        )
        card.add_widget(fit_image)

        # Interview Tip Label
        self.topic_label = MDLabel(
            text="Interview Tips will appear here",
            font_style="H5",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None
        )
        card.add_widget(self.topic_label)

        # ScrollView for bullet points
        scroll_view = ScrollView()
        self.bullet_point_label = MDLabel(
            text="Content will appear here",
            font_style="Body1",
            theme_text_color="Custom",
            text_color=(0, 0, 1, 0.8),
            halign="left",
            size_hint_y=None
        )
        scroll_view.add_widget(self.bullet_point_label)
        card.add_widget(scroll_view)

        # Next Button
        next_button = MDRaisedButton(
            text="Next",
            size_hint_y=None,
            height="50dp",
            width="200dp",
            pos_hint={"center_x": 0.5},
            on_press=self.show_tip
        )
        card.add_widget(next_button)

        # Add everything to main layout
        main_layout.add_widget(card)
        self.add_widget(main_layout)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def back_button(self, instance):
        self.manager.current = "interview_section"

    def show_tip(self, instance):
        if len(interview_tips.get('tips', [])) > 0:
            tip = interview_tips['tips'].pop(0)
            self.topic_label.text = f"Tip: {tip['title']}"
            bullet_points = "\n\n".join([f"- {point}" for point in tip['points']])
            self.bullet_point_label.text = bullet_points
        else:
            self.topic_label.text = "No more tips!"
            self.bullet_point_label.text = ""
