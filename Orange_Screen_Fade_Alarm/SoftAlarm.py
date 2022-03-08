from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image


# This class is the class which will be referenced for designing
class MyLayout(Widget):
    # initialize background color for the canvas to White
    background_color = ObjectProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set timer of 2 seconds. This will fade in Orange color
        # background after time interval of 2 seconds. OrangeScreen method is
        # referenced in the parameter
        Clock.schedule_once(self.orangeScreen, 2)
        Clock.schedule_once(self.playSoftAlarm, 3)

    # This function will create animation effect of background color
    def orangeScreen(self, *args):
        fadeIn = Animation(background_color=[250 / 255, 190 / 255, 88 / 255, 1])
        fadeIn.repeat = False
        fadeIn.start(self)

    # This function will play pinging sound and will also be displaying
    # image after time interval of 3 seconds.
    # Image is created by me using PicsArt. Did not take this image from
    # anywhere on internet
    # Reference for sound: https://orangefreesounds.com/soft-alarm-tone/
    def playSoftAlarm(self, *args):
        self.sound = SoundLoader.load('Soft-alarm-tone.mp3')  # load the mp3 file
        self.sound.loop = True  # keep the sound to continue playing
        self.sound.play()  # play the sound

        self.boxLayout = self.ids.boxLayout  # boxlayout
        self.img = Image(source='Attention.jpg')  # get the image

        self.boxLayout.add_widget(self.img)     # add the image to box layout


# Designing part for the canvas. Class MyLayout is referenced here
MyLayout = Builder.load_string('''
MyLayout:         
    canvas:
        Color: 
            rgba: self.background_color
        Rectangle:
            pos: self.pos
            size: self.size 
            
    BoxLayout:
        id:boxLayout
        padding:20
        spacing:20
        size: root.width, root.height           
''')


# Main App class
class SoftAlarm(App):
    def build(self):
        return MyLayout  # return output from MyLayout class


if __name__ == "__main__":
    SoftAlarm().run()  # call the function in main
