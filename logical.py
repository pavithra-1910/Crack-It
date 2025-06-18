from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.metrics import dp
from kivymd.uix.button import MDIconButton
from kivymd.app import MDApp

class Logical(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Header with menu icon and label
        header_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))

        # Back button
        back_button = MDIconButton(icon="arrow-left", size_hint=(None, None), size=(dp(40), dp(40)),
                                   pos_hint={'center_y': 0.5}, theme_text_color="Custom", text_color=(0, 0, 1, 1))
        back_button.bind(on_press=self.go_back)

        # Practice Section label
        header_label = MDLabel(text="Logical Reasoning", font_style="H5", halign="center",
                               size_hint=(None, None), width=dp(200), theme_text_color="Custom",
                               text_color=(0, 0, 1, 1), bold=True, pos_hint={'center_y': 0.5})

        # Spacer for layout balance
        spacer_left = MDBoxLayout(size_hint_x=None, width=dp(1))
        spacer_right = MDBoxLayout(size_hint_x=None, width=dp(10))

        # Adding widgets to header
        header_layout.add_widget(spacer_left)
        header_layout.add_widget(back_button)
        header_layout.add_widget(header_label)
        header_layout.add_widget(spacer_right)

        layout.add_widget(header_layout)

        # ScrollView
        scroll = ScrollView()
        scroll.add_widget(layout)
        self.add_widget(scroll)

        # Logical Reasoning Cards
        self.create_card(layout, "Puzzles", "puzzle.webp")
        self.create_card(layout, "Seating Arrangement", "seating.png")
        self.create_card(layout, "Blood Relation", "blood.png")
        self.create_card(layout, "Syllogism", "syllogism.png")
        self.create_card(layout, "Coding-      Decoding", "coding.png")
        self.create_card(layout, "Statement & Conclusion", "statement.png")
        self.create_card(layout, "Data Sufficiency", "data.png")

    def create_card(self, parent_layout, text, image_source):
        card = MDCard(orientation='vertical', size_hint=(None, None), size=(390, 150), padding=dp(10),
                      md_bg_color=(0, 0, 1, 0.8), radius=[10, 40, 10, 40], pos_hint={'center_x': 0.5})
        card.bind(on_release=lambda instance: self.load_practice_screen(text))

        content_layout = MDBoxLayout(orientation='horizontal', size_hint=(1, 1), padding=(10, 0))

        label = MDLabel(text=text, theme_text_color="Custom", text_color=(1, 1, 1, 1),
                        halign='left', font_style="H6", size_hint=(0.5, 1))

        image = Image(source=image_source, size_hint=(None, None), size=(180, 160), pos_hint={'center_y': 0.5})

        content_layout.add_widget(label)
        content_layout.add_widget(image)

        card.add_widget(content_layout)
        parent_layout.add_widget(card)

    def go_back(self, instance):
        self.manager.current = "practice_section"  # Switch back to home screen

    def load_practice_screen(self, category):
        from queations import Queations
        app = MDApp.get_running_app()

        # Ensure category string is in the correct case as per the mapping
        category = category.strip()  # Remove leading/trailing whitespaces if any

        # Create screen name with the correct formatting
        screen_name = f"{category.lower().replace(' ', '_')}_screen"

        if screen_name not in app.root.screen_names:
            screen = Queations(name=screen_name, category=category)
            app.root.add_widget(screen)

        app.root.current = screen_name


