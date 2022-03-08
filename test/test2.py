from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
import time
import cv2
import numpy as np
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty

''
Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text:'Driving Partner'
            font_size: '50'
        Button:
            text: 'Start Driving'
            font_size: '30'
            size_hint_y: None
            height: '150dp'
            on_press: root.manager.current = 'camera'

<CameraScreen>:
    BoxLayout:
        orientation:'vertical'
        Camera:
            id:camera
            resolution: (640,480)
            play:True
        
        Button:
            text: 'Stop Driving'
            font_size: '30'
            size_hint_y: None
            height: '150dp'
            on_press: root.manager.current = 'summary'
<SummaryScreen>:
    BoxLayout:
        orientation:'vertical'
        Label:
            text:'Driving Summary'
            font_size: '50'
""")

class MenuScreen(Screen):
    pass

class CameraScreen(Screen):
    pass

class SummaryScreen(Screen):
    pass


class TestApp(App):

    def build(self):
 
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(CameraScreen(name='camera'))
        sm.add_widget(SummaryScreen(name='summary'))
        return sm

if __name__ == '__main__':
    TestApp().run()
