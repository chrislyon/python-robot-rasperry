#necessite la fonction gpio WiringPi
set -x

## Moteur 1
moteur_1_setup()
{
    gpio -g mode 25 pwm 10
    gpio -g mode 18 out 
    gpio -g mode 23 out 
}

moteur_1_avance()
{
    gpio -g write 18 1
    gpio -g write 23 0
    gpio -g pwm 25 30
}

moteur_1_stop()
{
    gpio -g write 18 0
}

## Moteur 2
moteur_2_setup()
{
    gpio -g mode 17 pwm 10
    gpio -g mode 22 out 
    gpio -g mode 24 out 
}

moteur_2_avance()
{
    gpio -g write 22 1
    gpio -g write 24 0
    gpio -g pwm 17 30
}

moteur_2_stop()
{
    gpio -g write 22 0
}

gpio reset
moteur_1_setup
#moteur_2_setup
moteur_1_avance
sleep 1
#moteur_2_avance
sleep 1
moteur_1_stop
#moteur_2_stop
