import time
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import numpy as np

# to keep track of time
endT = []
startT = []

# Image is created by me using PicsArt. Did not take this image from
# anywhere on internet
softBox = BoxLayout(orientation='vertical')
softBox.add_widget(Image(source='Attention.jpg'))

# Image reference for 'warning.png':
# https://pixabay.com/vectors/warning-attention-road-sign-146916/
dangerBox = BoxLayout(orientation='vertical')
dangerBox.add_widget(Image(source='warning.png'))
dangerBox.add_widget(Label(text='UNSAFE', font_size=100, bold=True, color=(1, 1, 1, 1)))


# reference of orange background image:
# https://pixabay.com/photos/background-abstract-pattern-texture-2022763/
SoftPopup = Popup(title=' ', separator_height=0, background='orange.jpg',
                  content=softBox)
DangerPopUp = Popup(title=' ', separator_height=0, background_color=(255, 0, 0, 1),
                    content=dangerBox)

# Reference for sound: https://orangefreesounds.com/soft-alarm-tone/
SoftAlarm = SoundLoader.load('Soft-alarm-tone.mp3')
SoftAlarm.loop = True

# Reference for sound: https://orangefreesounds.com/loud-alarm-sound/
DangerAlarm = SoundLoader.load('Loud-alarm-sound.mp3')
DangerAlarm.loop = True

DangerSoundPlaying = False
SoftPopupShowing = False
DangerPopupShowing = False


class FaceDetection(Image):
    def __init__(self, capture, fps, **kwargs):
        super(FaceDetection, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    # This function updates the frame every second that has to be
    # displayed on screen
    def update(self, dt):
        global endT
        global startT
        global SoftPopup
        global DangerPopUp
        global SoftAlarm
        global DangerSoundPlaying
        global SoftPopupShowing
        global DangerPopupShowing

        isCameraOn, frame = self.capture.read()  # check whether camera is on
        FaceRectangle = np.ndarray((frame.shape[1], frame.shape[0]))

        if isCameraOn:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            face = cv2.CascadeClassifier(cv2.data.haarcascades +
                'haarcascade_frontalface_default.xml')  # reference: https://github.com/opencv/opencv/tree/master/data/haarcascades

            faces = face.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

            eye = cv2.CascadeClassifier(cv2.data.haarcascades +
                'haarcascade_eye.xml')  # reference: https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_eye.xml

            eyes = eye.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=2)

            # draw bounding rectangles to capture face and eyes
            if len(eyes) > 0 and len(faces) > 0:
                for (x, y, w, h) in faces:
                    FaceRectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                for (x, y, w, h) in eyes:
                    FaceRectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
            else:
                FaceRectangle = frame

            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tobytes()
            image_texture = Texture.create(
                size=(FaceRectangle.shape[1], FaceRectangle.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display the image from the texture
            self.texture = image_texture

            # check whether face detection and eye detection happens
            if len(eyes) > 0 and len(faces) > 0:
                SoftAlarm.play()
                SoftAlarm.stop()

                DangerAlarm.play()
                DangerAlarm.stop()

                endT = []
                startT = []

                SoftPopup.dismiss()
                DangerPopUp.dismiss()

                DangerSoundPlaying = False
                DangerPopupShowing = False
                SoftPopupShowing = False

            else:
                startTime = time.perf_counter()
                startT.append(startTime)

                timeLimit = 2
                dangerAlarmTimeLimit = 15
                endTime = time.perf_counter()
                endT.append(endTime)

                if int(endT[-1]) - int(startT[0]) == timeLimit:
                    if SoftPopupShowing == False:
                        SoftPopup.open()
                    SoftPopupShowing = True
                    SoftAlarm.play()
                    DangerPopUp.dismiss()

                elif int(endT[-1]) - int(startT[0]) > dangerAlarmTimeLimit:
                    SoftAlarm.stop()  # stop the soft alarm sound

                    if DangerSoundPlaying == False:
                        # play danger alarm when more than 4 seconds pass
                        # and no face detection still happens
                        DangerAlarm.play()

                    DangerSoundPlaying = True
                    SoftPopup.dismiss()
                    if DangerPopupShowing == False:
                        DangerPopUp.open()
                    DangerPopupShowing = True

                unwantedstartT = startT[1:]
                unwantedendT = endT[:-1]

                for unwantedElements in unwantedstartT:
                    startT.remove(unwantedElements)
                    # print(startT)

                for unwantedElements in unwantedendT:
                    endT.remove(unwantedElements)
                    # print(endT)


class MainApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        self.my_camera = FaceDetection(capture=self.capture, fps=30)
        return self.my_camera

    # Exit app when the window is closed
    def on_stop(self):
        self.capture.release()
        SoftAlarm.stop()
        DangerAlarm.stop()
        SoftAlarm.unload()
        DangerAlarm.unload()


if __name__ == '__main__':
    MainApp().run()
