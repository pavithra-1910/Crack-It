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

cred = credentials.Certificate("firebase-admin.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://crackit-8371d-default-rtdb.firebaseio.com'
    })


ref = db.reference('group_discussion')
gd_data = ref.get()
gd_data = gd_data if gd_data else {}

class GroupDiscussionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0, 0, 1, 0.8)
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
            text="Group Discussion",
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
            source="n2.jpg",
            pos_hint={"center_x": 0.5},
            height="150dp",
            radius=[20]
        )
        card.add_widget(fit_image)

        self.topic_label = MDLabel(
            text="Topic will appear here",
            font_style="H6",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None
        )
        card.add_widget(self.topic_label)

        scroll_view = ScrollView()
        self.bullet_point_label = MDLabel(
            text="Content will appear here",
            font_style="Body1",
            theme_text_color="Custom",
            text_color=(0, 0, 1, 1),
            halign="left",
            size_hint_y=None
        )
        scroll_view.add_widget(self.bullet_point_label)
        card.add_widget(scroll_view)

        next_button = MDRaisedButton(
            text="Next",
            size_hint_y=None,
            height="50dp",
            width="200dp",
            pos_hint={"center_x": 0.5},
            on_press=self.show_topic
        )
        card.add_widget(next_button)

        main_layout.add_widget(card)
        self.add_widget(main_layout)

        self.current_state = 0

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def back_button(self, instance):
        self.manager.current = "interview_section"  # change if needed

    def show_topic(self, instance):
        if self.current_state == 0:
            self.show_intro()
            self.current_state = 1
        elif self.current_state == 1:
            self.show_gd_tips()
            self.current_state = 2
        elif self.current_state == 2:
            self.show_important_topics()
            self.current_state = 3
        else:
            self.topic_label.text = "No more content!"
            self.bullet_point_label.text = ""

    def show_intro(self):
        self.topic_label.text = "What is Group Discussion (GD)?"
        self.bullet_point_label.text = gd_data.get('what_is_gd', '')

    def show_gd_tips(self):
        self.topic_label.text = "GD Tips"
        bullet_points = ""
        for tip in gd_data.get('tips', []):
            bullet_points += f"[b]{tip['title']}[/b]\n"
            for point in tip.get('points', []):
                bullet_points += f"- {point}\n"
            bullet_points += "\n"
        self.bullet_point_label.text = bullet_points

    def show_important_topics(self):
        self.topic_label.text = "Important GD Topics"
        topics = "\n".join([f"- {topic}" for topic in gd_data.get('important_topics', [])])
        self.bullet_point_label.text = topics