from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.graphics import Color, RoundedRectangle

class BaseScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (0.404, 0.055, 0.847, 1)  # Set background color
        Window.size = (350, 640)

        # Main layout for the screen
        self.layout = MDFloatLayout()

        # Create the bottom navigation bar
        bottom_nav = MDBoxLayout(size_hint=(1, 0.08), pos_hint={'x': 0, 'y': 0}, spacing=60, width=437, height=10)

        # Add a border to the BoxLayout using canvas instructions
        with bottom_nav.canvas.before:
            Color(0, 0, 1, 0.8)  # Border color (blue)
            self.rect = RoundedRectangle(size=bottom_nav.size, pos=bottom_nav.pos, radius=[30, 30, 0, 0])

        # Bind size and position updates to ensure the background resizes
        bottom_nav.bind(size=self.update_rect, pos=self.update_rect)

        # Add navigation buttons with icons
        self.home_button = MDIconButton(icon="home-outline", theme_text_color="Custom", text_color=(1, 1, 1, 1))
        self.leaderboard_button = MDIconButton(icon="magnify", theme_text_color="Custom", text_color=(1, 1, 1, 1))
        self.notification_button = MDIconButton(icon="trophy-outline", theme_text_color="Custom", text_color=(1, 1, 1, 1))
        self.profile_button = MDIconButton(icon="account-outline", theme_text_color="Custom", text_color=(1, 1, 1, 1))

        # Bind the on_press event to change icons from outline to filled when clicked
        self.home_button.bind(on_press=self.toggle_icon)
        self.notification_button.bind(on_press=self.toggle_icon)
        self.profile_button.bind(on_press=self.toggle_icon)

        # Add buttons to the bottom navigation bar
        bottom_nav.add_widget(self.home_button)
        bottom_nav.add_widget(self.leaderboard_button)
        bottom_nav.add_widget(self.notification_button)
        bottom_nav.add_widget(self.profile_button)

        # Add the navigation bar to the main layout
        self.layout.add_widget(bottom_nav)
        self.add_widget(self.layout)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def toggle_icon(self, button):
        if button.icon.endswith("outline"):
            button.icon = button.icon.replace("-outline", "")  # Change to filled version
        else:
            button.icon = button.icon + "-outline"  # Change back to outline

