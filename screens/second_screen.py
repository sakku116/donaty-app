from kivy.uix.screenmanager import Screen
from .pages import HomePage

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        self.bind(size=self.updateLayoutOrientation)

        self._page_container = self.ids.page_place
        self._home_page = HomePage()

        # spawn home_page first
        self._page_container.add_widget(self._home_page)

    def updateLayoutOrientation(self, win, size):
        width, height = size
        page_content = self._page_container.children[0]

        page_content.orientation = (
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
        top_element = self.ids.top_scroll_anchor
        self.ids.screen2_scrollview.scroll_to(top_element)

    def scrollToDown(self, *args):
        '''
        scroll otomatis ke bawah (person section) saat tombol
        view all di tap
        '''
        bottom_element = self.ids.bottom_scroll_anchor
        self.ids.screen2_scrollview.scroll_to(bottom_element)
