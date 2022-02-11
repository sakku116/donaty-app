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

from kivy.properties import NumericProperty
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock
# penggunaan Clock.schedule_once dapat mengoptimalkan kinerja aplikasi
# karena tidak perlu menunggu for loop dieksekusi
# konsepnya seperti async dan await

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
#from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.textinput import TextInput
#from kivy.uix.widget import Widget
#from kivy.core.text import Text
#from kivy.clock import mainthread

from datetime import datetime
from random import randint, sample
import time
from functools import partial
# partial memungkinkan untuk memberi parameter saat bind function

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
        # bind tombol yang ada di first_screen karena berbeda parent class dengan manager
        self._screen1.ids.get_started_btn.bind(on_release = self.showLoginForm)
        self._screen1.ids.line_sparator_login_form.bind(on_release = self.removeLoginForm)

        # sidebar config
        self._sidebar_barrier = ScreenBarrier()
        self._sidebar = Sidebar()
        # bind tombol menu
        self.ids.manager_menu_btn.bind(on_release = self.showSidebar)

    def secondScreenSetup(self, *args):
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

        # mereset form selected_person diperbarui
        self._screen2.ids.donate_card.ids.money_total.text = '0'
        self._screen2.ids.donate_card.ids.message_form.text = ''

    def sendDonate(self, *args):
        person = self._screen2.ids.donate_card.person_name
        money = self._screen2.ids.donate_card.ids.money_total.text
        message = self._screen2.ids.donate_card.ids.message_form.text

        if money == '0':
            self.spawnPopup(
                'Donasi Gagal!!!',
                f'Setidaknya butuh $1 untuk berdonasi'
            )
        else:
            self.spawnPopup(
                'Donasi Berhasil!!!',
                f'Terimakasih, Kamu telah mengirimkan donasi kepada {person} sebesar ${money}'
            )

        printLog('donate card info', person)
        printLog('donate card info', money)
        printLog('donate card info', message)

    def showSidebar(self, *args):
        self.ids.sidebar_place.add_widget(self._sidebar_barrier)
        self.ids.sidebar_place.add_widget(self._sidebar)
        
        anim = Animation(
            myX = 0,
            duration = .3,
            t = 'out_circ'
        )
        anim.start(self._sidebar)

        def callback(*args):
            self.ids.manager_menu_btn.unbind(on_release = self.showSidebar)
            self.ids.manager_menu_btn.bind(on_release = self.closeSidebar)
            self._sidebar_barrier.bind(on_release = self.closeSidebar)
            printLog('screen1 sidebar', 'Showed')

        anim.bind(on_complete = callback)

    def closeSidebar(self, *args):
        anim = Animation(
            myX = -1,
            duration = .1,
            t = 'out_circ'
        )
        anim.start(self._sidebar)

        def callback2(*args):
            #self.ids.sidebar_place.remove_widget(barrier)
            self.ids.manager_menu_btn.unbind(on_release = self.closeSidebar)
            self.ids.manager_menu_btn.bind(on_release = self.showSidebar)
            self.ids.sidebar_place.remove_widget(self._sidebar)
            self.ids.sidebar_place.remove_widget(self._sidebar_barrier)
            printLog('screen1 sidebar', 'Closed')

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
            
    def spawnPopup(self, title, message, *args):
        barrier = ScreenBarrier()
        popup = MyPopup()

        popup.title = title
        popup.message = message

        # spawn
        self.ids.popup_place.add_widget(barrier)
        self.ids.popup_place.add_widget(popup)

        # animasikan setelah di spawn
        Animation(
            my_top = 1,
            duration = .2,
            t = 'out_circ'
        ).start(popup)

        # declare task
        task = Clock.schedule_once(partial(
            self.removePopup, 
            barrier,
            popup), 4)

        # func untuk membatalkan task saat diremove manual oleh user
        def cancelTask(*args):
            task.cancel()

        # bind barrier ke removePopup
        barrier.bind(on_release = cancelTask)
        barrier.bind(on_release =
            partial(
                self.removePopup,
                barrier,
                popup
            )
        )

        printLog('popup log', 'barrier & popup placed')

    def removePopup(self, barrier_instance, popup_instance, *args):
        def remove(*args):
            self.ids.popup_place.remove_widget(barrier_instance)
            self.ids.popup_place.remove_widget(popup_instance)
            printLog('popup log', 'barrier & popup removed')

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

class FirstScreen(Screen):
    pass

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

############## UIX ##############

class PaymtdLabel(Label):
    pass

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
        kv = Builder.load_file('./screens/manager.kv')
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
