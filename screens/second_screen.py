from kivy.uix.screenmanager import Screen
from .pages import HomePage, SearchPage

from kivy.clock import Clock

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        self.bind(size=self.updateLayoutOrientation)

        self._page_container = self.ids.page_place
        self._home_page = HomePage()
        self._search_page = SearchPage()

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

    def updateDonateCard(self, name, role, pict, *args):
        self._home_page.ids.donate_card.person_name = name
        self._home_page.ids.donate_card.person_role = role
        self._home_page.ids.donate_card.person_pict = pict

        self._selected_person = name

        Clock.schedule_once(self.resetDonateCardForm)

    def resetDonateCardForm(self, *args):
        self._home_page.ids.donate_card.ids.money_total.text = '0'
        self._home_page.ids.donate_card.ids.message_form.text = ''

    def scrollToUp(self, *args):
        top_element = self.ids.top_scroll_anchor
        self.ids.screen2_scrollview.scroll_to(top_element)

    def scrollToDown(self, *args):
        bottom_element = self.ids.bottom_scroll_anchor
        self.ids.screen2_scrollview.scroll_to(bottom_element)
