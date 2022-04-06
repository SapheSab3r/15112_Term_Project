from cmu_112_graphics import *
from tkinter import * 
import random

#zombie images url:
#normal: https://villains.fandom.com/wiki/Zombies_(Plants_vs._Zombies)
#conehead: https://plantsvszombies.fandom.com/wiki/Conehead_Zombie?file=Conehead2009HD.png
#buckethead: https://static.wikia.nocookie.net/plantsvszombies/images/f/fb/Buckethead_Zombie.png/revision/latest?cb=20170407151116


#Constant Values
normalHealth = 100
coneheadHealth = 200
bucketHealth = 300
speed = 7


def addZombies(app):
    health = 0 
    zType = ''

    if app.zombieType == 1:
        zType = app.normal2
        attack = 10
        health = normalHealth

    elif app.zombieType == 2:
        zType = app.conehead2
        attack = 10
        health = coneheadHealth

    elif app.zombieType == 3:
        zType = app.buckethead2
        attack = 10
        health = bucketHealth

    return (health, zType) 


    