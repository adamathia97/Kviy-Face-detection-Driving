from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import time
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
import numpy as np

# keep track of alarm counts
SoftAlarmRingTime = 0
DangerAlarmRingTime = 0

# keep track of number of rides with total time for the ride
NoOfRides = 0
StartRideTime = 0
EndRideTime = 0

RideStartTime = []
RideEndTime = []

root = ScreenManager()

# to keep track of time
endT = []
startT = []

camRelease = False

# Image is created by me using PicsArt. Did not take this image from
# anywhere on internet
softBox = BoxLayout(orientation="vertical")
softBox.add_widget(Image(source='Attention.jpg'))

# Image reference for 'warning.png':
# https://pixabay.com/vectors/warning-attention-road-sign-146916/
dangerBox = BoxLayout(orientation="vertical")
dangerBox.add_widget(Image(source='warning.png'))
dangerBox.add_widget(Label(text="UNSAFE", font_size=100, bold=True, color=(1, 1, 1, 1)))

# reference of orange background image:
# https://pixabay.com/photos/background-abstract-pattern-texture-2022763/
SoftPopup = Popup(title=' ', separator_height=0, background='orange.jpg',
                  content=softBox)
DangerPopup = Popup(title=' ', separator_height=0, background_color=(255, 0, 0, 1),
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
        global DangerPopup
        global SoftAlarmSound
        global DangerSoundPlaying
        global SoftPopupShowing
        global DangerPopupShowing
        global DangerAlarmRingTime
        global SoftAlarmRingTime
        global camRelease
        global StartRideTime
        global EndRideTime
        global RideEndTime
        global RideStartTime

        # The loop captures the frame from camera only if current screen was Screen2
        if root.current == "Screen2":
            startRTime = time.perf_counter()
            RideStartTime.append(startRTime)

            StartRideTime = RideStartTime[0]

            endRTime = time.perf_counter()
            RideEndTime.append(endRTime)
            EndRideTime = RideEndTime[-1]

            unwantedRstartT = RideStartTime[1:]
            unwantedRendT = RideEndTime[:-1]

            for unwantedElements in unwantedRstartT:
                RideStartTime.remove(unwantedElements)

            for unwantedElements in unwantedRendT:
                RideEndTime.remove(unwantedElements)

            if camRelease == True:
                self.capture.open(0)

            isCameraOn, frame = self.capture.read()  # check whether camera is on

            try:
                FaceRectangle = np.ndarray(frame.shape)
            except:
                pass

            if isCameraOn:
                camRelease = False
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # reference: https://github.com/opencv/opencv/tree/master/data/haarcascades
                face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                faces = face.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

                # reference: https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
                eyes = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

                eye = eyes.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=2)

                # draw bounding rectangles to capture face and eyes
                if len(eye) > 0 and len(faces) > 0:
                    for (x, y, w, h) in faces:
                        FaceRectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

                    for (x, y, w, h) in eye:
                        FaceRectangle = cv2.rectangle(FaceRectangle, (x, y), (x + w, y + h), (0, 255, 0), 3)

                else:
                    FaceRectangle = frame

                # convert it to texture
                buf1 = cv2.flip(FaceRectangle, 0)
                buf = buf1.tostring()
                image_texture = Texture.create(
                    size=(1280, 720), colorfmt='bgr', mipmap=True)
                green = Image(source='green.jpg')
                greenTex = green.texture

                # display the image from the texture
                self.texture = greenTex

                # check whether face detection and eye detection happens
                if len(eye) > 0 and len(faces) > 0:
                    SoftAlarm.play()
                    SoftAlarm.stop()

                    DangerAlarm.play()
                    DangerAlarm.stop()

                    endT = []
                    startT = []

                    SoftPopup.dismiss()
                    DangerPopup.dismiss()

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
                            SoftPopup.open()  # show attention screen
                            SoftAlarmRingTime += 1

                        SoftPopupShowing = True
                        SoftAlarm.play()
                        DangerPopup.dismiss()

                    elif int(endT[-1]) - int(startT[0]) > dangerAlarmTimeLimit:
                        SoftAlarm.stop()  # stop the soft alarm sound

                        # play danger alarm when more than 15 seconds pass
                        # and no face and eye detection still happens
                        if DangerSoundPlaying == False:
                            DangerAlarm.play()

                        DangerSoundPlaying = True

                        SoftPopup.dismiss()

                        if DangerPopupShowing == False:
                            DangerPopup.open()  # show danger alarm screen
                            DangerAlarmRingTime += 1

                        DangerPopupShowing = True

                    unwantedstartT = startT[1:]
                    unwantedendT = endT[:-1]

                    for unwantedElements in unwantedstartT:
                        startT.remove(unwantedElements)

                    for unwantedElements in unwantedendT:
                        endT.remove(unwantedElements)


class CustomScreen(Screen):
    def __init__(self, **kwargs):
        super(CustomScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        layout.add_widget(Label(text='Driving Partner', font_size=50))

        navig = BoxLayout(size_hint_y=0.2)
        nextBtn = Button(text='START DRIVING')

        nextBtn.bind(on_release=self.switch_next)
        navig.add_widget(nextBtn)
        layout.add_widget(navig)

        self.add_widget(layout)

    # Start video analysis
    def switch_next(self, *args):
        global NoOfRides
        NoOfRides += 1
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = self.manager.next()


class DrivingScreen(Screen):
    def __init__(self, **kwargs):
        super(DrivingScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        self.capture = cv2.VideoCapture(0)

        self.my_camera = FaceDetection(capture=self.capture, fps=60)
        layout.add_widget(self.my_camera)

        navig = BoxLayout(size_hint_y=0.2)
        nextBtn = Button(text='STOP DRIVING')
        nextBtn.bind(on_release=self.switch_next)
        navig.add_widget(nextBtn)
        layout.add_widget(navig)

        self.add_widget(layout)

    # Stop video analysis
    def switch_next(self, *args):
        global camRelease

        self.capture.release()
        camRelease = True
        SoftAlarm.stop()
        DangerAlarm.stop()

        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = self.manager.next()


class DrivingSummary(Screen):
    def __init__(self, **kwargs):
        super(DrivingSummary, self).__init__(**kwargs)

        # Update Drive Summary after 1 second
        Clock.schedule_interval(lambda x: self.getSummary(), 1)

        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

    def switch_next(self, *args):
        global SoftAlarmRingTime
        global DangerAlarmRingTime

        SoftAlarmRingTime = 0
        DangerAlarmRingTime = 0
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = self.manager.next()

    def getSummary(self):
        global SoftAlarmRingTime
        global DangerAlarmRingTime
        global EndRideTime
        global StartRideTime

        self.layout.clear_widgets()

        totalTime = str(float(EndRideTime - StartRideTime))
        splitTime = totalTime.split(".")

        summary = """Here is Your Driving Summary: \n\n
Total No. of Rides taken: """ + str(NoOfRides) + """\n
Total Riding Time: """ + splitTime[0] + """ seconds\n
No. of Times caution alarm rings: """ + str(SoftAlarmRingTime) + """\n
No. of Times warning alarm rings: """ + str(DangerAlarmRingTime)

        self.layout.add_widget(Label(text=summary, font_size=20))
        navig = BoxLayout(size_hint_y=0.2)

        nextBtn = Button(text='START DRIVING AGAIN')
        nextBtn.bind(on_release=self.switch_next)

        navig.add_widget(nextBtn)
        self.layout.add_widget(navig)


class DriveMonitoringApp(App):
    def build(self):
        root.add_widget(CustomScreen(name='Screen1'))
        root.add_widget(DrivingScreen(name='Screen2'))
        root.add_widget(DrivingSummary(name='Screen3'))
        return root


if __name__ == '__main__':
    DriveMonitoringApp().run()
