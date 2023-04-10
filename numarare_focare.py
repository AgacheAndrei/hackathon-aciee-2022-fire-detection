import numpy as np
import cv2      # Library for openCV
import threading   # Library for threading -- which allows code to run in backend
import playsound   # Library for alarm sound
import smtplib     # Library for email sending
#import pywhatkit
import os
from twilio.rest import Client
from datetime import datetime
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
# Capturing video through webcam
webcam = cv2.VideoCapture(0)
runOnce=False
trimis=False
# Start a while loop
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
count=0
while(1):
    Alarm_Status = False
    # Reading the video from the
    # webcam in image frames
    _, imageFrame = webcam.read()

    # Convert the imageFrame in
    # BGR(RGB color space) to
    # HSV(hue-saturation-value)
    # color space
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # Set range for red color and
    # define mask
    # red_lower = np.array([136, 87, 111], np.uint8)
    # red_upper = np.array([180, 255, 255], np.uint8)
    # red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    # Set range for red1 color and
    # define mask
    red1_lower = np.array([0, 0, 255], np.uint8)
    red1_upper = np.array([100, 208, 255], np.uint8)
    red1_mask = cv2.inRange(hsvFrame, red1_lower, red1_upper)

    # Set range for blue color and
    # define mask
    #blue_lower = np.array([94, 80, 2], np.uint8)
    #blue_upper = np.array([120, 255, 255], np.uint8)
    #blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")

    # For red color
    # red_mask = cv2.dilate(red_mask, kernal)
    # res_red = cv2.bitwise_and(imageFrame, imageFrame,
    #                           mask = red_mask)

    #For red1 color
    red1_mask = cv2.dilate(red1_mask, kernal)
    res_red1 = cv2.bitwise_and(imageFrame, imageFrame,
                                mask = red1_mask)

    # For blue color
    #blue_mask = cv2.dilate(blue_mask, kernal)
    #res_blue = cv2.bitwise_and(imageFrame, imageFrame,
                               #mask = blue_mask)

    # Creating contour to track red color
    # contours, hierarchy = cv2.findContours(red_mask,
    #                                        cv2.RETR_TREE,
    #                                        cv2.CHAIN_APPROX_SIMPLE)

    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if(area > 300):
    #         x, y, w, h = cv2.boundingRect(contour)
    #         imageFrame = cv2.rectangle(imageFrame, (x, y),
    #                                    (x + w, y + h),
    #                                    (0, 0, 255), 2)

    #         cv2.putText(imageFrame, "FOC", (x, y),
    #                     cv2.FONT_HERSHEY_SIMPLEX, 1.0,
    #                     (0, 0, 255))

    # Creating contour to track green color
    contours, hierarchy = cv2.findContours(red1_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    count=0
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        
        #area pentru focuri care nu sunt periculoase, pe cele mici chiar le evita
        if(area > 400):
            count+=1
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y),
                                       (x + w, y + h),
                                       (0, 255, 0), 2)

            cv2.putText(imageFrame, "FOC"+" "+str(count) , (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (0, 255, 0))
            cv2.putText(imageFrame, str(area/100)+"%", (x, y-30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (0, 255, 0))
        if(area>1000): 
            if runOnce == False and trimis==False :
                count=count+1
                print("Mail send initiated")
                threading.Thread(target=send_mail_function).start() # To call alarm thread
                #pywhatkit.sendwhatmsg_instantly('+40757214117','Alerta foc gogule!')
                send_text_message('+40787429589','Alerta foc gogule!!!')
                apel('+40787429589')
                runOnce = True
                trimis=True
                now=datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                data = {"Timp":dt_string, "Tip Alarma":"SMS focar"}
                #database.push(data)
                database.child("Alarme focar").push(data)
                data = {"Timp":dt_string, "Tip Alarma":"Apel focar"}
                database.child("Alarme focar").push(data)
                data = {"Timp":dt_string, "Tip Alarma":"Email focar"}
                database.child("Alarme focar").push(data)
                
            if runOnce == True:
                print("Mail is already sent once")
                runOnce = True
                count=count+1
                

    # # Creating contour to track blue color
    # contours, hierarchy = cv2.findContours(blue_mask,
    #                                        cv2.RETR_TREE,
    #                                        cv2.CHAIN_APPROX_SIMPLE)
    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if(area > 300):
    #         x, y, w, h = cv2.boundingRect(contour)
    #         imageFrame = cv2.rectangle(imageFrame, (x, y),
    #                                    (x + w, y + h),
    #                                    (255, 0, 0), 2)

    #         cv2.putText(imageFrame, "Blue Colour", (x, y),
    #                     cv2.FONT_HERSHEY_SIMPLEX,
    #                     1.0, (255, 0, 0))

    # Program Termination
    cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break