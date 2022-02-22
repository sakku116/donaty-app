'''
C:/py_venv/kivy_venv/scripts/activate
'''

'''
# konfigurasi untuk openGl dibawah versi 2
from kivy import Config
Config.set('graphics', 'multisamples', '0')
from kivy import require
require('2.0.0')
'''

#from kivy.properties import NumericProperty
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
'''
penggunaan Clock.schedule_once dapat mengoptimalkan kinerja aplikasi
karena tidak perlu menunggu for loop dieksekusi.
konsepnya seperti async dan await
'''

# IMPORT UTILITIES
from datetime import datetime
from random import randint, sample
from functools import partial

# IMPORT FILES
from screens.screen1.first_screen import FirstScreen
from screens.screen2.second_screen import SecondScreen
from uix.uix_classes import *

def printLog(event, text):
    print(f'({event}) = {text}')

############## SCREEN ##############

class Manager(Screen):
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)

        # define first screen class
        self._screen1 = FirstScreen()
        self.ids.first_screen_place.add_widget(self._screen1)
        self.firstScreenSetup()

        # define second screen class
        self._screen2 = SecondScreen()

        # declare people
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

    def goToFirstScreen(self, *args):
        pass

    def goToSecondScreen(self, *args):
        # spawn second_screen
        screen2_place = self.ids.second_screen_place
        screen2_place.add_widget(self._screen2)
        self.secondScreenSetup()

        printLog('log','second_screen created in screen2_place')

        # remove first_screen
        screen1_place = self.ids.first_screen_place
        screen1_place.remove_widget(self._screen1)

        printLog('log','first screen removed from screen1_place')

    def firstScreenSetup(self, *args):
        # set sidebar state screen for
        self.sidebarConfig('for_screen1')

        # bind tombol yang ada di first_screen karena berbeda parent class dengan manager
        self._screen1.ids.get_started_btn.bind(on_release = self.showLoginForm)
        self._screen1.ids.line_sparator_login_form.bind(on_release = self.removeLoginForm)

    def secondScreenSetup(self, *args):
        # set sidebar state screen for
        self.sidebarConfig('for_screen2')

        # bind send_button
        self._screen2.ids.donate_card.ids.send_button.bind(on_release = self.sendDonate)

        # setting tanggal
        date = str(datetime.now().strftime('%d/%m/%Y'))
        self._screen2.ids.donate_card.datetime = date

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

        self.showLessPeopleSection()

        # bind view all button untuk auto scroll
        self._screen2.ids.view_all_btn.bind(on_release = self._screen2.scrollToDown)

    def updateDonateCard(self, name, role, pict, *args):
        self._screen2.ids.donate_card.person_name = name
        self._screen2.ids.donate_card.person_role = role
        self._screen2.ids.donate_card.person_pict = pict

        self._selected_person = name

        self.resetDonateCardForm()

    def resetDonateCardForm(self, *args):
        # mereset form selected_person diperbarui
        self._screen2.ids.donate_card.ids.money_total.text = '0'
        self._screen2.ids.donate_card.ids.message_form.text = ''

    def sendDonate(self, *args):
        person = self._screen2.ids.donate_card.person_name
        money = self._screen2.ids.donate_card.ids.money_total.text
        message = self._screen2.ids.donate_card.ids.message_form.text

        if money == '0':
            self.spawnPopup(
                (255/255, 144/255, 144/255, 1),
                'Donasi Gagal!!!',
                f'Setidaknya butuh [color=FFFFFF]$1[/color] untuk berdonasi!!'
            )
        else:
            self.spawnPopup(
                (221/255, 238/255, 170/255, 1),
                'Donasi Berhasil!!!',
                f'Terimakasih, Kamu telah mengirimkan donasi kepada [color=0800EF]{person}[/color] sebesar [color=EC0101]${money}[/color]'
            )
            self.resetDonateCardForm()

        printLog('donate card info', person)
        printLog('donate card info', money)
        printLog('donate card info', message)

    def sidebarConfig(self, screen):
        def spawnItems(menu_items):
            def addItems(*args):
                for i in menu_items:
                    self.ids.sidebar_container.add_widget(i)
            task = Clock.schedule_once(addItems)

        if screen == 'for_screen1':
            printLog('sidebar', 'for screen1')
            # bersihkan menu dari for_screen1
            # menghindari error ketika sidebar_place belum ditempati
            if len(self.ids.sidebar_container.children) == 0:
                pass
            else:
                self.ids.sidebar_container.clear_widgets()
            spawnItems([
                SidebarItem('s1_m1'),
                SidebarItem('s1_m2'),
                SidebarItem('s1_m3'),
            ])

        elif screen == 'for_screen2':
            printLog('sidebar', 'for screen2')
            # bersihkan menu dari for_screen1
            self.ids.sidebar_container.clear_widgets()

            spawnItems([
                SidebarItem('s2_m1'),
                SidebarItem('s2_m2'),
                SidebarItem('s2_m3'),
            ])

    def showSidebar(self, *args):
        # animate
        anim = Animation(
            myX = 0,
            duration = .3,
            t = 'out_circ'
        )
        anim.start(self.ids.sidebar)

        def callback(*args):
            printLog('sidebar', 'Showed')

        anim.bind(on_complete = callback)

    def closeSidebar(self, *args):
        anim = Animation(
            myX = -1,
            duration = .1,
            t = 'out_circ'
        )
        anim.start(self.ids.sidebar)

        def callback2(*args):
            printLog('sidebar', 'Closed')

        anim.bind(on_complete = callback2)

    def loginAuth(self, *args):
        email = self._screen1.ids.email_login_field.text
        password = self._screen1.ids.password_login_field.text

        if email == 'admin' and password == 'admin':
            self.goToSecondScreen()
            printLog('log', 'berhasil login')
        else:
            pass

    def showLoginForm(self, *args):
        anim = Animation(
            my = 0,
            duration = .3,
            t = 'out_circ'
        ).start(self._screen1.ids.login_form)

        self.loginFormState('active')

    def removeLoginForm(self, *args):
        anim = Animation(
            my = -.5,
            duration = .2,
            t = 'out_circ'
        ).start(self._screen1.ids.login_form)

        self.loginFormState('inactive')

    def loginFormState(self, state):
        printLog('login form sate', state)
        barrier = ScreenBarrier()

        if state == 'active': # (jika login form telah muncul)
            # unbind func showLoginForm
            self._screen1.ids.get_started_btn.unbind(on_release = self.showLoginForm)
            # bind ke login func
            self._screen1.ids.get_started_btn.bind(on_release = self.goToSecondScreen)

            # ubah text
            self._screen1.ids.get_started_btn.text = 'Login'

            # pasang screen barrier
            self._screen1.ids.barrier_place.add_widget(barrier)

            # bind barrier untuk removeLoginForm
            barrier.bind(on_release = self.removeLoginForm)

            # bind manager.ids.menu_button + search_button > removeLoginForm
            self.ids.manager_menu_btn.bind(on_release = self.removeLoginForm)
            self.ids.manager_search_btn.bind(on_release = self.removeLoginForm)

        else: # (jika login form tidak muncul)
            # unbind func removeLoginForm
            self._screen1.ids.get_started_btn.unbind(on_release = self.removeLoginForm)

            # bind kembali func showLoginForm
            self._screen1.ids.get_started_btn.unbind(on_release = self.goToSecondScreen)
            self._screen1.ids.get_started_btn.bind(on_release = self.showLoginForm)

            # rubah text button menjadi awalnya
            self._screen1.ids.get_started_btn.text = 'Get Started'

            # menghapus barrier
            barrier.unbind(on_release = self.removeLoginForm)
            self._screen1.ids.barrier_place.clear_widgets()

            # unbind manager.ids.menu_button + search_button > removeLoginForm
            self.ids.manager_menu_btn.unbind(on_release = self.removeLoginForm)
            self.ids.manager_search_btn.unbind(on_release = self.removeLoginForm)

    def spawnPopup(self, color=(239/255, 105/255, 137/255, 1), title='title', message='message', *args):
        # declare popup
        popup = MyPopup()

        popup.canvas_color = color
        popup.title = title
        popup.message = message

        # spawn
        self.ids.popup_place.add_widget(popup)

        # animasikan setelah di spawn
        Animation(
            my_top = 1,
            duration = .2,
            t = 'out_circ'
        ).start(popup)

        # task untuk remove popup
        task = Clock.schedule_once(partial(
            self.removePopup,
            popup), 4)

        # func untuk membatalkan task
        def cancelTask(*args):
            task.cancel()

        printLog('popup log', 'popup placed')

    def removePopup(self, popup_instance, *args):
        def remove(*args):
            self.ids.popup_place.remove_widget(popup_instance)
            printLog('popup log', 'popup removed')

        # animasikan sebelum dihapus
        anim = Animation(
            my_top = 1.5,
            duration = .25,
            t = 'out_circ'
        )
        anim.start(popup_instance)
        anim.bind(on_complete = remove)

    def showLessPeopleSection(self, *args):
        profile_section = self._screen2.ids.profile_card_container

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
                child.ids.pick_person_btn.bind(on_release = self._screen2.scrollToUp)

                people_index -= 1
        Clock.schedule_once(setPersonInfo)

        self._screen2.ids.view_all_btn.unbind(on_release = self.showLessPeopleSection)
        self._screen2.ids.view_all_btn.bind(on_release = self.showMorePeopleSection)

    def showMorePeopleSection(self, instance):
        profile_section = self._screen2.ids.profile_card_container

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
                    child.ids.pick_person_btn.bind(on_release = self._screen2.scrollToUp)

                    people_index -= 1
        Clock.schedule_once(setPersonInfo)

        self._screen2.ids.view_all_btn.unbind(on_release = self.showMorePeopleSection)
        self._screen2.ids.view_all_btn.bind(on_release = self.showLessPeopleSection)
        # unbind view all button untuk auto scroll
        #self._screen2.ids.view_all_btn.unbind(on_release = self.scrollToDown)

############## CONTENT ##############

class Person():
    def __init__(self, name='unknown', role='unknown', photo_path=''):
        self.name = name
        self.photo_path = photo_path
        self.role = role

    def getAttributeList(self):
        return [self.name, self.role, self.photo_path]

############## APP ##############

class MyApp(App):
    def build(self):

        '''
        [STRUCTURE]
        <Manager>:
            # import all of kv file and it used by the children
            # without importing the file again inside of children class
            <FirstScreen>:
            <SecondScreen>:
        '''

        kv = Builder.load_file('main.kv')
        Window.size = (384, 680)
        Window.minimum_width, Window.minimum_height = Window.size
        #changeStatusBarColor()

        return Manager()

    def changeStatusBarColor(self):
        from jnius import autoclass

        WindowManager = autoclass('android.view.WindowManager')
        R = autoclass('android.R')
        activity = autoclass('My.PythonActivity').mActivity

        window = activity.getWindow();
        window.clearFlags(WindowManager.LayoutParams.FLAG_TRANSLUCENT_STATUS)
        window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
        window.setStatusBarColor(activity.getResources().getColor(R.color.my_statusbar_color));

if __name__ == '__main__':
    MyApp().run()
