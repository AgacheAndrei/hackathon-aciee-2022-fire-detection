from collections import deque
from imutils.video import VideoStream
import numpy as np
import cv2
import argparse
import time
import imutils
import threading   # Library for threading -- which allows code to run in backend
import playsound   # Library for alarm sound
import smtplib     # Library for email sending
#import pywhatkit
import os
from twilio.rest import Client

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

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="Path to the (optional) video file")
ap.add_argument("-b", "--buffer", default=64, type=int, help="max buffer size")
args = vars(ap.parse_args())


#cv2.namedWindow("Tracking")

greenLower =(0,0,255)
greenUpper = (100,208,255)
pts = deque(maxlen=args["buffer"])

if not args.get("video", False):
    vs = VideoStream(src=0).start()
else:
    vs = cv2.VideoCapture(args["video"])

time.sleep(2.0)

runOnce=False
trimis=False
while True:
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame
    if frame is None:
        break

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    print("Frame jumate" + (str)(frame/2))
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
            print("PRINT X= " +str(int(x)))
            print("PRINT Y= " +str(int(y)))
            text = "PRINT X= " +str(int(x))+"  "+"PRINT Y= " +str(int(y))
            coordinates = (40,50)
            coordinates2 = (40,80)
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255,0,255)
            thickness = 1
            if int(x) <255 and int(y)<255:
                frame = cv2.putText(frame, text, coordinates, font, fontScale, color, thickness, cv2.LINE_AA)
                frame = cv2.putText(frame, "stanga sus", coordinates2, font, fontScale, color, thickness, cv2.LINE_AA) 
            elif int(x) >255 and int(y)<255:
                frame = cv2.putText(frame, text, coordinates, font, fontScale, color, thickness, cv2.LINE_AA)
                frame = cv2.putText(frame, "dreapta sus", coordinates2, font, fontScale, color, thickness, cv2.LINE_AA) 
            elif int(x) <255 and int(y)>255:
                frame = cv2.putText(frame, text, coordinates, font, fontScale, color, thickness, cv2.LINE_AA)
                frame = cv2.putText(frame, "stanga jos", coordinates2, font, fontScale, color, thickness, cv2.LINE_AA) 
            elif int(x) >255 and int(y)>255:
                frame = cv2.putText(frame, text, coordinates, font, fontScale, color, thickness, cv2.LINE_AA) 
                frame = cv2.putText(frame, "dreapta jos", coordinates2, font, fontScale, color, thickness, cv2.LINE_AA)        
        print("Fire alarm initiated")
        #threading.Thread(target=play_alarm_sound_function).start()  # To call alarm thread
        trimis=False
        if runOnce == False and trimis==False :
            print("Mail send initiated")
            threading.Thread(target=send_mail_function).start() # To call alarm thread
            #pywhatkit.sendwhatmsg_instantly('+40757214117','Alerta foc gogule!')
            send_text_message('+40787429589','Alerta foc gogule!!!')
            apel('+40787429589')
            runOnce = True
            trimis=True
        if runOnce == True:
            print("Mail is already sent once")
            runOnce = True 
    pts.append(center)

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

cv2.destroyAllWindows()