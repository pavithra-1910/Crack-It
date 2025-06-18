from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
import os
import requests

class splashscreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (350, 640)

        self.layout = FloatLayout()

        self.text = Label(
            text="[b][color=#0000FFCC]Crack[/color][color=#FF4500]it![/color][/b]",
            font_size='30sp',
            markup=True,
            opacity=0,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.layout.add_widget(self.text)
        self.add_widget(self.layout)

        animate = Animation(opacity=1, duration=3)
        animate.bind(on_complete=self.check_auto_login)
        animate.start(self.text)

        Clock.schedule_once(self.check_auto_login, 10)

    def check_auto_login(self, *args):
        if os.path.exists("user_token.txt"):
            with open("user_token.txt", "r") as f:
                id_token = f.readline().strip()
                refresh_token = f.readline().strip()
            self.verify_token(id_token, refresh_token)
        else:
            self.manager.current = 'welcome1'

    def verify_token(self, id_token, refresh_token):
        api_key = 'AIzaSyAG0rlXIgjX87PUwaI6L6XhXfME2W-W9GI'
        url = f'https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={api_key}'
        data = {"idToken": id_token}

        response = requests.post(url, json=data)
        if response.status_code == 200:
            user_email = response.json()['users'][0]['email']
            self.switch_to_home(user_email)
        else:
            self.refresh_token(refresh_token)

    def refresh_token(self, refresh_token):
        api_key = 'AIzaSyAG0rlXIgjX87PUwaI6L6XhXfME2W-W9GI'
        url = f'https://securetoken.googleapis.com/v1/token?key={api_key}'
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }

        response = requests.post(url, data=data)
        if response.status_code == 200:
            result = response.json()
            id_token = result['id_token']
            refresh_token = result['refresh_token']
            with open("user_token.txt", "w") as f:
                f.write(id_token + "\n")
                f.write(refresh_token)
            self.verify_token(id_token, refresh_token)
        else:
            self.manager.current = 'welcome1'

    def switch_to_home(self, user_email):
        home_screen = self.manager.get_screen('homepage')
        home_screen.set_user_email(user_email)
        self.manager.current = 'homepage'
