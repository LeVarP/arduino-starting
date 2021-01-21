import cv2
import numpy as np
import video
from serial import Serial
import time


ser = Serial('/dev/ttyUSB0', baudrate=9600, timeout=1) # подключаемся к Arduino



edge = 35 # рамки условного центра изо6ражения
panAngle = 90 # начальное положение сервопривода 1 
tiltAngle = 90 # начальное положение сервопривода 2

        
def ObjectPosition (x, y): # функция вывода в консоль координат центра цели
    print ("[INFO] Object Center coordenates at X0 = {0} and Y0 =  {1}".format(x, y))

        
def ServoPosition (x, y): # функция управления сервоприводами
    global panAngle
    global tiltAngle
    if (x < width/2 - edge):
        panAngle += 1
        if panAngle > 170:
            panAngle = 170
        ser.write(bytearray([85, panAngle,180 - tiltAngle]))
        
    if (x > width/2 + edge):
        panAngle -= 1
        if panAngle < 10:
            panAngle = 10
        ser.write(bytearray([85, panAngle,180 - tiltAngle]))
        
    if (y < height/2 - edge):
        tiltAngle += 1
        if tiltAngle > 170:
            tiltAngle = 170
        ser.write(bytearray([85, panAngle, 180 - tiltAngle]))
        
    if (y > height/2 + edge):
        tiltAngle -= 1
        if tiltAngle < 10:
            tiltAngle = 10
        ser.write(bytearray([85, panAngle, 180 - tiltAngle]))
        
        
        

cv2.namedWindow( "result" )

cap = video.create_capture(0) # ловим камеру

hsv_min = np.array((80, 60, 60), np.uint8) # нижняя граница зеленого в HSV
hsv_max = np.array((160, 255, 255), np.uint8) # верxняя граница зеленого в HSV

while True:  

    flag, img = cap.read() # считываем изо6ражение
    height, width = img.shape[:2] # размеры изо6ражения
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV ) # прео6разуем RGB к HSV 
    # накладываем маску и применяем ее
    thresh = cv2.inRange(hsv, hsv_min, hsv_max)
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
 

    if len(cnts) > 0:
		# поиск наи6ольIIIего контура
        c = max(cnts, key = cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
        if radius > 50:
			# рисуем окружность в центре фигуры
            cv2.circle(img, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
            cv2.circle(img, center, 5, (0, 0, 255), -1)
            
            ObjectPosition(int(x), int(y))
            ServoPosition (int(x), int(y))


    cv2.imshow('result', img) 

    ch = cv2.waitKey(5) # выxод через escp
    if ch == 27:
        break
    time.sleep(0.02) # временная задержка, что6ы из6авиться от осциляции 

cap.release()
cv2.destroyAllWindows()