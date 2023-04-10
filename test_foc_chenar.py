import cv2         # Library for openCV
import threading   # Library for threading -- which allows code to run in backend
import playsound   # Library for alarm sound
import smtplib     # Library for email sending
#import pywhatkit
import os
from twilio.rest import Client
#from datetime import datetime
#now=datetime.now()
#current_hour=now.strftime("%H")
#current_min=now.strftime("%M")
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


fire_cascade = cv2.CascadeClassifier('fire_detection_cascade_model.xml') # To access xml file which includes positive and negative images of fire. (Trained images)
                                                                         # File is also provided with the code.

vid = cv2.VideoCapture(0) # To start camera this command is used "0" for laptop inbuilt camera and "1" for USB attahed camera
runOnce = False # created boolean

# def play_alarm_sound_function(): # defined function to play alarm post fire detection using threading
#     playsound.playsound('/home/pufos/Desktop/hack2022/fire.mp3',True) # to play alarm # mp3 audio file is also provided with the code.
#     print("Fire alarm end") # to print in consol

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
        print(e) # To print error if any
		
while(True):
    Alarm_Status = False
    ret, frame = vid.read() # Value in ret is True # To read video frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # To convert frame into gray color
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5) # to provide frame resolution

    ## to highlight fire with square 
    for (x,y,w,h) in fire:
        cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
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

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break