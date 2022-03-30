from kivy.uix.screenmanager import Screen
from kivy.animation import Animation

from widgets import ScreenBarrier
from logger import printLog

class FirstScreen(Screen):
    def __init__(self, manager):
        super(FirstScreen, self).__init__()
        
        self._parent = manager

        self.ids.get_started_btn.bind(on_release = self.showLoginForm)
        self.ids.line_sparator_login_form.bind(on_release = self.removeLoginForm)

    def loginAuth(self, *args):
        email = self.ids.email_login_field.text
        password = self.ids.password_login_field.text

        if email == 'admin' and password == 'admin':
            self._parent.goToSecondScreen()
            printLog('log', 'berhasil login')
        else:
            pass

    def showLoginForm(self, *args):
        anim = Animation(
            my = 0,
            duration = .3,
            t = 'out_circ'
        ).start(self.ids.login_form)

        self.loginFormState('active')

    def removeLoginForm(self, *args):
        anim = Animation(
            my = -1,
            duration = .5,
            t = 'out_circ'
        ).start(self.ids.login_form)

        self.loginFormState('inactive')

    def loginFormState(self, state):
        printLog('login form sate', state)
        barrier = ScreenBarrier()

        if state == 'active': # (jika login form telah muncul)
            # unbind func showLoginForm
            self.ids.get_started_btn.unbind(on_release = self.showLoginForm)
            # bind ke login func
            self.ids.get_started_btn.bind(on_release = self._parent.goToSecondScreen)

            # ubah text
            self.ids.get_started_btn.text = 'Login'

            # pasang screen barrier
            self.ids.barrier_place.add_widget(barrier)

            # bind barrier untuk removeLoginForm
            barrier.bind(on_release = self.removeLoginForm)

            # bind manager.ids.menu_button + search_button > removeLoginForm
            self._parent.ids.manager_menu_btn.bind(on_release = self.removeLoginForm)
            self._parent.ids.manager_search_btn.bind(on_release = self.removeLoginForm)

        else: # (jika login form tidak muncul)
            # unbind func removeLoginForm
            self.ids.get_started_btn.unbind(on_release = self.removeLoginForm)

            # bind kembali func showLoginForm
            self.ids.get_started_btn.unbind(on_release = self._parent.goToSecondScreen)
            self.ids.get_started_btn.bind(on_release = self.showLoginForm)

            # rubah text button menjadi awalnya
            self.ids.get_started_btn.text = 'Get Started'

            # menghapus barrier
            barrier.unbind(on_release = self.removeLoginForm)
            self.ids.barrier_place.clear_widgets()

            # unbind manager.ids.menu_button + search_button > removeLoginForm
            self._parent.ids.manager_menu_btn.unbind(on_release = self.removeLoginForm)
            self._parent.ids.manager_search_btn.unbind(on_release = self.removeLoginForm)