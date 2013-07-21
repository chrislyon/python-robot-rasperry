# Don't try to run this as a script or it will all be over very quickly  
# it won't do any harm though.  
# these are all the elements you need to control PWM on 'normal' GPIO ports  
# with RPi.GPIO - requires RPi.GPIO 0.5.2a or higher  
  
import RPi.GPIO as GPIO # always needed with RPi.GPIO  
import time
  
GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM  

pwm1 = 25
pwm2 = 17

en1 = 18
en2 = 23

en3 = 22
en4 = 27

all  = (pwm1, pwm2, en1, en2, en3, en4)

for g in all:
    GPIO.setup(g, GPIO.OUT)
    print "Setting GPIO %s : OUT" % g

## Moteur 1
print "Enable moteur 1"
GPIO.output(en1, GPIO.LOW)
GPIO.output(en2, GPIO.HIGH)
p1 = GPIO.PWM(pwm1, 50)    # create an object p for PWM on port at 50 Hertz  
                        # you can have more than one of these, but they need  
                        # different names for each port   
                        # e.g. p1, p2, motor, servo1 etc.  
  
p1.start(50)             # start the PWM on 50 percent duty cycle  
                        # duty cycle value can be 0.0 to 100.0%, floats are OK  


## Moteur 2
print "Enable moteur 1"
GPIO.output(en3, GPIO.LOW)
GPIO.output(en4, GPIO.HIGH)
p2 = GPIO.PWM(pwm2, 50)
p2.start(50)
  
print "Attente"
time.sleep(10)
  
p1.stop()                # stop the PWM output  
p2.stop()
  
GPIO.cleanup()          # when your program exits, tidy up after yourself  
