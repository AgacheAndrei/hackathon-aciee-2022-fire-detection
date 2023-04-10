from collections import deque
from imutils.video import VideoStream
import numpy as np
import cv2
import argparse
import time
import imutils
import os
import RPi.GPIO as GPIO
from datetime import datetime
# GPIO.setmode(GPIO.BOARD)
# 
# GPIO.setwarnings(False)
# 
# GPIO.setup(11,GPIO.OUT)
# panServo = GPIO.PWM(11,50)
# GPIO.setup(12,GPIO.OUT)
# tiltServo = GPIO.PWM(12,50)
# 
# panServo.start(0)
# tiltServo.start(0)

# Library for openCV
import threading   # Library for threading -- which allows code to run in backend
import playsound   # Library for alarm sound
import smtplib     # Library for email sending
#import pywhatkit
import os
from twilio.rest import Client
import pyrebase

config = {

    "apiKey": "AIzaSyALS4mlqo9JRESijz7fxlSsBCX21eId6y0",
    "authDomain": "pufuletii-e0ed3.firebaseapp.com",
    "databaseURL": "https://pufuletii-e0ed3-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "pufuletii-e0ed3",
    "databaseURL":"https://pufuletii-e0ed3-default-rtdb.europe-west1.firebasedatabase.app/",
    "storageBucket": "pufuletii-e0ed3.appspot.com",
    "messagingSenderId": "413670163869",
    "appId": "1:413670163869:web:6aeabd5eb1790b43609b74",
    "measurementId": "G-RJX9VJHK1J"
}
firebase = pyrebase.initialize_app(config)
database = firebase.database()
def send_text_message(destination: str,message: str):
    account_sid ='ACe756a124e3127844059c5d0cc2b747a9'
    auth_token ='b8715de16ee19a718e7f7784fc34cc5e'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
      body=message,
      from_='+13854752620',
      to=destination
    )
    print(message.sid)
def apel(destination: str):
    account_sid ='ACe756a124e3127844059c5d0cc2b747a9'
    auth_token ='b8715de16ee19a718e7f7784fc34cc5e'
    client = Client(account_sid, auth_token)
    call=client.calls.create(
        url='http://demo.twilio.com/docs/voice.xml',
        to=destination,
        from_='+13854752620'
        )
def send_mail_function(): # defined function to send mail post fire detection using threading
    
    recipientmail = "agacheandrei09@yahoo.com" # recipients mail
    recipientmail = recipientmail.lower() # To lower case mail
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("pufos.pufosi2022@gmail.com", 'dwupwobwaavscohr') # Senders mail ID and password
        server.sendmail("agacheandrei09@yahoo.com",recipientmail, "Warning fire accident has been reported") # recipients mail with mail message
        print("Alert mail sent sucesfully to {}".format(recipientmail)) # to print in consol to whome mail is sent
        server.close() ## To close server
        
    except Exception as e:
        print(e) # To print error if an
panServo = 27 
tiltServo = 17

#position servos 
def positionServo (servo, angle):
    os.system("python angleServoCtrl.py " + str(servo) + " " + str(angle))
    print("[INFO] Positioning servo at GPIO {0} to {1} degrees\n".format(servo, angle))

# position servos to present object at center of the frame
def mapServoPosition (x, y):
    global panAngle
    global tiltAngle
    if (x < 220):
        panAngle += 5
        if panAngle > 140:
            panAngle = 140
        positionServo (panServo, panAngle)
 
    if (x > 280):
        panAngle -= 5
        if panAngle < 40:
            panAngle = 40
        positionServo (panServo, panAngle)

    if (y < 160):
        tiltAngle += -5
        if tiltAngle > 140:
            tiltAngle = 140
        positionServo (tiltServo, tiltAngle)
 
    if (y > 210):
        tiltAngle -= -5
        if tiltAngle < 40:
            tiltAngle = 40
        positionServo (tiltServo, tiltAngle)
        
# Initialize angle servos at 90-90 position
global panAngle
panAngle = 90
global tiltAngle
tiltAngle =90

# positioning Pan/Tilt servos at initial position
positionServo (panServo, panAngle)
positionServo (tiltServo, tiltAngle)

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="Path to the (optional) video file")
ap.add_argument("-b", "--buffer", default=64, type=int, help="max buffer size")
args = vars(ap.parse_args())

greenLower =(0,0,255)
greenUpper = (100,208,255)
pts = deque(maxlen=args["buffer"])



if not args.get("video", False):
    vs = VideoStream(src=0).start()
else:
    vs = cv2.VideoCapture(0)
    vs.set(cv2.CAP_PROP_FPS,40)
    fps = int(vs.get(5))
    print (fps)

#time.sleep(2.0)

runOnce=False
trimis=False
while True:
    frame = vs.read()
#merge si fara asta     f
    frame = cv2.flip(frame,-1)
    frame = frame[1] if args.get("video", False) else frame
    if frame is None:
        break
    frame = imutils.resize(frame, width=500)
    frame = imutils.rotate(frame, angle=180)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    bgr = cv2.cvtColor(blurred, cv2.COLOR_HSV2BGR)


    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M['m10']/M['m00']), int(M['m01']/M['m00']))

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 0), -1)
            mapServoPosition(int(x), int(y))
            if runOnce == False and trimis==False :
                print("Mail send initiated")
                threading.Thread(target=send_mail_function).start() # To call alarm thread
                #pywhatkit.sendwhatmsg_instantly('+40757214117','Alerta foc gogule!')
                send_text_message('+40787429589','Alerta foc gogule!!!')
                apel('+40787429589')
                runOnce = True
                trimis=True
                now=datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                data = {"Timp":dt_string, "Tip Alarma":"SMS track"}
                #database.push(data)
                database.child("Alarme track").push(data)
                data = {"Timp":dt_string, "Tip Alarma":"Apel track"}
                database.child("Alarme track").push(data)
                data = {"Timp":dt_string, "Tip Alarma":"Email track"}
                database.child("Alarme track").push(data)
            if runOnce == True:
                print("Mail is already sent once")
                runOnce = True

            
    pts.append(center)
#coditele
    for i in range(1, len(pts)):
        if pts[i-1] is None or pts[i] is None:
            continue

        thickness = int(np.sqrt(args["buffer"] / float(i+1)) * 2.5)
        cv2.line(frame, pts[i-1], pts[i], (20, 247, 255), thickness)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

if not args.get("video", False):
    vs.stop()
else:
    vs.release()

positionServo (panServo, 90)
positionServo (tiltServo, 90)
GPIO.cleanup()
cv2.destroyAllWindows()
