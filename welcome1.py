from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Ellipse, Color
from kivy.uix.screenmanager import Screen


class welcome1(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (1,1,1,1)
        Window.size = (350, 640)

    def on_pre_enter(self):
        # Build the login screen when this screen is entered
        self.build()

    def build(self):
        self.layout = FloatLayout()
        self.labe=Label(text="[b][color=#0000FFCC]Crack[/color][color=#FF4500]it![/color][b]",
                        font_size='30sp',
                        markup=True,
                        size_hint=(None,None),
                        pos_hint={"center_x":0.5,"center_y":0.89})
        self.layout.add_widget(self.labe)
        self.img=Image(source="welcome1.webp",
                       size_hint=(None,None),
                       size=(400,400),
                       pos_hint={'center_x':0.5,'center_y':0.68})
        self.layout.add_widget(self.img)
        self.tit=Label(text="[b][[color=#0000FFCC]TRAIN THROUGH APP[/color][/b]",
                       font_size='19sp',
                       markup=True,
                       size_hint=(None,None),
                       pos_hint={'center_x':0.5,'center_y':0.50})
        self.layout.add_widget(self.tit)
        t1="""Prepare, practice, and prevail with CrackIt.
        Everything you need for placement
        success in one powerful app!"""
        self.titl = Label(text=t1,
                         font_size='15sp',
                         color=(0.5,0.5,0.5,1),
                         size_hint=(None, None),
                         pos_hint={'center_x': 0.5, 'center_y': 0.39})
        self.layout.add_widget(self.titl)
        self.but=Button(
            text="[b]>[/b]",
            font_size=30,
            size_hint=(None,None),
            size=(55,55),
            markup=True,
            background_normal='',
            background_color=(0,0,0,0),
            pos_hint={'right':0.95,'top':0.13}
        )
        with self.but.canvas.before:
            Color(0,0,1,0.8)  # Set color to purple
            self.circle = Ellipse(pos=self.but.pos, size=self.but.size)

        # Bind the circle to update when the button's position or size changes
        self.but.bind(pos=self.update_circle, size=self.update_circle)
        self.but.bind(on_press=self.on_button_press)
        self.layout.add_widget(self.but)
        self.st1=Image(
            source="st1.png",
            size_hint=(None, None),
            size=(100, 150),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}

        )
        self.layout.add_widget(self.st1)
        self.skip=Label(
            text="Skip",
            size_hint=(None,None),
            font_size="15sp",
            color=(0.5,0.5,0.5,1),
            pos_hint={'left':0.95,'top':0.15}
        )
        self.skip.bind(on_touch_down=self.switch_to_skip)

        self.layout.add_widget(self.skip)

        self.add_widget(self.layout)

    def update_circle(self, *args):
        self.circle.pos = self.but.pos
        self.circle.size = self.but.size

    def on_button_press(self, instance):
        self.manager.current='welcome2'
    def switch_to_skip(self,widget,touch):
        if self.skip.collide_point(*touch.pos):
            self.manager.current = 'login'