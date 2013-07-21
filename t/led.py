#!/usr/bin/env python
# -*- coding: latin-1 -*-

import RPi.GPIO as GPIO, time

DEBUG = 1

LED_PAUSE = 2 # temps de pause en seconde
STATE = 0     # conteint RED_LED ou GREEN_ en fonction de la LED Actuellement allumée

GPIO.setmode(GPIO.BCM)
GREEN_LED = 18
RED_LED = 23
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)

while True:

        if DEBUG:
                print "."

        if STATE == RED_LED:
                # Si LED Rouge Allumée... l'éteindre et allumer la verte
                GPIO.output(GREEN_LED, True)
                GPIO.output(RED_LED, False)
                STATE = GREEN_LED
        else:
                # Si LED Verte Allumée... l'éteindre et allumer la rouge  
                GPIO.output(GREEN_LED, False)
                GPIO.output(RED_LED, True)
                STATE = RED_LED

        time.sleep(LED_PAUSE)
