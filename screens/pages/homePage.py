from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from functools import partial

from widgets import ProfileCard
from logger import printLog

class HomePage(BoxLayout):
    def __init__(self, second_screen):
        super(HomePage, self).__init__()
        self._manager = second_screen._parent
        self._parent = second_screen

        # bind send_button
        self.ids.donate_card.ids.send_button.bind(on_release = self.sendDonate)
        # bind view all button untuk auto scroll
        self.ids.view_all_btn.bind(on_release = self._parent.scrollToDown)

    def sendDonate(self, *args):
        person = self.ids.donate_card.person_name
        money = self.ids.donate_card.ids.money_total.text
        message = self.ids.donate_card.ids.message_form.text

        if money == '0':
            self._manager.spawnPopup(
                (255/255, 144/255, 144/255, 1),
                'Donasi Gagal!!!',
                f'Setidaknya butuh [color=FFFFFF]$1[/color] untuk berdonasi!!'
            )
        else:
            self._manager.spawnPopup(
                (221/255, 238/255, 170/255, 1),
                'Donasi Berhasil!!!',
                f'Terimakasih, Kamu telah mengirimkan donasi kepada [color=0800EF]{person}[/color] sebesar [color=EC0101]${money}[/color]'
            )
            self.resetDonateCardForm()

        printLog('donate card info', person)
        printLog('donate card info', money)
        printLog('donate card info', message)

    def updateDonateCard(self, name, role, pict, *args):
        self.ids.donate_card.person_name = name
        self.ids.donate_card.person_role = role
        self.ids.donate_card.person_pict = pict

        self._selected_person = name

        Clock.schedule_once(self.resetDonateCardForm)

    def resetDonateCardForm(self, *args):
        self.ids.donate_card.ids.money_total.text = '0'
        self.ids.donate_card.ids.message_form.text = ''

    def showLessPeopleSection(self, *args):
        self.ids.view_all_btn.text = 'view all'
        
        profile_section = self.ids.profile_card_container

        if len(profile_section.children) == len(self._parent._people):
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
                child.person_name = self._parent._people[people_index].name
                child.person_role = self._parent._people[people_index].role
                child.person_pict = self._parent._people[people_index].photo_path

                child.ids.pick_person_btn.bind(
                    on_release = partial(
                        self.updateDonateCard,
                        child.person_name,
                        child.person_role,
                        child.person_pict
                    )
                )
                child.ids.pick_person_btn.bind(on_release = self._parent.scrollToUp)

                people_index -= 1
        Clock.schedule_once(setPersonInfo)

        self.ids.view_all_btn.unbind(on_release = self.showLessPeopleSection)
        self.ids.view_all_btn.bind(on_release = self.showMorePeopleSection)

    def showMorePeopleSection(self, instance):
        self.ids.view_all_btn.text = 'view less'

        profile_section = self.ids.profile_card_container

        # menambah profile card
        profile_card_showed_total = len(profile_section.children)
        def generateCard(*args):
            for i in range(len(self._parent._people)-profile_card_showed_total):
                profile_section.add_widget(ProfileCard())
        Clock.schedule_once(generateCard)

        # menampilkan sisa person
        def setPersonInfo(*args):
            people_index = len(self._parent._people)-1
            for child in profile_section.children:
                if child.person_name == 'Unknown':
                    child.person_name = self._parent._people[people_index].name
                    child.person_role = self._parent._people[people_index].role
                    child.person_pict = self._parent._people[people_index].photo_path

                    child.ids.pick_person_btn.bind(
                        on_release = partial(
                            self.updateDonateCard,
                            child.person_name,
                            child.person_role,
                            child.person_pict
                        )
                    )
                    child.ids.pick_person_btn.bind(on_release = self._parent.scrollToUp)

                    people_index -= 1
        Clock.schedule_once(setPersonInfo)

        self.ids.view_all_btn.unbind(on_release = self.showMorePeopleSection)
        self.ids.view_all_btn.bind(on_release = self.showLessPeopleSection)
        # unbind view all button untuk auto scroll
        #self._screen2.ids.view_all_btn.unbind(on_release = self.scrollToDown)
