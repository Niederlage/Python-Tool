#!/usr/bin/env python

import RPI.GPIO as GPIO
import time
import signal
import atexit

atexit.register(GPIO.cleanup)

servopin=23
GPIO.setmode(GPIO.BCM)
GPIO.setup(servopin,GPIO.OUT,initial=False)
p=GPIO.PWM(servopin,50)
p.start(0)
time.sleep(2)

while(True):
   for i in range(0,360,10):
       p.ChangeDutyCycle(12.5-5*i/360)
       time.sleep(1)
   for i in  range(0,360,10):
        p.ChangeCutyCycle(7.5-5*i/360)
        time.sleep(1)
