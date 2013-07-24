import RPi.GPIO as GPIO


## Mode BCM (numerotation des GPIO ?)
GPIO.setmode(GPIO.BCM)

## Evite les messages GPIO Already in use
GPIO.setwarnings(False)

SPEED_MIN = 20
SPEED_MED = 40
SPEED_MAX = 80

PWM_FREQ = 50

RASP_SET1 = (25, 18, 23)
RASP_SET2 = (17, 22, 27)

def GPIO_cleanup(self):
    ## GPIO COMMAND
    GPIO.cleanup()

