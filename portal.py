from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
import webbrowser
import threading

Window.size = (350, 640)

from firebase_admin import credentials, initialize_app, firestore

try:
    cred = credentials.Certificate("firebase-admin.json")
    initialize_app(cred)
except:
    pass

db = firestore.client()

class JobPortalScreen(MDScreen):
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
            text="Job Portal",
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

        self.scroll = ScrollView(
            size_hint=(1, None),
            size=(Window.width, Window.height - dp(50)),
            pos_hint={"top": 0.92},
        )

        self.jobs_container = MDBoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            size_hint_y=None,
        )
        self.jobs_container.bind(minimum_height=self.jobs_container.setter('height'))

        self.scroll.add_widget(self.jobs_container)
        self.add_widget(self.scroll)

        threading.Thread(target=self.load_jobs, daemon=True).start()

    def create_job_card(self, title, company, location, description, apply_link):
        card = MDCard(
            orientation="vertical",
            size_hint_x=1,
            size_hint_y=None,
            height=dp(260),
            padding=dp(10),
            ripple_behavior=True,
        )

        title_label = MDLabel(
            text=f"[b]{title}[/b]",
            markup=True,
            font_style="H5",
            theme_text_color="Custom",
            text_color=(0, 0, 1, 0.8),
        )

        company_label = MDLabel(
            text=f"Company: {company}",
            theme_text_color="Secondary",
            text_color=(0, 0, 0, 1)  # Black color
        )

        location_label = MDLabel(
            text=f"Location: {location}",
            theme_text_color="Secondary",
            text_color=(0, 0, 0, 1)  # Black color
        )

        description_label = MDLabel(
            text=description,
            theme_text_color="Secondary",
            text_color=(0, 0, 0, 1),  # Black color
            size_hint_y=None,
            height=dp(70)
        )

        card.add_widget(title_label)
        card.add_widget(company_label)
        card.add_widget(location_label)
        card.add_widget(description_label)

        if apply_link:
            apply_button = MDRaisedButton(
                text="Apply Now",
                size_hint=(None, None),
                size=("120dp", "40dp"),
                pos_hint={"center_x": 0.5},
                on_release=lambda x: self.open_link(apply_link)
            )
            card.add_widget(apply_button)

        return card

    def load_jobs(self):
        jobs_ref = db.collection('jobs')
        docs = jobs_ref.stream()
        jobs = [doc.to_dict() for doc in docs]
        Clock.schedule_once(lambda dt: self.update_ui_with_jobs(jobs))

    def update_ui_with_jobs(self, jobs):
        self.jobs_container.clear_widgets()

        if len(jobs) == 0:
            no_jobs_label = MDLabel(
                text="No Jobs Available",
                font_style="H6",
                halign="center",
                theme_text_color="Custom",
                text_color=(1, 0, 0, 1),
                size_hint_y=None,
                height=50,
            )
            self.jobs_container.add_widget(no_jobs_label)

        for job in jobs:
            title = job.get('title', 'No Title')
            company = job.get('company', 'No Company')
            location = job.get('location', 'No Location')
            description = job.get('description', 'No Description')
            apply_link = job.get('apply_link', None)

            card = self.create_job_card(title, company, location, description, apply_link)
            self.jobs_container.add_widget(card)

    def open_link(self, link):
        webbrowser.open(link)

    def go_back(self, instance):
        self.manager.current="homepage"

