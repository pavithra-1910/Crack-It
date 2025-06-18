
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivymd.app import MDApp
from about import AboutScreen
from todo import TodoPage
from verbal import Verbal_prac
from interview import Interview
from practice import Practice
from weeklytest import WeeklyTestScreen
from welcome1 import welcome1
from welcomepage2 import welcome2
from welcome3 import welcome3
from welcomescreen import splashscreen
from loginpage import LoginPage
from home import HomeScreen
from logical import Logical
from quatative import quants
from technical_p import Technical_Prac
from company_prac import Company_Prac
from profile import ProfilePage
from notification import NotificationScreen
from setting import SettingsPage
from interviewtip import InterviewTipsScreen
from CommonHrQes import CommonHrQes
from gd import GroupDiscussionScreen
from technical import TechnicalQuestionsScreen
from portal import JobPortalScreen
from weeklytest import WeeklyTestScreen



class Main(MDApp):
    def build(self):
        Window.clearcolor=(1,1,1,1)
        Window.size=(350,640)

        self.sm = ScreenManager()

        self.sm.add_widget(splashscreen(name='splash'))
        self.sm.add_widget(welcome1(name='welcome1'))
        self.sm.add_widget(welcome2(name='welcome2'))
        self.sm.add_widget(welcome3(name='welcome3'))
        self.sm.add_widget(LoginPage(name='login'))
        self.sm.add_widget(HomeScreen(screen_manager=self.sm, name="homepage"))
        self.sm.add_widget(Practice(screen_manager=self.sm, name='practice_section'))
        self.sm.add_widget(Interview(screen_manager=self.sm,name='interview_section'))
        self.sm.add_widget(AboutScreen(name="about"))
        self.sm.add_widget(Logical(name="logical_practice"))
        self.sm.add_widget(quants(name="quants"))
        self.sm.add_widget(Technical_Prac(name="technical_p"))
        self.sm.add_widget(Company_Prac(name="company_p"))
        self.sm.add_widget(Verbal_prac(name="verbal"))
        self.sm.add_widget(ProfilePage(name='profile'))
        self.sm.add_widget(NotificationScreen(name="notifications"))
        self.sm.add_widget(SettingsPage(name="setting"))
        self.sm.add_widget(InterviewTipsScreen(name="interviewtip"))
        self.sm.add_widget(CommonHrQes(name="commonhr"))
        self.sm.add_widget(GroupDiscussionScreen(name="gd"))
        self.sm.add_widget(TechnicalQuestionsScreen(name="techq"))
        self.sm.add_widget(JobPortalScreen(name="jobportal"))
        self.sm.add_widget(TodoPage(name="todo"))
        self.sm.add_widget(WeeklyTestScreen(name="week"))
        self.sm.current="splash"
        return self.sm

  


if __name__ == '__main__':
    Main().run()