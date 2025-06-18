from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Rotate
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel


class RotatableCard(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rotation_y = 0
        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate(
                angle=self.rotation_y,
                axis=(0, 1, 0),
                origin=self.center
            )
            PopMatrix()
        self.bind(pos=self.update_origin, size=self.update_origin)

    def on_rotation_y(self, instance, value):
        self.rot.angle = value

    def update_origin(self, *args):
        self.rot.origin = self.center


class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0, 0, 1, 0.8)  # White background
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Widget(size_hint_y=None, height=40))

        header = MDBoxLayout(size_hint_y=None, height=50, padding=10)

        back_button = MDIconButton(
            icon="arrow-left",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=("50dp", "50dp"),
            pos_hint={"center_y": 0.45},
            on_release=self.go_back
        )

        title = MDLabel(
            text="About",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H6",
            size_hint_x=None,
            width="200dp",
            halign="left",
            valign="middle"
        )

        header.add_widget(back_button)
        header.add_widget(title)
        layout.add_widget(header)

        self.about_card = RotatableCard(
            size_hint=(None, None),
            size=("310dp", "550dp"),
            pos_hint={"center_x": 0.5},
            padding=20,
            radius=[30, 30, 30, 30],
            md_bg_color=(1, 1, 1, 1),
            elevation=6
        )
        # Correct way to bind the flip card event
        self.about_card.bind(on_release=self.flip_card)

        card_content = MDBoxLayout(orientation='vertical', padding=20, spacing=15)

        logo = Image(
            source="logoofcrackit.png",
            size_hint_y=None,
            height="180dp",
            allow_stretch=True,
            keep_ratio=True,
            pos_hint={"center_x": 0.5}
        )

        description1 = MDLabel(
            text="CrackIt is your ultimate companion for mastering challenging topics and acing exams.",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 1, 0.8),
            font_style="Body1"
        )

        description2 = MDLabel(
            text="Prepare for interviews with practice sections, tips, and more.",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 1, 0.8),
            font_style="Body1"
        )

        version = MDLabel(
            text="Version 1.0.0",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="Subtitle1"
        )

        policy = MDLabel(
            text="Developed by SASTRA Arts & Science Students",
            halign="center",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            font_style="Caption"
        )

        card_content.add_widget(logo)
        card_content.add_widget(description1)
        card_content.add_widget(description2)
        card_content.add_widget(version)
        card_content.add_widget(policy)

        self.about_card.add_widget(card_content)
        layout.add_widget(self.about_card)

        layout.add_widget(Widget(size_hint_y=None, height=20))

        self.add_widget(layout)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def flip_card(self, *args):
        # Rotate the card and ensure it flips back when it reaches 180 degrees
        anim = Animation(rotation_y=self.about_card.rotation_y + 180, duration=0.5)
        anim.start(self.about_card)

    def go_back(self, instance):
        self.manager.current = "homepage"
