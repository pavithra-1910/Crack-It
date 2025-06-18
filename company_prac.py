from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.button import MDIconButton
from kivymd.app import MDApp
import webbrowser


Window.size = (340, 650)

class Company_Prac(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))


        header_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))


        back_button = MDIconButton(icon="arrow-left", size_hint=(None, None), size=(dp(40), dp(40)),
                                   pos_hint={'center_y': 0.5}, theme_text_color="Custom", text_color=(0, 0, 1, 1))
        back_button.bind(on_press=self.go_back)


        header_label = MDLabel(text="Company Specific Practice", font_style="H5", halign="center",
                               size_hint=(None, None), width=dp(250), theme_text_color="Custom",
                               text_color=(0, 0, 1, 1), bold=True, pos_hint={'center_y': 0.5})

        spacer_left = MDBoxLayout(size_hint_x=None, width=dp(1))
        spacer_right = MDBoxLayout(size_hint_x=None, width=dp(10))

        header_layout.add_widget(spacer_left)
        header_layout.add_widget(back_button)
        header_layout.add_widget(header_label)
        header_layout.add_widget(spacer_right)

        layout.add_widget(header_layout)

        scroll = ScrollView()
        scroll.add_widget(layout)
        self.add_widget(scroll)

        self.create_card(layout, "Past Year Questions", "puzzle.webp")

    def create_card(self, parent_layout, text, image_source):
        card = MDCard(orientation='vertical', size_hint=(None, None), size=(390, 150), padding=dp(10),
                      md_bg_color=(0, 0, 1, 0.8), radius=[10, 40, 10, 40], pos_hint={'center_x': 0.5})

        content_layout = MDBoxLayout(orientation='horizontal', size_hint=(1, 1), padding=(10, 0))

        label = MDLabel(text=text, theme_text_color="Custom", text_color=(1, 1, 1, 1),
                        halign='left', font_style="H6", size_hint=(0.6, 1))

        image = Image(source=image_source, size_hint=(None, None), size=(180, 150), pos_hint={'center_y': 0.5})

        content_layout.add_widget(label)
        content_layout.add_widget(image)

        card.add_widget(content_layout)
        card.bind(on_release=self.go_to_company_queastions)
        parent_layout.add_widget(card)

    def go_back(self, instance):
        app = MDApp.get_running_app()
        app.root.current = "practice_section"

    def go_to_company_queastions(self, instance):
        url = "https://drive.google.com/drive/folders/1SkCOcAS0Kqvuz-MJkkjbFr1GSue6Ms6m"
        webbrowser.open(url)



