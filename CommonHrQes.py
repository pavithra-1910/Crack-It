from firebase_admin import credentials, db
import firebase_admin
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.fitimage import FitImage
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock


if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-admin.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://crackit-8371d-default-rtdb.firebaseio.com'
    })


ref = db.reference('interview_questions')
questions = ref.get()
questions = list(questions.values()) if questions else []


class CommonHrQes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        with self.canvas.before:
            Color(0, 0,1,0.8)  # Light Blue
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)


        main_layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)


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
            text="Common HR",
            theme_text_color="Custom",
            text_color=(1,1,1,1),
            halign="left",
            font_style="H6"
        )
        toolbar.add_widget(title_label)

        main_layout.add_widget(toolbar)


        card = MDCard(
            orientation='vertical',
            size_hint=(None, None),
            size=("320dp", "580dp"),
            pos_hint={"center_x": 0.5},
            radius=[25],
            md_bg_color=(1, 1, 1, 1),
            padding=15,
            spacing=15,
            elevation=8,
        )


        fit_image = FitImage(
            source="n1.jpg",
            pos_hint={"center_x": 0.5},
            height="100dp",
            radius=[20]
        )
        card.add_widget(fit_image)


        self.question_label = MDLabel(
            text="Question will appear here",
            font_style="H6",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None
        )
        card.add_widget(self.question_label)


        self.tip_label = MDLabel(
            text="Tip will appear here",
            font_style="Body1",
            theme_text_color="Custom",
            text_color=(0, 0, 1, 1),
            halign="center",
            size_hint_y=None
        )
        card.add_widget(self.tip_label)


        scroll_view = ScrollView()
        self.response_label = MDLabel(
            text="Response will appear here",
            font_style="Body1",
            theme_text_color="Custom",
            text_color=(0.2, 0.2, 0.2, 1),
            halign="left",
            size_hint_y=None,
            text_size=(300, None)
        )
        scroll_view.add_widget(self.response_label)
        card.add_widget(scroll_view)


        next_button = MDRaisedButton(
            text="Next",
            size_hint_y=None,
            height="50dp",
            width="200dp",
            pos_hint={"center_x": 0.5},
            on_press=self.show_question
        )
        card.add_widget(next_button)


        main_layout.add_widget(card)
        self.add_widget(main_layout)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def back_button(self, instance):
        self.manager.current = "interview_section"

    def on_enter(self, *args):
        Clock.schedule_once(self.show_question, 0)

    def show_question(self, *args):
        if self.question_label.text == "No more questions!":
            return

        if len(questions) > 0:
            item = questions.pop(0)
            self.question_label.text = f"Q: {item.get('question', 'No question available')}"
            self.tip_label.text = f"Tip: {item.get('tip', '')}"
            self.response_label.text = f"Response: {item.get('response', '')}"
        else:
            self.question_label.text = "No more questions!"
            self.tip_label.text = ""
            self.response_label.text = ""
