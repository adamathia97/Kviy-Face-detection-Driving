import cv2
import numpy as np

cap = cv2.VideoCapture(0)
face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #reference: https://github.com/opencv/opencv/tree/master/data/haarcascades

while(True): 

	ret, frame = cap.read()

	#convert to grayscale
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	faces = face.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)

	for (x, y, w, h) in faces:
		
		#getting coordinates of face
		print(x,y,w,h)
		roi = frame[y:y+h, x:x+w]

		#setting up bounding boxes for face
		color = (0, 0, 255) 					#note that colors are in BGR and not RGB
		color2 = (0, 255, 0 )
		stroke = 3
		width = x+w
		height = y+h
		cv2.rectangle(frame, (x, y), (width, height), color, stroke )
		cv2.putText(frame, "Face Detected", (x,y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color2, 2 )







	cv2.imshow('frame', frame)

	#pressing Q terminates frame capture
	if cv2.waitKey(20) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()