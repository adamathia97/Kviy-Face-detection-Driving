from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window


# Load GUI file. This file contains all designing part
Builder.load_file('DangerAlarm.kv')


# This class is the class which will be referenced for designing for the
# kv file
# Reference for sound: https://orangefreesounds.com/loud-alarm-sound/
# Reference for image: https://pixabay.com/vectors/warning-attention-road-sign-146916/
class MyLayout(Widget):
    pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound = SoundLoader.load('Loud-alarm-sound.mp3')  # load the mp3 file
        self.sound.loop = True  # keep the sound to continue playing
        self.sound.play()  # play the sound


# Main App class
class DangerAlarm(App):
    def build(self):
        # Color is in rgba format. Applies red background color
        Window.clearcolor = (1, 0, 0, 1)
        return MyLayout()  # return output from MyLayout class


if __name__ == "__main__":
    DangerAlarm().run()  # call the function in main
