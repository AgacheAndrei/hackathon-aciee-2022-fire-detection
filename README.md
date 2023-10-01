# The hackathon Aciee 2022 🤖
## The problem to solve fire detection in a warehouse 🔥🔥🔥
**Here is all the code except the website (another membero of the team build it)**
<br>
**! 48 hours to resolve this problem !**
### Solution
### Programing languages and technology used

<img align="left" width="30px" style="padding-right:10px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" /> 
<img align="left" width="30px" style="padding-right:10px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/opencv/opencv-original.svg" />  

<br>
<br>
<p>A mobile system with a camera 🎥 for fire detection in a warehouse, alerting individuals through a mobile message📳, phone call📲, email📨, sound alarm🔊, and real-time notification. 
The data could be viewed on a website🕸️.
The system was a raspberry pi with a camara mounted on and the camera was moved using a small electric engine. To cool❄️ the system we used a small fan.
The system was able to move after the fire source if this was the case.
</p>

**The code for the fire detection was written in Python🐍 using advanced image manipulation to detect the fire**.
<br>
**The code for the movement of the camera was written in Python🐍**.
<br>
**The code for the system of alerts was written in Python🐍 I used Twilio for SMS and to call the number of the end user, for the sound alarm I used playsound and for the emails smtplib**.

### Libraries  for camera

<pre>
 import cv2
 imutils.video import VideoStream
</pre>

### Library for camera movement

<pre>
 RPi.GPIO
 </pre>
 
### Libraries for openCV
<pre>
 threading   # Library for threading -- which allows code to run in backend
 playsound   # Library for alarm sound
 smtplib     # Library for email sending
</pre>
### Library for twilio
 <pre>
 twilio.rest 
 </pre>



## Some photos from the project:
![307985187_655728812619160_174156980997263208_n](https://github.com/AgacheAndrei/hackathon-aciee-2022-fire-detection/assets/36128809/4cb0fb48-5d4d-49fa-a37d-6d636d941e0a)
![314083537_3314773368759563_6221691020969563081_n (1)](https://github.com/AgacheAndrei/hackathon-aciee-2022-fire-detection/assets/36128809/c62df5bd-9537-42c2-a756-7cd1087e4004)
![315112593_640100637810672_2142126775487418075_n (1)](https://github.com/AgacheAndrei/hackathon-aciee-2022-fire-detection/assets/36128809/4c75c39b-9143-463a-b157-699b03ad19d0)
![314622835_1092858694759078_4649768303309502003_n (1)](https://github.com/AgacheAndrei/hackathon-aciee-2022-fire-detection/assets/36128809/5848fdf2-554e-4ced-892a-8952cac30e60)
