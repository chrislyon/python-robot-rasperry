#Liste des ordres

# Introduction #

Liste les ordres prevus ou a venir pour le robot


# Details #

```

SET DEFAULT
        Met les valeurs par defaut 
                SPEED MIN
                SENS AVANT

SENS <AVANT|ARRIERE>

AVANCE
        Si ROBOT EN MOUVEMENT
                STOP
        SPEED MIN
        SENS AVANT
        START

RECULE
        Si ROBOT EN MOUVEMENT
                STOP
        SPEED MIN
        SENS ARRIERE
        START

SPEED   <SPEED> <MIN> <MED> <MAX>
        Change la vitesse
        MIN = 10%
        MED = 40%
        MAX = 80%

CYCLE   <CYCLE>
        Change la frequence du cycle PWM
        Default 50

GAUCHE  <ANGLE>
        Modifie les vitesses pour effectuer un virage a gauche

DROITE  <ANGLE>
        Modifie les vitesses pour effectuer un virage a droite

STOP
        Arrete le robot
        Decremente la vitesse jusqu'a 0

START
        Demarre le robot
        Incremente la vitesse jusqu'a VITESSE

DIRECTION <ANGLE>
        Changement de direction
```