  	

The SIM800 opens you the world for a many interesting communication projects. Some of them may be very useful and professional. Let you inspire and invent something special. In the following example the Raspberry Pi communicates via SMS.

Aim:
Turn your Raspberry Pi in a SMS Butler that returns an SMS with state information each time an SMS is received. (The Butler could be expanded to perform some useful actions when an SMS is received, e.g. to switch on/off the heater in a remote unoccupied winter residence and report the current room temperature.)

You may use a PuTTY terminal to play with the SMS commands manually. Do the following:
 Command (terminate with <cr>) 	 Reply : Meaning
 AT+CMGF=1 	 OK : Set the modem in text mode
 AT+CMGS="+41764331357" 	 > : Prepare to send to given phone number
 Have a good day!<^Z> 	 OK : Send text and terminate with Ctrl+Z
 Third incoming SMS 	 +CMTL: "SM", 3
 AT+CMGR=3 	 Show content of SMS #3
 AT+CMGDA="DEL ALL" 	 Delete all SMS

If the Raspberry Pi receives an SMS containing the text "getStatus", it sends an SMS with current time stamp and state of GPIO pin #24 to a certain phone number.

Program:[►]

Program:

# SIMSMS1.py

import RPi.GPIO as GPIO
import serial
import time, sys
import datetime

P_BUTTON = 24 # Button, adapt to your wiring

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(P_BUTTON, GPIO.IN, GPIO.PUD_UP)

SERIAL_PORT = "/dev/ttyAMA0"  # Raspberry Pi 2
#SERIAL_PORT = "/dev/ttyS0"    # Raspberry Pi 3

ser = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 5)
setup()
ser.write("AT+CMGF=1\r") # set to text mode
time.sleep(3)
ser.write('AT+CMGDA="DEL ALL"\r') # delete all SMS
time.sleep(3)
reply = ser.read(ser.inWaiting()) # Clean buf
print "Listening for incomming SMS..."
while True:
    reply = ser.read(ser.inWaiting())
    if reply != "":
        ser.write("AT+CMGR=1\r") 
        time.sleep(3)
        reply = ser.read(ser.inWaiting())
        print "SMS received. Content:"
        print reply
        if "getStatus" in reply:
            t = str(datetime.datetime.now())
            if GPIO.input(P_BUTTON) == GPIO.HIGH:
                state = "Button released"
            else:
                state = "Button pressed"
            ser.write('AT+CMGS="+41764331356"\r')
            time.sleep(3)
            msg = "Sending status at " + t + ":--" + state
            print "Sending SMS with status info:" + msg
            ser.write(msg + chr(26))
        time.sleep(3)
        ser.write('AT+CMGDA="DEL ALL"\r') # delete all
        time.sleep(3)
        ser.read(ser.inWaiting()) # Clear buf
    time.sleep(5)    

