from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.navigationdrawer import MDNavigationDrawer

class MenuDrawer(MDNavigationDrawer):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.width = 250
        self.md_bg_color = (0, 0, 1, 0.8)
        self.screen_manager = screen_manager  # Store reference to ScreenManager

        # Create the menu layout
        menu_layout = MDBoxLayout(orientation='vertical', padding='10dp', spacing='10dp', size_hint_y=None)
        menu_layout.bind(minimum_height=menu_layout.setter('height'))

        # Add menu items with navigation
        self.add_menu_item(menu_layout, "Home", "homepage")
        self.add_menu_item(menu_layout, "ToDo List", "todo")
        self.add_menu_item(menu_layout, "Job Portal", "jobportal")
        self.add_menu_item(menu_layout, "Practice Section", "practice_section")
        self.add_menu_item(menu_layout, "Interview Section", "interview_section")
        self.add_menu_item(menu_layout, "Settings", "setting")
        self.add_menu_item(menu_layout, "About", "about")


        # Add the layout to a ScrollView for scrolling
        scroll_view = ScrollView()
        scroll_view.add_widget(menu_layout)
        self.add_widget(scroll_view)

    def add_menu_item(self, layout, text, screen_name):
        item_button = MDFlatButton(
            text=text,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H6"
        )
        item_button.bind(on_release=lambda instance: self.navigate_to(screen_name))
        layout.add_widget(item_button)

    def navigate_to(self, screen_name):
        """Switch screen when a menu item is clicked"""
        if screen_name in self.screen_manager.screen_names:
            self.screen_manager.current = screen_name
            self.set_state("close")  # Close the menu after navigation
