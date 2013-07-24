#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import shlex
import time
import pudb

## -------------------------------------
## CLASSE ROBOT
## -------------------------------------

class Robot(object):
    """
    Classe Robot
        A des moteurs (un droit et un gauche)
        d'autres peripherique a venir
        va recevoir des ordres
        AVANCE / TOURNE A GAUCHE (Angle ?) / TOURNE A DROITE
        STOP / VITESSE x% etc ..
    """
    def __init__(self, name):
        self.name = name
        self.rasperry = RASPERRY()
        self.moteur_gauche = None
        self.moteur_droit = None
        self.vitesse = 0
        self.sens = Motor.HO
        self.moving = False
        self.online = False
        self.test = False
        self.ficlog = sys.stdout

    def status(self):
        r = ""
        r += "\n"
        r += "-" * 70
        r += "\n"
        r += "Robot %s / ONLINE %s / MOVING %s / TEST %s " % (self.name, self.online, self.moving, self.test)
        r += "\n"
        r += "-" * 70
        r += "\n"
        r += "%30s" % self.moteur_droit.name
        r += "%30s" % self.moteur_gauche.name
        r += "\n"
        r += "%10s %10s %10s" % ('Speed', 'Sens', 'Enable')
        r += "%10s %10s %10s" % ('Speed', 'Sens', 'Enable')
        r += "\n"
        r += "%10s %10s %10s" % self.moteur_droit.status()
        r += "%10s %10s %10s" % self.moteur_gauche.status()
        r += "\n"
        r += "-" * 70
        r += "\n"
        return r

    def log(self, msg):
        print >> self.ficlog, "%s" % msg

    def initialise(self):
        self.log("Debut Initialisation")
        ## Moteur 1
        self.log("Soft Init moteur 1")
        self.moteur_droit = Motor('Moteur Droit', RASPERRY.RASP_SET1[0], RASPERRY.RASP_SET1[1], RASPERRY.RASP_SET1[2] ) 
        ## Moteur 2
        self.log("Soft Init moteur 2")
        self.moteur_gauche = Motor('Moteur Gauche', RASPERRY.RASP_SET2[0], RASPERRY.RASP_SET2[1], RASPERRY.RASP_SET2[2] )
        ## Fin
        self.log("Fin initialisation")

    ## ----------------------
    ## Gestion des commandes
    ## ----------------------
    def commande(self, ligne):
        """
            Recoit une ligne traduit cela en token
            puis execute la commande
        """
        lexer = shlex.shlex(ligne)
        ## Pour l'instant je n'ai que des commandes avec 
        ## un seul argument
        ## Mais il y a aussi de commandes sans arg
        cmd = lexer.get_token()
        arg = [ x for x in lexer ]
        self.log( "ORDRE : %s arg = %s " % (cmd, arg) )
        if cmd == "SET":
            return self.do_set(arg)
        elif cmd == "STATUS":
            return self.do_status()

        ## Pour les commandes suivantes le robot doit etre ONLINE
        if not self.online:
            return ('KO', 'Robot is not online')
        else:
            if cmd == "START":
                return self.do_start()
            elif cmd == "STOP":
                return self.do_stop()
            elif cmd == "AVANCE":
                return self.do_avance()
            elif cmd == "RECULE":
                return self.do_recule()
            elif cmd == "SENS":
                return self.do_sens(arg)
            elif cmd == "SPEED":
                return self.do_speed(arg)
            elif cmd == "CYCLE":
                return self.do_cycle(arg)
            elif cmd == "DROITE":
                return self.do_droite()
            elif cmd == "GAUCHE":
                return self.do_gauche()
            elif cmd == "DIRECTION":
                return self.do_direction()
            else:
                self.log("Commande inexistante : %s " % ligne )
                return ('KO', 'Commande inexistante')
        
    ## --------------
    ## Commandes 
    ## --------------
    def dummy_cmd(self):
        """
        Commande non implementee
        """
        return ('KO', 'NOT IMPLEMENTED')

    def do_set_online(self):
        """
        Met le robot Online = prepare les moteurs
        """
        for m in (self.moteur_droit, self.moteur_gauche):
            m.Hard_Init()
        self.online = True
        return ('OK', 'ONLINE')

    def do_set_offline(self):
        """
        Met le robot offline et nettoie les GPIO
        """
        for m in (self.moteur_droit, self.moteur_gauche):
            m.enable = False
        self.rasperry.GPIO_cleanup()
        self.online = False
        return ('OK', 'OFFLINE')

    def do_set_test(self, bool):
        """
           Bascule en mode test 
            Test = True : les commandes Hard ne passent pas
            Test = False : Les commandes hard passent 
        """
        for m in (self.moteur_droit, self.moteur_gauche):
            m.test = bool
        self.test = bool
        return ('OK', 'SET TEST %s' % bool )

    def do_set(self,arg):
        """
        La commande SET <arg> <opt>
        """
        self.log("Cmd : %s / %s" % ("SET", arg))
        if arg[0] == "ROBOT":
            if arg[1] == "ONLINE":
                r = self.do_set_online()
            elif arg[1] == "OFFLINE":
                r = self.do_set_offline()
            else:
                r = ('KO', 'SET ROBOT %s error' % arg[1] )
        elif arg[0] == 'TEST':
            if arg[1] == 'TRUE':
                r = self.do_set_test(True)
            elif arg[1] == 'FALSE':
                r = self.do_set_test(False)
            else:
                r = ('KO', 'SET TEST %s error' % arg[1])
        else:
            r = ('KO', 'SET %s INEXISTANT' % arg)
        return r

    def do_status(self):
        """
        La commande de status 
        return une string formatte
        """
        self.log("Cmd : STATUS")
        return ('OK', self.status() )

    def do_start(self):
        """
        Commande start
        On demarre 
        """
        self.log("Cmd : START")
        if not self.vitesse:
            self.vitesse = RASPERRY.SPEED_MIN
        for m in (self.moteur_droit, self.moteur_gauche):
            m.set_sens(self.sens)
            m.set_speed(self.vitesse)
            m.start()
        self.moving = True
        return ( 'OK', 'START' )

    def do_stop(self):
        """
            Commande STOP
            arret du robot
        """
        self.log("Cmd : STOP")
        self.vitesse = 0
        for m in (self.moteur_droit, self.moteur_gauche):
            m.set_speed(self.vitesse)
            m.stop()
        self.moving = False
        return ( 'OK', 'STOP' )

    def do_avance(self):
        self.log("Cmd : AVANCE")
        return self.dummy_cmd()

    def do_recule(self):
        return self.dummy_cmd()

    def do_sens(self, arg):
        self.log("Cmd : %s / %s" % ("SENS", arg))
        if arg[0] == "AVANT":
            self.do_stop()
            for m in (self.moteur_droit, self.moteur_gauche):
                m.set_sens(Motor.HO)
            self.sens = Motor.HO
            self.do_start()
        elif arg[0] == "ARRIERE":
            self.do_stop()
            for m in (self.moteur_droit, self.moteur_gauche):
                m.set_sens(Motor.AH)
            self.sens = Motor.AH
            self.do_start()
        else:
            return ('KO', 'SENS ERROR %s ' % arg[0])
        return ('OK', "SENS %s " % arg[0] )

    def do_speed(self, arg):
        self.log("Cmd : %s / %s" % ("SPEED", arg))
        if arg[0] == 'MIN':
            self.vitesse = RASPERRY.SPEED_MIN
            if self.moving:
                self.do_start()
        elif arg[0] == 'MED':
            self.vitesse = RASPERRY.SPEED_MED
            if self.moving:
                self.do_start()
        elif arg[0] == 'MAX':
            self.vitesse = RASPERRY.SPEED_MAX
            if self.moving:
                self.do_start()
        else:
            return ('KO', 'SPEED ERROR %s ' % arg)
        return ('OK', 'SPEED %s' % self.vitesse )

    def do_cycle(self, arg):
        self.log("Cmd : %s / %s" % ("CYCLE", arg))
        return self.dummy_cmd()

    def do_droite(self):
        self.log("Cmd : DROITE")
        return self.dummy_cmd()

    def do_gauche(self):
        self.log("Cmd : GAUCHE")
        return self.dummy_cmd()

    def do_direction(self, arg):
        self.log("Cmd : %s / %s" % ("DIRECTION", arg))
        return self.dummy_cmd()

## ------------------------
## LANCEMENT DES TESTS
## ------------------------

def test():
    R = Robot("R1")
    R.initialise()
    #print R.status()
    print "STATUS    : ", R.commande("STATUS")[1]
    print "SET TEST TRUE : ", R.commande("SET TEST TRUE")
    print "SET TEST FALSE : ", R.commande("SET TEST FALSE")
    print "SET ROBOT ONLINE : ", R.commande("SET ROBOT ONLINE")
    print "START     : ", R.commande("START")
    print "STATUS    : ", R.commande("STATUS")[1]
    #print "GAUCHE    : ", R.commande("GAUCHE")
    time.sleep(2)
    print "SPEED_MED : ", R.commande("SPEED MED")
    print "STATUS    : ", R.commande("STATUS")[1]
    time.sleep(2)
    print "SPEED_MAX : ", R.commande("SPEED MAX")
    print "STATUS    : ", R.commande("STATUS")[1]
    time.sleep(2)
    print "SPEED_MIN : ", R.commande("SPEED MIN")
    print "STATUS    : ", R.commande("STATUS")[1]
    time.sleep(2)
    print "SENS_ARRIERE : ", R.commande("SENS ARRIERE")
    print "STATUS    : ", R.commande("STATUS")[1]
    time.sleep(2)
    print "STOP      : ", R.commande("STOP")
    print "SET ROBOT OFFLINE : ", R.commande("SET ROBOT OFFLINE")
    print "STATUS    : ", R.commande("STATUS")[1]

if __name__ == "__main__":
        test()
