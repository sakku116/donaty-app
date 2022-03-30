'''
"venv/scripts/activate"

[konfigurasi untuk openGl dibawah versi 2]
import os 
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
from kivy import Config, require
require('2.0.0')
Config.set('graphics', 'multisamples', '0')
'''

import os
from kivy.utils import platform

'''
if platform == 'android':
    dpi = '170'
else:
    dpi = '96'

os.environ['KIVY_DPI'] = dpi
'''

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from logger import printLog

class main(App):
    def build(self):
        self.title = 'Donaty'

        # main widget (@screen) class
        from manager import Manager # py class
        main_widget = Builder.load_file('manager.kv') # kv class
        
        printLog('starting', f'app is running...')
        printLog('platform', f'{platform}')
        
        if platform == 'win':
            Window.size = (384, 683)
            Window.minimum_width, Window.minimum_height = Window.size
            printLog('Window.size', f'{Window.size}')
        elif platform == 'android':
            #self.changeStatusBarColor()
            pass
        else:
            pass

        return Manager()

    def changeStatusBarColor(self):
        from jnius import autoclass

        WindowManager = autoclass('android.view.WindowManager')
        R = autoclass('android.R')
        activity = autoclass('My.PythonActivity').mActivity

        window = activity.getWindow()
        window.clearFlags(WindowManager.LayoutParams.FLAG_TRANSLUCENT_STATUS)
        window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
        window.setStatusBarColor(activity.getResources().getColor(R.color.my_statusbar_color))

if __name__ == '__main__':
    main().run()        
