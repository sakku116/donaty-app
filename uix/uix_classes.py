from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
#from kivy.uix.label import Label
#from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.textinput import TextInput
#from kivy.uix.widget import Widget
#from kivy.core.text import Text

from kivy.animation import Animation

class GetStartedButton(Button):
    def __init__(self, **kwargs):
        super(GetStartedButton, self).__init__(**kwargs)

    def pressed(self):
        anim = Animation(
            mx = 0.01,
            my = .96,
            duration = .03,
        ).start(self.ids.fg_button)

    def released(self):
        # kembali ke posisi awal
        anim = Animation(
            mx = 0,
            my = 1,
            duration = .2,
            t = 'out_circ'
        ).start(self.ids.fg_button)

class ScreenBarrier(Button):
    pass

class DonateCard(FloatLayout):
    pass

class ProfileCard(FloatLayout):
    pass

class MyPopup(Button):
    pass

class Sidebar(Button):
    def __init__(self, **kwargs):
        super(Sidebar, self).__init__(**kwargs)
        self.spawnUnLogedinElement()

    def spawnUnLogedinElement(self, *args): # (for screen 1)
        pass
    
    def spawnLogedinElement(self, *args): # (for screen 2)
        pass