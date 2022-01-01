# import kivymd
from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from Lib.Screens.clockscreen import ClockScreen
from Lib.Screens.reportsscreen import ReportsScreen


Builder.load_file('timekeeper.kv')


class TimeKeeper(MDApp):

    def build(self):

        self.wm = ScreenManager()
        self.wm.add_widget(ClockScreen(name='clock'))
        self.wm.add_widget(ReportsScreen(name='reports'))
        self.wm.current = 'clock'
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        return self.wm

    def ChangeScreen(self, name):
        self.wm.current = name


timekeeper = TimeKeeper()
timekeeper.run()
