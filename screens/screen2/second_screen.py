from kivy.uix.screenmanager import Screen
from kivy.core.window import Window

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        Window.bind(size=self.updateLayoutOrientation)

    def updateLayoutOrientation(self, win, size):
        width, height = size

        self.ids.home_container.orientation = (
            'vertical' if width <= 725 else 'horizontal'
        )
        '''
        membuat boxlayout container ke tengah serta
        children menjadi responsive, karena stacklayout hanya bisa
        membuat responsive, tetapi tidak bisa dibuat ke tengah,
        maka dari itu menggunakan boxlayout dan membuatnya
        responsive dengan cara manual
        '''

    def scrollToUp(self, *args):
        '''
        scroll otomatis ke atas (donate card) saat tombol donate
        di profile card di tap
        '''
        donate_card_id = self.ids.donate_card
        self.ids.screen2_scrollview.scroll_to(donate_card_id)

    def scrollToDown(self, *args):
        '''
        scroll otomatis ke bawah (person section) saat tombol
        view all di tap
        '''
        bottom_profile_card = self.ids.profile_list_section_container
        self.ids.screen2_scrollview.scroll_to(bottom_profile_card)
