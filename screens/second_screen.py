from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from datetime import datetime
from random import randint, sample
from functools import partial

from .pages import HomePage, SearchPage
from logger import printLog
import people

class SecondScreen(Screen):
    def __init__(self, manager):
        super(SecondScreen, self).__init__()
        self.bind(size=self.updateLayoutOrientation)
        self._parent = manager

        self._people = people.getList()
        self._selected_person = ''

        self._page_container = self.ids.page_place
        self._home_page = HomePage(self)
        self._search_page = SearchPage(self)
        self.bottomNavbarSetup()

        # spawn home_page first
        self._page_container.add_widget(self._home_page)

    def updateLayoutOrientation(self, win, size):
        width, height = size
        page_content = self._page_container.children[0]
        page_content.orientation = (
            'vertical' if width <= 760 else 'horizontal'
        )

    def setup(self, *args):
        # setting tanggal
        date = str(datetime.now().strftime('%d/%m/%Y'))
        self._home_page.ids.donate_card.datetime = date

        # mengacak _people
        self._people = sample(self._people, k=len(self._people))

        # memilih person untuk ditampilkan di donate card
        random_integer = randint(0, len(self._people)-1)
        random_choosen_person = self._people[random_integer]

        self._home_page.updateDonateCard(
            random_choosen_person.name,
            random_choosen_person.role,
            random_choosen_person.photo_path
        )

        # reset list dari person card
        self._home_page.ids.profile_card_container.clear_widgets()
        self._home_page.showLessPeopleSection()

    def bottomNavbarSetup(self):
        self.ids.home_nav_btn.bind(on_release=partial(self.goToPage, self._home_page))
        self.ids.search_nav_btn.bind(on_release=partial(self.goToPage, self._search_page))

    def goToPage(self, target_page, *args):
        current_page = self._page_container.children[0]

        def spawnTargetPage(*args):
            self._page_container.add_widget(target_page)
            # or do animation

        def removeCurrentPage(*args):
            self._page_container.remove_widget(current_page)
            # or do animation

        spawnTargetPage()
        removeCurrentPage()

    def scrollToUp(self, *args):
        top_element = self.ids.top_scroll_anchor
        self.ids.screen2_scrollview.scroll_to(top_element)

    def scrollToDown(self, *args):
        bottom_element = self.ids.bottom_scroll_anchor
        self.ids.screen2_scrollview.scroll_to(bottom_element)
