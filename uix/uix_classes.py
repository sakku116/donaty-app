from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
#from kivy.uix.label import Label
#from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.textinput import TextInput
#from kivy.uix.widget import Widget
#from kivy.core.text import Text

from kivy.animation import Animation

'''
file ini berisi python class dari uix yang sudah dibuat sendiri.
jika uix tidak mempunyai class di sini, maka uix tersebut sudah
di define menggunakan @widget dalam kv class uix tersebut
'''

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

class SidebarItem(Button):
    def __init__(self, name='item'):
        super(SidebarItem, self).__init__()
        self.text = name
