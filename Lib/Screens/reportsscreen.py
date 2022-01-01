from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineListItem
from kivymd.uix.picker import MDDatePicker
from datetime import datetime
from Lib.Helpers.helpers import SwipeToClockOut
from Lib.Helpers.database import TKDB


class ReportsScreen(Screen, BoxLayout):

    def __init__(self, **kwargs):
        super(ReportsScreen, self).__init__(**kwargs)

        self.db = TKDB()

    def on_pre_enter(self):
        self.ids.container.clear_widgets()
        self.records = self.db.getAllRecords()
        self._refreshRecords(self.records)
        print(self.records)


    def _refreshRecords(self, records):
        hours = 0
        minutes = 0
        seconds = 0
        totalTime = 0
        for record in records:
            if record[0] != 1 and record[3]:
                clockIn = datetime.fromisoformat(f'{record[1]} {record[2]}')
                clockOut = datetime.fromisoformat(f'{record[1]} {record[3]}')
                difference = clockOut - clockIn
                hours, rem = divmod(difference.total_seconds(), 3600)
                minutes, seconds = divmod(rem, 60)
                totalTime += difference.total_seconds()
                if hours:
                    self.ids.container.add_widget(
                        OneLineListItem(text=f'{int(hours)} Hours, {int(minutes)} Minutes, {int(seconds)} seconds.')
                    )
                else:
                    self.ids.container.add_widget(
                        OneLineListItem(text=f'{int(minutes)} Minutes, {int(seconds)} seconds.')
                    )
        return totalTime
                

    def on_save(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: selected date;

        :type value: <class 'datetime.date'>;
        :param date_range: list of 'datetime.date' objects in the selected range;

        :type date_range: <class 'list'>;
        '''

        self.ids.container.clear_widgets()
        records = self.db.getRange(date_range)
        totalTime = self._refreshRecords(records)
        tHours, tRem = divmod(totalTime, 3600)
        tMinutes, tSeconds = divmod(tRem, 60)
        self.ids.container.add_widget(
            OneLineListItem(text=f'between the date of {date_range[0]} and {date_range[-1]} you had {int(tHours)} hour {int(tMinutes)} minutes and {int(tSeconds)} seconds, on the clock.')
        )

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):
        date_dialog = MDDatePicker(
            mode="range",
        )

        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
