from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from datetime import datetime
from random import randint, sample
from functools import partial

from .pages import HomePage, SearchPage
from logger import printLog
from person import Person
from widgets import ProfileCard

class SecondScreen(Screen):
    def __init__(self, manager):
        super(SecondScreen, self).__init__()
        self.bind(size=self.updateLayoutOrientation)
        self._parent = manager
        self._page_container = self.ids.page_place
        self._home_page = HomePage()
        self._search_page = SearchPage()
        self._people = [
            Person('Steven Doe', 'Content Creator', './assets/creators/steven_doe.png'),
            Person('Ze', 'Digital Artist', './assets/creators/ze.jpg'),
            Person('Andre Rio', 'UI/UIX Designer', './assets/creators/andre_rio.jpg'),
            Person('Ky Craft 116', 'Content Creator', './assets/creators/ky_craft_116.jpg'),
            Person('Irwansyah Saputra', 'Influencer', './assets/creators/irwansyah_saputra.jpg'),
            Person('Aspect30', 'Content Creator', './assets/creators/aspect30.jpg'),
            Person('Rayen', 'Digital Artist', './assets/creators/rayen.jpg'),
            Person('Nino', 'Digital Artist', './assets/creators/nino.jpg'),
            Person('Windo Anggara', 'Content Creator', './assets/creators/windo_anggara.jpg')
        ]
        self._selected_person = ''
        # spawn home_page first
        self._page_container.add_widget(self._home_page)
        # bind send_button
        self._home_page.ids.donate_card.ids.send_button.bind(on_release = self.sendDonate)
        # bind view all button untuk auto scroll
        self._home_page.ids.view_all_btn.bind(on_release = self.scrollToDown)

    def updateLayoutOrientation(self, win, size):
        width, height = size
        page_content = self._page_container.children[0]
        page_content.orientation = (
            'vertical' if width <= 725 else 'horizontal'
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

        self.updateDonateCard(
            random_choosen_person.name,
            random_choosen_person.role,
            random_choosen_person.photo_path
        )

        Clock.schedule_once(self.showLessPeopleSection)

    def getCurrentPage(self, *args):
        return self._page_container.children[0].id_string

    def goToPage(self, current_page, target_page):
        def spawnTargetPage(*args):
            self._page_container.add_widget(target_page)
            # or do animation

        def removeCurrentPage(*args):
            self._page_container.remove_widget(current_page)
            # or do animation

    def sendDonate(self, *args):
        person = self._home_page.ids.donate_card.person_name
        money = self._home_page.ids.donate_card.ids.money_total.text
        message = self._home_page.ids.donate_card.ids.message_form.text

        if money == '0':
            self._parent.spawnPopup(
                (255/255, 144/255, 144/255, 1),
                'Donasi Gagal!!!',
                f'Setidaknya butuh [color=FFFFFF]$1[/color] untuk berdonasi!!'
            )
        else:
            self._parent.spawnPopup(
                (221/255, 238/255, 170/255, 1),
                'Donasi Berhasil!!!',
                f'Terimakasih, Kamu telah mengirimkan donasi kepada [color=0800EF]{person}[/color] sebesar [color=EC0101]${money}[/color]'
            )
            self.resetDonateCardForm()

        printLog('donate card info', person)
        printLog('donate card info', money)
        printLog('donate card info', message)

    def updateDonateCard(self, name, role, pict, *args):
        self._home_page.ids.donate_card.person_name = name
        self._home_page.ids.donate_card.person_role = role
        self._home_page.ids.donate_card.person_pict = pict

        self._selected_person = name

        Clock.schedule_once(self.resetDonateCardForm)

    def resetDonateCardForm(self, *args):
        self._home_page.ids.donate_card.ids.money_total.text = '0'
        self._home_page.ids.donate_card.ids.message_form.text = ''

    def showLessPeopleSection(self, *args):
        self._home_page.ids.view_all_btn.text = 'view all'
        
        profile_section = self._home_page.ids.profile_card_container

        if len(profile_section.children) == len(self._people):
            profile_section.clear_widgets()
            printLog('log', 'clear widgets for every children in profile_section')
        else:
            pass

        # generate profile card pada profile section
        def generateCard(*args):
            for i in range(3):
                profile_section.add_widget(ProfileCard())
        Clock.schedule_once(generateCard)

        # memberikan identitas pada setiap profile card
        def setPersonInfo(*args):
            people_index = 2
            # karena container children bersifat reversed, maka index juga diambil dari belakang
            for child in profile_section.children:
                child.person_name = self._people[people_index].name
                child.person_role = self._people[people_index].role
                child.person_pict = self._people[people_index].photo_path

                child.ids.pick_person_btn.bind(
                    on_release = partial(
                        self.updateDonateCard,
                        child.person_name,
                        child.person_role,
                        child.person_pict
                    )
                )
                child.ids.pick_person_btn.bind(on_release = self.scrollToUp)

                people_index -= 1
        Clock.schedule_once(setPersonInfo)

        self._home_page.ids.view_all_btn.unbind(on_release = self.showLessPeopleSection)
        self._home_page.ids.view_all_btn.bind(on_release = self.showMorePeopleSection)

    def showMorePeopleSection(self, instance):
        self._home_page.ids.view_all_btn.text = 'view less'

        profile_section = self._home_page.ids.profile_card_container

        # menambah profile card
        profile_card_showed_total = len(profile_section.children)
        def generateCard(*args):
            for i in range(len(self._people)-profile_card_showed_total):
                profile_section.add_widget(ProfileCard())
        Clock.schedule_once(generateCard)

        # menampilkan sisa person
        def setPersonInfo(*args):
            people_index = len(self._people)-1
            for child in profile_section.children:
                if child.person_name == 'Unknown':
                    child.person_name = self._people[people_index].name
                    child.person_role = self._people[people_index].role
                    child.person_pict = self._people[people_index].photo_path

                    child.ids.pick_person_btn.bind(
                        on_release = partial(
                            self.updateDonateCard,
                            child.person_name,
                            child.person_role,
                            child.person_pict
                        )
                    )
                    child.ids.pick_person_btn.bind(on_release = self.scrollToUp)

                    people_index -= 1
        Clock.schedule_once(setPersonInfo)

        self._home_page.ids.view_all_btn.unbind(on_release = self.showMorePeopleSection)
        self._home_page.ids.view_all_btn.bind(on_release = self.showLessPeopleSection)
        # unbind view all button untuk auto scroll
        #self._screen2.ids.view_all_btn.unbind(on_release = self.scrollToDown)

    def scrollToUp(self, *args):
        top_element = self.ids.top_scroll_anchor
        self.ids.screen2_scrollview.scroll_to(top_element)

    def scrollToDown(self, *args):
        bottom_element = self.ids.bottom_scroll_anchor
        self.ids.screen2_scrollview.scroll_to(bottom_element)
