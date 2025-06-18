from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.metrics import dp
from kivymd.uix.button import MDIconButton
from kivymd.uix.screen import MDScreen
from menu import MenuDrawer
from kivy.properties import ObjectProperty


class Practice(MDScreen):
    screen_manager = ObjectProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_drawer = MenuDrawer(screen_manager=self.screen_manager)
        self.menu_drawer.set_state("close")  # Ensure the menu starts as closed

        self.menu_drawer.pos_hint = {"x": 0}
        layout = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Header with menu icon and label
        header_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))

        # Menu button with blue color, positioned to the left
        menu_button = MDIconButton(icon="menu", size_hint=(None, None), size=(dp(40), dp(40)),
                                   pos_hint={'center_y': 0.5}, theme_text_color="Custom", text_color=(0, 0, 1, 1))
        menu_button.bind(on_press=self.open_menu)

        # Practice Section label with bold text and blue color
        header_label = MDLabel(text="Practice Section", font_style="H5", halign="center",
                               size_hint=(None, None), width=dp(200), theme_text_color="Custom",
                               text_color=(0, 0, 1, 1), bold=True, pos_hint={'center_y': 0.5})

        # Spacer to balance the layout
        spacer_left = MDBoxLayout(size_hint_x=None, width=dp(1))  # Spacer to push the menu icon left
        spacer_right = MDBoxLayout(size_hint_x=None, width=dp(10))

        # Adding the widgets to the header layout
        header_layout.add_widget(spacer_left)  # Spacer before menu icon
        header_layout.add_widget(menu_button)
        header_layout.add_widget(header_label)
        header_layout.add_widget(spacer_right)  # Spacer after the label

        layout.add_widget(header_layout)

        scroll = ScrollView()
        scroll.add_widget(layout)
        self.add_widget(scroll)

        # Verbal Ability Card
        card1 = MDCard(orientation='vertical', size_hint=(None, None), size=(390, 150), padding=dp(10),
                       md_bg_color=(0, 0, 1, 0.8), radius=[10, 40, 10, 40], pos_hint={'center_x': 0.5})

        # Layout for label and image (horizontal layout)
        content_layout1 = MDBoxLayout(orientation='horizontal', size_hint=(1, 1), padding=(10, 0))

        # Add the label to the left side
        verbal_label = MDLabel(text="Verbal Ability", theme_text_color="Custom", text_color=(1, 1, 1, 1),
                               halign='left', font_style="H6", size_hint=(0.5, 1))

        # Add the image to the right side
        verbal_image = Image(source="verbal.webp", size_hint=(None, None), size=(150, 150), pos_hint={'center_y': 0.6})

        # Add label and image to content layout
        content_layout1.add_widget(verbal_label)
        content_layout1.add_widget(verbal_image)

        # Add the content layout to the card
        card1.add_widget(content_layout1)
        card1.bind(on_release=self.go_to_verbal)
        layout.add_widget(card1)

        # Logical Reasoning Card
        card2 = MDCard(orientation='vertical', size_hint=(None, None), size=(390, 150), padding=dp(10),
                       md_bg_color=(0, 0, 1, 0.8), radius=[10, 40, 10, 40], pos_hint={'center_x': 0.5})

        content_layout2 = MDBoxLayout(orientation='horizontal', size_hint=(1, 1), padding=(10, 0))

        # Add the label to the left side
        logical_label = MDLabel(text="Logical Reasoning", theme_text_color="Custom", text_color=(1, 1, 1, 1),
                               halign='left', font_style="H6", size_hint=(0.5, 1))

        # Add the image to the right side
        logical_image = Image(source="logical.webp", size_hint=(None, None), size=(150, 150), pos_hint={'center_y': 0.5})

        # Add label and image to content layout
        content_layout2.add_widget(logical_label)
        content_layout2.add_widget(logical_image)

        # Add the content layout to the card
        card2.add_widget(content_layout2)
        card2.bind(on_release=self.go_to_logical_practice)

        layout.add_widget(card2)

        # Quantitative Aptitude Card
        card3 = MDCard(orientation='vertical', size_hint=(None, None), size=(390, 150), padding=dp(10),
                       md_bg_color=(0, 0, 1, 0.8), radius=[10, 40, 10, 40], pos_hint={'center_x': 0.5})

        # Layout for label and image (horizontal layout)
        content_layout3 = MDBoxLayout(orientation='horizontal', size_hint=(1, 1), padding=(10, 0))

        # Add the label to the left side
        quant_label = MDLabel(text="Quantitative Aptitude", theme_text_color="Custom", text_color=(1, 1, 1, 1),
                               halign='left', font_style="H6", size_hint=(0.5, 1))

        # Add the image to the right side
        quant_image = Image(source="quants.webp", size_hint=(None, None), size=(150, 150), pos_hint={'center_y': 0.5})

        # Add label and image to content layout
        content_layout3.add_widget(quant_label)
        content_layout3.add_widget(quant_image)

        # Add the content layout to the card
        card3.add_widget(content_layout3)
        card3.bind(on_release=self.go_to_quants)

        layout.add_widget(card3)

        # Technical Questions Card
        card4 = MDCard(orientation='vertical', size_hint=(None, None), size=(390, 150), padding=dp(10),
                       md_bg_color=(0, 0, 1, 0.8), radius=[10, 40, 10, 40], pos_hint={'center_x': 0.5})

        # Layout for label and image (horizontal layout)
        content_layout4 = MDBoxLayout(orientation='horizontal', size_hint=(1, 1), padding=(10, 0))

        # Add the label to the left side
        tech_label = MDLabel(text="Technical Questions", theme_text_color="Custom", text_color=(1, 1, 1, 1),
                               halign='left', font_style="H6", size_hint=(0.5, 1))

        # Add the image to the right side
        tech_image = Image(source="technical.webp", size_hint=(None, None), size=(170, 170), pos_hint={'center_y': 0.5})

        # Add label and image to content layout
        content_layout4.add_widget(tech_label)
        content_layout4.add_widget(tech_image)

        # Add the content layout to the card
        card4.add_widget(content_layout4)
        card4.bind(on_release=self.go_to_technical_practice)

        layout.add_widget(card4)

        # Company-Specific Practice Card
        card5 = MDCard(orientation='vertical', size_hint=(None, None), size=(390, 150), padding=dp(10),
                       md_bg_color=(0, 0, 1, 0.8), radius=[10, 40, 10, 40], pos_hint={'center_x': 0.5})

        # Layout for label and image (horizontal layout)
        content_layout5 = MDBoxLayout(orientation='horizontal', size_hint=(1, 1), padding=(10, 0))

        # Add the label to the left side
        company_label = MDLabel(text="Company-Specific Practice", theme_text_color="Custom", text_color=(1, 1, 1, 1),
                               halign='left', font_style="H6", size_hint=(0.5, 1))

        # Add the image to the right side
        company_image = Image(source="company.webp", size_hint=(None, None), size=(140, 150), pos_hint={'center_y': 0.4})

        # Add label and image to content layout
        content_layout5.add_widget(company_label)
        content_layout5.add_widget(company_image)

        # Add the content layout to the card
        card5.add_widget(content_layout5)
        card5.bind(on_release=self.go_to_company_p)
        layout.add_widget(card5)

        self.add_widget(self.menu_drawer)

    def open_menu(self, instance):
        if self.menu_drawer.state == "open":
            self.menu_drawer.set_state("close")  # Close if it's already open
        else:
            self.menu_drawer.set_state("open")  # Open if it's closed

    def go_to_logical_practice(self, instance):
        self.manager.current = 'logical_practice'

    def go_to_verbal(self, instance):
        self.manager.current = 'verbal'

    def go_to_quants(self, instance):
        self.manager.current = 'quants'

    def go_to_technical_practice(self, instance):
        self.manager.current = 'technical_p'

    def go_to_company_p(self, instance):
        self.manager.current = 'company_p'
