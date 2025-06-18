from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import OneLineAvatarIconListItem, IRightBodyTouch, MDList
from kivy.uix.scrollview import ScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from firebase_admin import db
import firebase_admin
from firebase_admin import credentials


# Firebase initialization
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-admin.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://crackit-8371d-default-rtdb.firebaseio.com/'
    })

class DeleteButton(IRightBodyTouch, MDIconButton):
    pass

class EditButton(IRightBodyTouch, MDIconButton):
    pass

class TodoPage(Screen):
    def __init__(self, email="", **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.regno = self.extract_regno(email)
        self.dialog = None
        self.editing_key = None

        self.layout = MDBoxLayout(orientation="vertical", padding=10, spacing=10)
        self.layout.md_bg_color = (0.95, 0.95, 1, 1)

        self.build_ui()
        self.add_widget(self.layout)
        self.fetch_todo_items()

    def extract_regno(self, email):
        return email.split('@')[0] if email else "Unknown"

    def go_back(self, instance):
        self.manager.current = 'homepage'

    def build_ui(self):
        # Top bar
        top_bar = MDBoxLayout(
            size_hint=(1, None),
            height=60,
            padding=10,
            spacing=10
        )
        back_btn = MDIconButton(
            icon="arrow-left",
            on_release=self.go_back,
            theme_text_color="Custom",
            text_color=(0,0,1,0.8)
        )
        title = MDLabel(
            text="To-Do List",
            font_style="H5",  # Optional: use a predefined font style like 'H6'
            bold=True,
            theme_text_color="Custom",
            text_color=(0,0,1,0.8),
            pos_hint={'center_x': 0.2}
        )

        top_bar.add_widget(back_btn)
        top_bar.add_widget(title)

        # Input and add button
        input_layout = MDBoxLayout(size_hint_y=None, height=60, spacing=10)
        self.task_input = MDTextField(
            hint_text="Add a new task",
            mode="rectangle",
            size_hint_x=0.7
        )
        add_button = MDRaisedButton(
            text="Add",
            size_hint_x=0.2,
            md_bg_color=(0, 0, 1, 1),
            on_release=self.add_task
        )
        input_layout.add_widget(self.task_input)
        input_layout.add_widget(add_button)

        # Scroll list
        scroll = ScrollView()
        self.todo_list = MDList()
        scroll.add_widget(self.todo_list)

        self.layout.add_widget(top_bar)
        self.layout.add_widget(input_layout)
        self.layout.add_widget(scroll)

    def fetch_todo_items(self):
        try:
            self.todo_list.clear_widgets()
            ref = db.reference(f"user/{self.regno}/username/todo")
            tasks = ref.get()
            if tasks:
                for key, task in tasks.items():
                    self.todo_list.add_widget(self.create_task_item(key, task))
        except Exception as e:
            print("Error loading tasks:", e)

    def create_task_item(self, key, task_text):
        item_layout = MDBoxLayout(
            orientation='horizontal',
            padding=(10, 5),
            spacing=10,
            size_hint_y=None,
            height=50
        )

        task_label = MDLabel(
            text=task_text,
            halign='left',
            valign='middle',
            size_hint_x=0.8,
            theme_text_color="Primary"
        )

        edit_button = EditButton(
            icon="pencil",
            on_release=lambda x: self.open_edit_dialog(key, task_text),
            size_hint=(None, None),
            size=(30, 30),
            pos_hint={"center_y": 0.5},
        )

        delete_button = DeleteButton(
            icon="delete",
            on_release=lambda x: self.delete_task(key),
            size_hint=(None, None),
            size=(30, 30),
            pos_hint={"center_y": 0.5},
        )

        item_layout.add_widget(task_label)
        item_layout.add_widget(edit_button)
        item_layout.add_widget(delete_button)

        return item_layout

    def add_task(self, instance):
        task = self.task_input.text.strip()
        if task:
            try:
                ref = db.reference(f"user/{self.regno}/username/todo")
                ref.push(task)
                self.task_input.text = ""
                self.fetch_todo_items()
            except Exception as e:
                print("Error adding task:", e)

    def delete_task(self, key):
        try:
            ref = db.reference(f"user/{self.regno}/username/todo/{key}")
            ref.delete()
            self.fetch_todo_items()
        except Exception as e:
            print("Error deleting task:", e)

    def open_edit_dialog(self, key, old_text):
        self.editing_key = key
        self.dialog = MDDialog(
            title="Edit Task",
            type="custom",
            content_cls=MDTextField(text=old_text, multiline=False),
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text="SAVE", on_release=self.save_edited_task)
            ],
        )
        self.dialog.open()

    def save_edited_task(self, instance):
        new_text = self.dialog.content_cls.text.strip()
        if new_text:
            try:
                ref = db.reference(f"user/{self.regno}/username/todo/{self.editing_key}")
                ref.set(new_text)
                self.fetch_todo_items()
            except Exception as e:
                print("Error updating task:", e)
        self.dialog.dismiss()
        self.editing_key = None
