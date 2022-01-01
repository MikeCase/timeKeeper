from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import BoxLayout
from Lib.Helpers.helpers import SwipeToClockOut
from datetime import datetime
from Lib.Helpers.database import TKDB


class ClockScreen(Screen, BoxLayout):
    """ Clock Screen logic """

    def __init__(self, **kwargs):
        super(ClockScreen, self).__init__(**kwargs)
        self.db = TKDB()
        self.records = self.db.getAllRecords()

        if self.records:
            for record in self.records:
                convTime = datetime.fromisoformat(f'{record[1]} {record[2]}').strftime("%H:%M")
                if record[4] != 0:
                    self.ids.container.add_widget(
                        SwipeToClockOut(
                            db_id=record[0],
                            text=str(convTime)
                        )
                    )

    def clockIn(self):
        # self.clocktime.text = str(datetime.now().strftime('%b %d %Y - %H:%M'))
        clocktime = datetime.now()
        self.db.clockIn(clocktime)
        self.ids.container.add_widget(
            SwipeToClockOut(
                db_id=self.db.getLastRecord()[0],
                text=str(clocktime.strftime('%H:%M'))
            )
        )

    def clockOut(self, id, instance):
        """ Clock out function 

            Removes the list widget from the tree, and update the database
            to reflect the removal. 

        Args:
            id (int): The id of the db row
            instance (): The root widget requesting the clockout.

        Returns: 
            nothing..

        """

        self.db.clockOut(id, datetime.now())
        self.ids.container.remove_widget(instance)
