from kivymd.uix.card import MDCard, MDCardSwipe
from kivy.properties import StringProperty, NumericProperty


class SwipeToClockOut(MDCardSwipe):
    '''Card width `swipe-to-clockout` behavior'''

    db_id = NumericProperty()
    text = StringProperty()
