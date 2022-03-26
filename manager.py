from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from functools import partial

from logger import printLog
from screens import FirstScreen, SecondScreen
from widgets import *

class Manager(Screen):
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.bind(size=self.updateLayout)

        # declare screen class
        self._screen1 = FirstScreen(self)
        self._screen2 = SecondScreen(self)

        # spawn first screen
        self.ids.first_screen_place.add_widget(self._screen1)

        self._sidebar_shown_state = False

        # set sidebar screen state
        self.sidebarConfig('for_screen1')

    def updateLayout(self, win, size):
        width, height = size

        sidebar_width = self.ids.sidebar.width

        if width <= 725:
            pass
        else:
            if self._sidebar_shown_state == True:
                # ubah layout dengan mengurangi width dari screens_place
                # dan membuatnya stuck ke kanan (bisa dilakukan karena parentnya adalah floatlayout)
                #self.ids.main_container.width = width-sidebar_width
                Animation(
                    duration = .7,
                    width = width-sidebar_width,
                    t = 'out_circ'
                ).start(self.ids.main_container)
            else:
                self.ids.main_container.width = self.width

    def goToFirstScreen(self, *args):
        def callback(*args):
            screen1_place = self.ids.first_screen_place
            screen1_place.add_widget(self._screen1)
            printLog('log','first_screen created in screen1_place')

            screen2_place = self.ids.second_screen_place
            screen2_place.remove_widget(self._screen2)
            printLog('log','second screen removed from screen2_place')

        self.closeSidebar()

        # menunggu sidebar ditutup selama .2 detik
        Clock.schedule_once(callback, .2)

        # set sidebar screen state
        self.sidebarConfig('for_screen1')

    def goToSecondScreen(self, *args):
        def callback(*args):
            # spawn second_screen
            screen2_place = self.ids.second_screen_place
            screen2_place.add_widget(self._screen2)
            self._screen2.setup()

            printLog('log','second_screen created in screen2_place')

            # remove first_screen
            screen1_place = self.ids.first_screen_place
            screen1_place.remove_widget(self._screen1)

            printLog('log','first screen removed from screen1_place')

        if self._sidebar_shown_state == True:
            self.closeSidebar()
            # menunggu sidebar ditutup selama .2 detik
            Clock.schedule_once(callback, .2)
        else:
            Clock.schedule_once(callback)

        # mencegah config berjalan saat proses closeSidebar() berjalan
        Clock.schedule_once(partial(self.sidebarConfig, 'for_screen2'), .2)

    def sidebarConfig(self, screen, *args):
        def spawnItems(menu_items):
            def addItems(*args):
                for i in menu_items:
                    self.ids.sidebar_items_container.add_widget(i)
            task = Clock.schedule_once(addItems)

        self._sidebar_screen_state = screen

        if screen == 'for_screen1':
            printLog('sidebar', 'for screen1')
            # bersihkan menu dari for_screen1
            # menghindari error ketika sidebar_place belum ditempati
            if len(self.ids.sidebar_items_container.children) == 0:
                pass
            else:
                self.ids.sidebar_items_container.clear_widgets()
            if len(self.ids.sidebar_footer_container.children) == 0:
                pass
            else:
                self.ids.sidebar_footer_container.clear_widgets()

            spawnItems([
                SidebarItem('s1_m1'),
                SidebarItem('s1_m2'),
                SidebarItem('s1_m3'),
            ])

        elif screen == 'for_screen2':
            printLog('sidebar', 'for screen2')
            self.ids.sidebar_items_container.clear_widgets()

            spawnItems([
                SidebarItem('s2_m1'),
                SidebarItem('s2_m2'),
                SidebarItem('s2_m3'),
            ])

            # spawn signout btn
            signout_button = SignoutButton()
            signout_button.bind(on_release = self.goToFirstScreen)
            self.ids.sidebar_footer_container.add_widget(signout_button)

    def showSidebar(self, *args):
        # animate
        anim = Animation(
            myX = 0,
            duration = .3,
            t = 'out_circ')
        anim.start(self.ids.sidebar)

        self._sidebar_shown_state = True
        printLog('sidebar', 'Showed')

        self.updateLayout(None, self.size)

    def closeSidebar(self, *args):
        anim = Animation(
            myX = -1,
            duration = .5,
            t = 'out_circ')
        anim.start(self.ids.sidebar)

        self._sidebar_shown_state = False
        printLog('sidebar', 'Closed')

        self.updateLayout(None, self.size)

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
