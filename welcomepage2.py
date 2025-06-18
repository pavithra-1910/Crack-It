from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Ellipse, Color


class welcome2(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (1,1,1,1)
        Window.size = (350, 640)
    def on_enter(self):
        self.layout = FloatLayout()
        self.labe=Label(text="[b][color=#0000FFCC]Crack[/color][color=#FF4500]it![/color][b]",
                        font_size='30sp',
                        markup=True,
                        size_hint=(None,None),
                        pos_hint={"center_x":0.5,"center_y":0.89})
        self.layout.add_widget(self.labe)
        self.img=Image(source="wp2.webp",
                       size_hint=(None,None),
                       size=(250,250),
                       pos_hint={'center_x':0.5,'center_y':0.68})
        self.layout.add_widget(self.img)
        self.tit=Label(text="[b][color=#0000FFCC]KNOW YOUR LEVEL[/color][/b]",
                       font_size='19sp',
                       markup=True,
                       size_hint=(None,None),
                       pos_hint={'center_x':0.5,'center_y':0.50})
        self.layout.add_widget(self.tit)
        t1="""  Unlock your true potential with Crack It's level 
    assessment feature. Quickly assess your 
skills and gain access to personalized learning
    paths designed to match your proficiency."""
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
            Color(0.5, 0, 0.5, 1)  # Set color to purple
            self.circle = Ellipse(pos=self.but.pos, size=self.but.size)

        # Bind the circle to update when the button's position or size changes
        self.but.bind(pos=self.update_circle, size=self.update_circle)
        self.layout.add_widget(self.but)
        self.st1=Image(
            source="st2.png",
            size_hint=(None, None),
            size=(70, 150),
            pos_hint={'center_x': 0.5, 'center_y': 0.2}

        )
        self.layout.add_widget(self.st1)
        self.back=Label(
            text="Back",
            size_hint=(None,None),
            font_size="15sp",
            color=(0.5,0.5,0.5,1),
            pos_hint={'left':0.95,'top':0.15}
        )
        self.back.bind(on_touch_down=self.back_to_welcome1)
        self.layout.add_widget(self.back)

        self.add_widget(self.layout)

    def update_circle(self, *args):
        self.circle.pos = self.but.pos
        self.circle.size = self.but.size
        self.but.bind(on_press=self.on_button_press)

    def on_button_press(self, widget,*args):
        self.manager.current='welcome3'

    def back_to_welcome1(self,widget,touch):
        if self.back.collide_point(*touch.pos):
            self.manager.current = 'welcome1'
