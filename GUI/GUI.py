from kivy.app import App
import cv2
import numpy as np
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty

global name=''

class CustomScreen(Screen):


    def softAlarm(self, *args):
        self.sound = SoundLoader.load('Soft-alarm-tone.mp3')
        self.sound.loop = True
        self.sound.play()



    def __init__(self, **kwargs):

        super(CustomScreen, self).__init__(**kwargs)

 
        layout = BoxLayout(orientation='vertical')


        layout.add_widget(Label(text='Driving Patner', font_size=50))


        navig = BoxLayout(size_hint_y=0.2)

        label1 = Label(text='Enter your name:', font_size = 30 , valign = 'bottom')

        navig.add_widget(label1)
      
        next = TextInput(font_size=30)

        name = next.text

        btn=Button(text='Save Name', font_size=30 , valign = 'bottom' ,halign='right')

        btn.bind(on_release=self.switch_next)
 
        navig.add_widget(next)
        navig.add_widget(btn)
        layout.add_widget(navig)


        self.add_widget(layout)


#Here we can write the code to start video analysis and all that
    def switch_next(self, *args):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = self.manager.next()



class DrivingScreen(Screen):



    def __init__(self, **kwargs):

        super(DrivingScreen, self).__init__(**kwargs)




        layout = BoxLayout(orientation='vertical')


        layout.add_widget(Label(text='Safe Driving' + name, font_size=50))


        navig = BoxLayout(size_hint_y=0.2)

        next = Button(text='Start Driving')

        next.bind(on_release=self.switch_next)

        navig.add_widget(next)
        layout.add_widget(navig)

        self.add_widget(layout)

#Here we can write to stop video analysis 
    def switch_next(self, *args):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = self.manager.next()
        cap = cv2.VideoCapture(0)
        face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #reference: https://github.com/opencv/opencv/tree/master/data/haarcascades
        eyes = cv2.CascadeClassifier('haarcascade_eye.xml') #reference: https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
        while (True):

                ret, frame = cap.read()

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

                if len(faces) > 0:
                        print('Face Detected')
                else:
                        print('Face not Detected')
				#Clock.schedule_once(self.softAlarm, 3)
				#time.sleep(5) this freezes the whole program, best to find another way to implement
				#Event.wait(5)
                        cv2.rectangle(frame,(0,200), (640,300),(0,255,0),cv2.FILLED)
                        cv2.putText(frame, "User Distracted",(150,265),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0,0,0),2 )
				#softAlarm()

                for (x, y, w, h) in faces:
				#getting coordinates of face
				#print(x,y,w,h)
                        roi = frame[y:y+h, x:x+w]

				#setting up bounding boxes for face
                        color = (0, 0, 255) 					#note that colors are in BGR and not RGB
                        color2 = (0, 255, 0 )
                        stroke = 3
                        width = x+w
                        height = y+h

				#drawing the bounding box with text
                        cv2.rectangle(frame, (x, y), (width, height), color, stroke )
                        cv2.putText(frame, "Face Detected", (x,y-5), cv2.FONT_HERSHEY_PLAIN, 1, color2, 2 )

                        roi_gray = gray[y:y+h, x:x+w]
                        roi_color = frame[y:y+h, x:x+w]
     
                        eye = eyes.detectMultiScale(roi_gray, scaleFactor=1.3, minNeighbors=2)
                        if len(eye) > 0:
                                print('Eyes detected')
                        else:
                                print('Eyes not detected')
                                cv2.rectangle(frame,(0,200), (640,300),(0,0,255),cv2.FILLED)
                                cv2.putText(frame, "Pay Attention!",(150,265),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0,0,0),2 )
                        for (ex, ey, ew, eh) in eye:
                                cv2.rectangle(roi_color,(ex,ey), (ex+ew, ey+eh),color2,2)
                cv2.imshow('Video', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        cap.release()
        cv2.destroyAllWindows()

class DrivingSummary(Screen):



    def __init__(self, **kwargs):

        super(DrivingSummary, self).__init__(**kwargs)




        layout = BoxLayout(orientation='vertical')


        layout.add_widget(Label(text='Here is your driving summary', font_size=50))


        navig = BoxLayout(size_hint_y=0.2)

        next = Button(text='START DRIVING AGAIN')

        next.bind(on_release=self.switch_next)

        navig.add_widget(next)
        layout.add_widget(navig)

        self.add_widget(layout)


    def switch_next(self, *args):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = self.manager.next()


class ScreenManagerApp(App):


    def build(self):

        root = ScreenManager()
        root.add_widget(CustomScreen(name='Screen1'))
        root.add_widget(DrivingScreen(name='Screen2'))
        root.add_widget(DrivingSummary(name='Screen3'))
        return root


# This is only a protection, so that if the file
# is imported it won't try to launch another App

if __name__ == '__main__':
    # And run the App with its method 'run'
    ScreenManagerApp().run()