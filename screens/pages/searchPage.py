from kivy.uix.boxlayout import BoxLayout

class SearchPage(BoxLayout):
    def __init__(self, second_screen):
        super(SearchPage, self).__init__()
        
        self._parent = second_screen