from kivy.config import Config

Config.set('graphics', 'width', '350')
Config.set('graphics', 'height', '640')

import firebase_admin
from firebase_admin import credentials, db

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.screen import MDScreen
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.clock import Clock
import time

# Firebase Setup
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-admin.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://crackit-8371d-default-rtdb.firebaseio.com/'
    })


class Queations(MDScreen):
    category = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.category = kwargs.get('category', 'Reading Comprehension')
        self.selected_option = None
        self.current_index = 0
        self.questions = self.load_questions_from_firebase()
        self.option_buttons = []
        self.selected_answers = []

        self.main_layout = MDBoxLayout(orientation="vertical")
        self.setup_ui()
        self.timer_enabled = False
        self.start_time = None
        self.elapsed_time = 0
        self.dialog = None
        self.ask_timer_permission()

    def load_questions_from_firebase(self):
        category_map = {
            "Reading Comprehension": "/reading_comprehension",
            "Sentence Correction": "/sentence_correction",
            "Synonyms & Antonyms": "/synonyms_antonyms",
            "Para Jumbles": "/para_jumbles",
            "Fill in the Blanks": "/fill_in_the_blank",
            "Critical Reasoning": "/critical_reasoning",
            "Puzzles":"/puzzles",
            "Seating Arrangement":"/seating_arrangements",
            "Blood Relation":"/blood_relation",
            "Syllogism":"/syllogism",
            "Coding Decoding":"/coding_decoding",
            "Statement & conclusion":"/statement_conclusion",
            "Data Sufficiency":"/data_sufficiency",
            "Number System & Arithmetic":"/number_system_arithmetic",
            "Algebra & Equations":"/algebra_equations",
            "Probability & Permutations":"/probability_permutations",
            "Data Interpretation":"/data_interpretation",
            "Time, Speed & Distance":"/time_speed_distance",
            "Data Sufficiency":"/data_sufficiency",
            "Data Structures & Algorithms":"/data_structures_algorithms",
            "Object-Oriented Programming":"/object_oriented_programming",
            "Operating Systems":"/operating_system",
            "Database Management Systems":"/dbms",
            "Networking & Cloud Computing":"/networking_cloud_computing",
            "System Design":"/system_design",
            "Advanced Coding":"/advanced_coding"
        }
        path = category_map.get(self.category, "/reading_comprehension")
        ref = db.reference(path)
        data = ref.get()
        if data:
            return list(data.values())
        return []

    def setup_ui(self):
        # Create a BoxLayout to contain both toolbar and timer
        toolbar_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="50dp",
            padding=[10, 10, 10, 10],
            md_bg_color=(0, 0, 1, 0.8)
        )

        title = MDLabel(
            text=f"{self.category} Questions",
            halign="left",
            font_style="H6",
            size_hint_x=1,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )

        # Add the title to the toolbar layout
        toolbar_layout.add_widget(title)

        # Add the timer label to the toolbar layout
        self.timer_label = MDLabel(
            text="00:00",
            halign="right",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_x=0.2
        )

        toolbar_layout.add_widget(self.timer_label)

        # Now add the toolbar_layout to the main layout
        self.main_layout.add_widget(toolbar_layout)

        # Scroll Area
        self.scroll = ScrollView()
        self.content = MDBoxLayout(
            orientation="vertical",
            padding=[20, 30, 20, 30],
            spacing=25,
            size_hint_y=None
        )
        self.content.bind(minimum_height=self.content.setter('height'))

        self.question_label = MDLabel(
            text="",
            size_hint_y=None,
            height=100,
            theme_text_color="Primary",
            halign="left",
            font_style="Subtitle1"
        )
        self.content.add_widget(self.question_label)

        # Option buttons
        for _ in range(4):
            btn = MDRaisedButton(
                text="",
                size_hint=(1, None),
                height="48dp",
                md_bg_color=(0.7, 0.85, 1, 1),
                text_color=(0, 0, 0, 1),
                on_release=self.select_option,
                font_style="Button"
            )
            self.content.add_widget(btn)
            self.option_buttons.append(btn)

        # Submit button
        self.submit_btn = MDRaisedButton(
            text="Submit & Next",
            pos_hint={"center_x": 0.5},
            on_release=self.submit_answer
        )
        self.content.add_widget(self.submit_btn)

        self.scroll.add_widget(self.content)
        self.main_layout.add_widget(self.scroll)
        self.add_widget(self.main_layout)

    def add_timer_to_toolbar(self):
        # Timer label is already added in the setup_ui method

        pass  # No need to add timer here anymore

    def update_timer(self, dt):
        if self.timer_enabled:
            elapsed = int(time.time() - self.start_time)
            mins, secs = divmod(elapsed, 60)
            self.timer_label.text = f"{mins:02d}:{secs:02d}"
            self.elapsed_time = elapsed

    def submit_answer(self, instance):
        if self.selected_option:
            current_q = self.questions[self.current_index]
            self.selected_answers.append({
                'question': current_q['question'],
                'selected': self.selected_option,
                'correct': current_q['answer']
            })
        else:
            self.selected_answers.append({
                'question': self.questions[self.current_index]['question'],
                'selected': None,
                'correct': self.questions[self.current_index]['answer']
            })

        self.current_index += 1
        if self.current_index < len(self.questions):
            self.display_question()
        else:
            self.display_summary()
            # Stop the timer if last question is submitted
            if self.timer_enabled:
                Clock.unschedule(self.update_timer)

    def display_question(self):
        if self.current_index < len(self.questions):
            q = self.questions[self.current_index]
            self.question_label.text = f"Q{self.current_index + 1}. {q['question']}"
            for i, opt_text in enumerate(q['options']):
                self.option_buttons[i].text = opt_text
                self.option_buttons[i].md_bg_color = (0.7, 0.85, 1, 1)
                self.option_buttons[i].text_color = (0, 0, 0, 1)
                self.option_buttons[i].disabled = False
            self.submit_btn.disabled = False
            self.selected_option = None

    def select_option(self, button_instance):
        for btn in self.option_buttons:
            btn.md_bg_color = (0.7, 0.85, 1, 1)
            btn.text_color = (0, 0, 0, 1)
        button_instance.md_bg_color = (0, 0, 0.7, 1)
        button_instance.text_color = (1, 1, 1, 1)
        self.selected_option = button_instance.text

    def display_summary(self):
        self.content.clear_widgets()

        # 🔙 Back toolbar
        back_toolbar = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="50dp",
            padding=[10, 10, 10, 10],
            md_bg_color=(0, 0, 1, 0.8)
        )
        back_btn = MDIconButton(
            icon="arrow-left",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            on_release=self.go_back_to_practice
        )
        title = MDLabel(
            text="Summary",
            halign="left",
            font_style="H6",
            size_hint_x=1,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        )
        back_toolbar.add_widget(back_btn)
        back_toolbar.add_widget(title)
        self.content.add_widget(back_toolbar)

        # ✅ Score
        correct_count = sum(1 for item in self.selected_answers if item['selected'] == item['correct'])
        score_label = MDLabel(
            text=f"[b]You answered {correct_count} out of {len(self.selected_answers)} correctly![/b]",
            markup=True,
            halign="center",
            size_hint_y=None,
            height=60,
            theme_text_color="Primary",
            font_style="H6"
        )
        self.content.add_widget(score_label)

        # 🎯 Summary
        summary_label = MDLabel(
            text="Answer Summary",
            theme_text_color="Primary",
            size_hint_y=None,
            height=50,
            halign="center",
            font_style="Subtitle1"
        )
        self.content.add_widget(summary_label)

        for idx, item in enumerate(self.selected_answers):
            is_correct = item['selected'] == item['correct']
            color = (0, 1, 0, 1) if is_correct else (1, 0, 0, 1)
            selected_text = item['selected'] if item['selected'] else "❌ Not answered"
            correct_text = item['correct']

            q_label = MDLabel(
                text=f"[b]Q{idx + 1}. {item['question']}[/b]",
                markup=True,
                size_hint_y=None,
                height=60
            )
            self.content.add_widget(q_label)

            ans_label = MDLabel(
                text=f"Your Answer: {selected_text}\nCorrect Answer: {correct_text}",
                theme_text_color="Custom",
                text_color=color,
                size_hint_y=None,
                height=60
            )
            self.content.add_widget(ans_label)

        # Show total time taken
        if self.timer_enabled:
            mins, secs = divmod(self.elapsed_time, 60)
            time_label = MDLabel(
                text=f"[b]Total Time Taken: {mins:02d} mins {secs:02d} secs[/b]",
                markup=True,
                size_hint_y=None,
                height=40,
                halign="center",
                theme_text_color="Secondary"
            )
            self.content.add_widget(time_label)

        self.submit_btn.disabled = True

    def go_back_to_practice(self, instance):
        self.manager.current = "practice_section"

    def ask_timer_permission(self):
        self.dialog = MDDialog(
            title="Start Timer?",
            text="Do you want to practice with a timer?",
            buttons=[
                MDFlatButton(text="No", on_release=self.start_without_timer),
                MDFlatButton(text="Yes", on_release=self.start_with_timer)
            ]
        )
        self.dialog.open()

    def start_with_timer(self, instance):
        self.timer_enabled = True
        self.start_time = time.time()
        self.dialog.dismiss()
        self.display_question()
        Clock.schedule_interval(self.update_timer, 1)

    def start_without_timer(self, instance):
        self.dialog.dismiss()
        self.display_question()



