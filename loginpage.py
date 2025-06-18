
import requests
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivymd.uix.textfield import MDTextField
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDIconButton
from kivy.uix.popup import Popup

class LoginPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (350, 640)

        self.layout = FloatLayout()

        # Welcome label
        self.label = Label(
            text="[b]Welcome To[/b]",
            font_size='27sp',
            markup=True,
            halign="center",
            pos_hint={"center_y": 0.9},
            color=(0,0,1,0.8),
            font_name='verdana'
        )
        self.layout.add_widget(self.label)

        self.text = Label(
            text="[b][color=#0000FFCC]Crack[/color][color=#FF4500]it![/color][b]",
            font_size='25sp',
            markup=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        self.layout.add_widget(self.text)

        self.img = Image(
            source="login.webp",
            size_hint=(None, None),
            size=(400, 400),
            pos_hint={'center_x': 0.5, 'center_y': 0.64}
        )
        self.layout.add_widget(self.img)

        # Email Input
        self.email_input = MDTextField(
            hint_text="Enter student mail ID",
            size_hint=(None, None),
            size=(350, 40),
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            multiline=False,
            mode="rectangle",
            max_text_length=22
        )
        self.layout.add_widget(self.email_input)

        # Password Input
        self.password_input = MDTextField(
            hint_text="Enter Your password",
            size_hint=(None, None),
            size=(350, 40),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            multiline=False,
            password=True,
            mode="rectangle",
            max_text_length=20
        )
        self.layout.add_widget(self.password_input)
        self.icon_button = MDIconButton(
            icon="eye-off",
            pos_hint={"center_x": 0.85, "center_y": 0.3}
        )
        self.icon_button.bind(on_release=self.toggle_password_visibility)
        self.layout.add_widget(self.icon_button)

        # Forget Password Label (Clickable)
        self.forget_password_label = MDFlatButton(
            text="Forget Password?",
            pos_hint={"center_x": 0.73, "center_y": 0.23},
            text_color=(1, 0, 0, 1),
            on_release=self.send_reset_email
        )
        self.layout.add_widget(self.forget_password_label)

        # Login Button
        self.login = MDRaisedButton(
            text="Login",
            size_hint=(None, None),
            size=(140, 50),
            md_bg_color=(1, 0.5, 0, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.15}
        )
        self.layout.add_widget(self.login)
        self.login.bind(on_press=self.login_with_firebase)

        self.add_widget(self.layout)




    def toggle_password_visibility(self,instance):
        if self.password_input.password:
            self.password_input.password = False
            self.icon_button.icon = "eye"
        else:
            self.password_input.password = True
            self.icon_button.icon = "eye-off"

    def login_with_firebase(self, instance):
        email = self.email_input.text
        password = self.password_input.text

        if not email.endswith('@sastra.ac.in'):
            self.show_popup("Enter a valid SASTRA email ID")
            return

        # Firebase Sign-In API endpoint
        api_key = 'AIzaSyAG0rlXIgjX87PUwaI6L6XhXfME2W-W9GI'  # Get from Firebase project settings
        url = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}'

        data = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            result = response.json()
            user_email = result['email']
            id_token = result['idToken']
            refresh_token = result['refreshToken']

            # 🔐 Save tokens for future auto-login
            with open("user_token.txt", "w") as f:
                f.write(id_token + "\n")
                f.write(refresh_token)

            self.show_popup_login("Login successfully!")
            Clock.schedule_once(lambda dt: self.switch_to_home(user_email), 2)

    def send_reset_email(self, instance):
        email = self.email_input.text
        if email:
            api_key = 'AIzaSyAG0rlXIgjX87PUwaI6L6XhXfME2W-W9GI'  # Get from Firebase project settings
            url = f'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}'
            data = {
                "requestType": "PASSWORD_RESET",
                "email": email
            }
            response = requests.post(url, json=data)

            if response.status_code == 200:
                self.show_popup("Password reset email sent.")
            else:
                self.show_popup("Failed to send password reset email.")
        else:
            self.show_popup("Please enter your email first.")

    def show_popup(self, message):
        popup = Popup(title='Attention!', content=Label(text=message), size_hint=(0.6, 0.2), background_color=(1, 1, 1, 0.3))
        popup.open()

    def switch_to_home(self, user_email):
        home_screen = self.manager.get_screen('homepage')  # Get HomeScreen instance
        home_screen.set_user_email(user_email)  # Set email to HomeScreen
        self.manager.current = 'homepage'  # Switch to the home screen

    def show_popup_login(self, message):
        popup = Popup(title='', content=Label(text=message), size_hint=(0.6, 0.1), background_color=(1, 1, 1, 0.3))
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)



