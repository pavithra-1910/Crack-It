from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class welcome3(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (1,1,1,1)
        Window.size = (350, 640)

        self.layout = FloatLayout()
        self.labe=Label(text="[b][color=#0000FFCC]Crack[/color][color=#FF4500]it![/color][b]",
                        font_size='30sp',
                        markup=True,
                        size_hint=(None,None),
                        pos_hint={"center_x":0.5,"center_y":0.89})
        self.layout.add_widget(self.labe)
        self.img=Image(source="wp3.webp",
                       size_hint=(None,None),
                       size=(250,250),
                       pos_hint={'center_x':0.5,'center_y':0.68})
        self.layout.add_widget(self.img)
        self.tit=Label(text="[b][color=#0000FFCC]GROW YOUR CAREER[/color][/b]",
                       font_size='19sp',
                       markup=True,
                       size_hint=(None,None),
                       pos_hint={'center_x':0.5,'center_y':0.50})
        self.layout.add_widget(self.tit)
        t1="""         Fuel your career growth with Crack 
      It's comprehensive resources. Access 
   industry-relevant courses, expert insights.
job placement support tailored to your ambitions."""
        self.titl = Label(text=t1,
                         font_size='15sp',
                         color=(0.5,0.5,0.5,1),
                         size_hint=(None, None),
                         pos_hint={'center_x': 0.5, 'center_y': 0.39})
        self.layout.add_widget(self.titl)
        self.but=Button(
            text="[b]Get Started[b]",
            font_size=15,
            size=(150,50),
            markup=True,
            background_color=(0,0,1,0.8),
            size_hint=(None,None),
            pos_hint={'right':0.95,'top':0.13}
        )
        self.but.bind(on_press=self.switch_to_login)

        self.layout.add_widget(self.but)

        self.st1=Image(
            source="st3.png",
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
        self.back.bind(on_touch_down=self.back_to_welcome2)
        self.layout.add_widget(self.back)


        self.add_widget(self.layout)

    def back_to_welcome2(self, widget, touch):
        if self.back.collide_point(*touch.pos):
            self.manager.current = "welcome2"

    def switch_to_login(self, widget):
        self.manager.current="login"
