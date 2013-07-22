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


## Attente
def attente(t=2):
    print "Attente : %s s" % t
    time.sleep(t)


## Init
def init():
    for g in all:
        GPIO.setup(g, GPIO.OUT)
        print "Setting GPIO %s : OUT" % g


def av_1():
    print "Avance moteur 1"
    GPIO.output(en1, GPIO.LOW)
    GPIO.output(en2, GPIO.HIGH)
    p1.start(30)

def re_1():
    print "Recule moteur 1"
    GPIO.output(en1, GPIO.HIGH)
    GPIO.output(en2, GPIO.LOW)
    p1.start(30)

## Moteur 2
def av_2():
    print "Forward moteur 2"
    GPIO.output(en3, GPIO.LOW)
    GPIO.output(en4, GPIO.HIGH)
    p2.start(30)
  
## ======
## Main
## ======

init()

p1 = GPIO.PWM(pwm1, 50)
p2 = GPIO.PWM(pwm2, 50)

av_1()
attente()
p1.stop()


av_2()
attente()
p2.stop()

re_1()
attente()
p1.stop()

av_1()
attente()
p1.stop()
  
GPIO.cleanup()          # when your program exits, tidy up after yourself  
