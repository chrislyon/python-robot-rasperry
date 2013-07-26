
import Rasperry as RASP
import RPi.GPIO as GPIO

import time

## Attente
def attente(t=2):
    print "Attente : %s s" % t
    time.sleep(t)

## -------------------------------------
## CLASSE MOTEUR
## -------------------------------------
class Motor(object):
    """
    Classe Motor
        Composante d'un robot
        elle est commande par le robot
    """

    def __init__(self, name, PWM, IN1, IN2):
        self.name = name
        self.test = False
        self.vitesse = 0
        self.online = False
        self.GPIO_PWM = PWM
        self.GPIO_IN1 = IN1
        self.GPIO_IN2 = IN2
        self.pwm = None

    def __str__(self):
        return "%s[%02d %02d %02d] v=%03d t=%s o=%s" % (self.name, self.GPIO_PWM, self.GPIO_IN1, self.GPIO_IN2, self.vitesse, self.test, self.online)

    def enable(self):
        self.online = True
        if not self.test:
            ## GPIO COMMAND
            ## ON passe les GPIO en OUT
            for gpio in (self.GPIO_PWM, self.GPIO_IN1, self.GPIO_IN2):
                ## GPIO COMMAND
                GPIO.setup(gpio, GPIO.OUT)
            self.pwm = GPIO.PWM( self.GPIO_PWM, RASP.PWM_FREQ )

    def disable(self):
            self.online = False
            for gpio in (self.GPIO_PWM, self.GPIO_IN1, self.GPIO_IN2):
                GPIO.output(gpio, False)

    def avance(self,vitesse=RASP.SPEED_MIN):
        GPIO.output(self.GPIO_IN1, GPIO.LOW)
        GPIO.output(self.GPIO_IN2, GPIO.HIGH)
        self.pwm.start(vitesse)
        self.vitesse = vitesse

    def recule(self,vitesse=RASP.SPEED_MIN):
        GPIO.output(self.GPIO_IN1, GPIO.HIGH)
        GPIO.output(self.GPIO_IN2, GPIO.LOW)
        self.pwm.start(vitesse)
        self.vitesse = vitesse

    def stop(self):
        GPIO.output(self.GPIO_IN1, GPIO.LOW)
        GPIO.output(self.GPIO_IN2, GPIO.LOW)
        self.pwm.stop()
        self.vitesse = 0

def test_m1():
    M = Motor( "Moteur 1", RASP.RASP_SET1[0], RASP.RASP_SET1[1], RASP.RASP_SET1[2] )
    print "Enable %s " % M
    M.enable()
    print "Avance %s " % M
    M.avance()
    attente()
    print "Stop %s " % M
    M.stop()
    print "Recule %s " % M
    M.recule()
    attente()
    print "Stop %s " % M
    M.stop()
    print "Disable %s " % M
    M.disable()

def test_m2():
    ## Moteur 2
    M = Motor( "Moteur 2", RASP.RASP_SET2[0], RASP.RASP_SET2[1], RASP.RASP_SET2[2] )
    print "Enable %s " % M
    M.enable()
    print "Avance %s " % M
    M.avance()
    attente()
    print "Stop %s " % M
    M.stop()
    print "Recule %s " % M
    M.recule()
    attente()
    print "Stop %s " % M
    M.stop()
    print "Disable %s " % M
    M.disable()
    
def test():
    #test_m1()
    test_m2()
    GPIO.cleanup()

if __name__ == '__main__':
    test()
