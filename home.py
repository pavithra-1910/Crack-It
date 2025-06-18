import firebase_admin
from firebase_admin import credentials, db
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle
from menu import MenuDrawer

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-admin.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://crackit-8371d-default-rtdb.firebaseio.com/'
    })
def extract_regno(email):
    return email.split('@')[0]

class HomeScreen(Screen):

    def __init__(self,screen_manager, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (0,0,1,0.8)
        Window.size = (350, 640)
        self.user_email = None
        self.username_label = None


        self.layout = MDFloatLayout()
        self.menu_drawer = MenuDrawer(screen_manager)
        self.menu_drawer.set_state("close")
        self.menu_drawer.pos_hint = {"x": 0}



        scroll_view = ScrollView(size_hint=(1, 0.92), pos_hint={'x': 0, 'y': 0.08}, scroll_x=0)


        main_box = MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=20)
        main_box.bind(minimum_height=main_box.setter('height'))


        rectangle_card = MDCard(
            orientation='vertical',
            size_hint=(None, None),
            width=437,
            height=400,
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            radius=[0, 0, 30, 30],  # Rounded corners
            md_bg_color=(0, 0, 1, 0.7)
        )


        header = MDFloatLayout(size_hint=(1, None), height=100)


        notification_icon = MDIconButton(
            icon="bell-outline",
            pos_hint={"center_y": 0.6, 'right': 1},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)  # Set to white color
        )
        notification_icon.bind(on_press=self.open_notification_screen)

        menu = MDIconButton(
            icon="menu",
            pos_hint={'x': 0, 'top': 1},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        menu.bind(on_press=self.open_menu)

        self.username_label = MDLabel(
            text="",
            pos_hint={"center_x": 0.54, "y": -0.3},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size='40sp',
            bold=True
        )


        header.add_widget(notification_icon)
        header.add_widget(menu)
        header.add_widget(self.username_label)


        rectangle_card.add_widget(header)


        image = Image(
            source="learn5.webp",
            width=437,
            pos_hint={'center_x': 0.5, 'y': -0.5}
        )
        rectangle_card.add_widget(image)


        main_box.add_widget(rectangle_card)


        mcq_card = MDCard(
            orientation='vertical',
            size_hint=(None, None),
            width=400,
            height=130,
            pos_hint={'center_x': 0.5},
            radius=[30, 30, 30, 30],
            md_bg_color=(0, 0, 1, 0.8),
        )

        interview_card = MDCard(
            orientation='vertical',
            size_hint=(None, None),
            width=400,
            height=130,
            pos_hint={'center_x': 0.5},
            radius=[30, 30, 30, 30],
            md_bg_color=(0, 0, 1, 0.8),
        )

        mcq_layout = MDBoxLayout(orientation='horizontal', padding=10)

        mcq_image = Image(
            source="practice.webp",
            size_hint=(None, None),
            width=150,
            height=150
        )

        mcq_label = MDLabel(
            text="Practice Zone",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size='50dp',
            bold=True
        )

        mcq_layout.add_widget(mcq_image)
        mcq_layout.add_widget(mcq_label)

        mcq_card.add_widget(mcq_layout)
        mcq_card.bind(on_press=lambda x: setattr(self.manager, 'current', 'practice_section'))

        interview_layout = MDBoxLayout(orientation='horizontal', padding=10)


        interview_image = Image(
            source="interview.webp",
            size_hint=(None, None),
            width=120,
            height=120
        )


        interview_label = MDLabel(
            text="Interview Zone",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_size='50dp',
            bold=True
        )

        interview_layout.add_widget(interview_image)
        interview_layout.add_widget(interview_label)


        interview_card.add_widget(interview_layout)
        interview_card.bind(on_press=lambda x: setattr(self.manager, 'current', 'interview_section'))


        main_box.add_widget(mcq_card)
        main_box.add_widget(interview_card)

        scroll_view.add_widget(main_box)
        self.layout.add_widget(scroll_view)


        bottom_nav = MDBoxLayout(size_hint=(1, 0.08), pos_hint={'x': 0, 'y': 0}, spacing=60, width=437, height=10)


        with bottom_nav.canvas.before:
            Color(0, 0, 1, 0.8)
            self.rect = RoundedRectangle(size=bottom_nav.size, pos=bottom_nav.pos, radius=[30, 30, 0, 0])

        # Bind size and position updates to ensure the background resizes
        bottom_nav.bind(size=self.update_rect, pos=self.update_rect)

        # Add navigation buttons with icons
        self.home_button = MDIconButton(icon="home-outline", theme_text_color="Custom", text_color=(1, 1, 1, 1))
        self.leaderboard_button = MDIconButton(icon="checkbox-marked-outline", theme_text_color="Custom", text_color=(1, 1, 1, 1))
        self.notification_button = MDIconButton(icon="briefcase-outline", theme_text_color="Custom",
                                                text_color=(1, 1, 1, 1))
        self.profile_button = MDIconButton(icon="account-outline", theme_text_color="Custom", text_color=(1, 1, 1, 1))

        # Bind the on_press event to change icons from outline to filled when clicked
        self.home_button.bind(on_press=self.toggle_icon)
        self.leaderboard_button.bind(on_press=self.go_to_test)
        self.profile_button.bind(on_press=self.go_to_profile)
        self.notification_button.bind(on_press=self.go_to_job)


        # Add buttons to the bottom navigation bar
        bottom_nav.add_widget(self.home_button)
        bottom_nav.add_widget(self.leaderboard_button)
        bottom_nav.add_widget(self.notification_button)
        bottom_nav.add_widget(self.profile_button)

        # Add the navigation bar to the main layout
        self.layout.add_widget(bottom_nav)
        self.layout.add_widget(self.menu_drawer)

        self.add_widget(self.layout)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def toggle_icon(self, button):
        if button.icon.endswith("outline"):
            button.icon = button.icon.replace("-outline", "")  # Change to filled version
        else:
            button.icon = button.icon + "-outline"  # Change back to outline

# Firebase setup with error handling
        try:
            cred = credentials.Certificate("firebase-admin.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://crackit-8371d-default-rtdb.firebaseio.com/'
            })
        except Exception as e:
            print(f"Error initializing Firebase: {e}")

    def set_user_email(self, email):
        self.user_email = email
        self.load_username()

    def load_username(self):
        if self.user_email:
            regno = extract_regno(self.user_email)

            # Fetch user data from Firebase database using regno
            ref = db.reference(f'user/{regno}/username/name')

            try:
                username = ref.get()

                if username:
                    self.username_label.text = f'Hi ! \n{username}'
                else:
                    self.username_label.text = f'Hi!'
            except Exception as e:
                print(f"Error loading username: {e}")
                self.username_label.text = "Hi!"

    def open_menu(self, instance):
        if self.menu_drawer.state == "open":
            self.menu_drawer.set_state("close")  # Close if it's already open
        else:
            self.menu_drawer.set_state("open")  # Open if it's closed

    def go_to_profile(self, instance):
        self.toggle_icon(instance)  # Change icon style
        profile_screen = self.manager.get_screen('profile')
        profile_screen.email = self.user_email  # Directly pass the email to the profile screen
        profile_screen.fetch_user_data()  # Ensure the user data is fetched
        self.manager.current = 'profile'

    def open_notification_screen(self, instance):
        self.manager.current = 'notifications'

    def go_to_job(self,instance):
        self.manager.current="jobportal"

    def go_to_test(self,instance):
        self.manager.current="week"
