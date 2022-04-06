from cmu_112_graphics import *
from tkinter import * 

#code to import image from CMU 15-112 page
#https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#getAndPutPixels
def drawImage(app):  
    url = 'https://static.wikia.nocookie.net/plantsvszombies/images/3/38/Background1.jpg/revision/latest/scale-to-width-down/1000?cb=20160502033025'
    app.image1 = app.loadImage(url)
    app.image2 = app.scaleImage(app.image1, 1)

    #https://external-preview.redd.it/lTULcYjzydX46Q0j5mIVcYzjWKMe8bfqxS_1DKrbwd4.png?auto=webp&s=e6bed987de0fe9273034911a812a4a30babfce40
    app.image3 = app.loadImage('board.png')
    app.image4 = app.scaleImage(app.image3, 1/3)

    #'https://static.wikia.nocookie.net/plantsvszombies/images/1/15/Night.png/revision/latest?cb=20200520163556'
    app.night1 = app.loadImage('Night.png')
    app.night2 = app.scaleImage(app.night1, 1)

    #https://www.techradar.com/news/gaming/how-to-win-at-plants-vs-zombies-1100259
    app.StartPage1 = app.loadImage('Starting Page.webp')
    app.StartPage2 = app.scaleImage(app.StartPage1, 8/9)

    #https://plantsvszombies.fandom.com/wiki/Sun?file=SunFA.png
    app.sun1 = app.loadImage('sun.png')
    app.sun2 = app.scaleImage(app.sun1, 2/3)

    #https://plantsvszombies.fandom.com/wiki/Shovel?file=Shovel2.png
    app.shovel1 = app.loadImage('shovel.png')
    app.shovel2 = app.scaleImage(app.shovel1, 3/15)

    #'https://plantsvszombies.fandom.com/wiki/Brain/Gallery?file=PvZ1ZombiesWon.png'
    app.lose1 = app.loadImage('lose.png')
    app.lose2 = app.scaleImage(app.lose1, 4/3)

    #all the images below from source: 
    #https://pvz-rp.fandom.com/wiki/Plants_vs._Zombies_2_Seed_Packets/Normal
    #https://pvz-rp.fandom.com/wiki/Plants_vs._Zombies_2_Seed_Packets/Normal?file=Sunflower_Seed_Packet.png
    app.sunflower = app.loadImage('Sunflower.png')
    app.sunflower2 = app.scaleImage(app.sunflower, 3/7)

    #https://pvz-rp.fandom.com/wiki/Plants_vs._Zombies_2_Seed_Packets/Normal?file=Peashooter_Seed_Packet.png
    app.peashooter = app.loadImage('Peashooter.png')
    app.peashooter2 = app.scaleImage(app.peashooter, 3/7)

    #https://pvz-rp.fandom.com/wiki/Plants_vs._Zombies_2_Seed_Packets/Normal?file=Wall-nut_Seed_Packet.png
    app.wallnut = app.loadImage('Wallnut.png')
    app.wallnut2 = app.scaleImage(app.wallnut, 3/7)

    #https://pvz-rp.fandom.com/wiki/Plants_vs._Zombies_2_Seed_Packets/Normal?file=Kernel-pult_Seed_Packet.png
    app.kernelpult = app.loadImage('Kernelpult.png')
    app.kernelpult2 = app.scaleImage(app.kernelpult, 3/7)

    #https://pvz-rp.fandom.com/wiki/Plants_vs._Zombies_2_Seed_Packets/Normal?file=Potato_Mine_Seed_Packet.png
    app.potatomine = app.loadImage('Potatomine.png')
    app.potatomine2 = app.scaleImage(app.potatomine, 3/7)

    app.cattail1 = app.loadImage('cattail.png')
    app.cattail2 = app.scaleImage(app.cattail1, 3/7)

    #https://hero.fandom.com/wiki/Sunflower?file=Sunflower+HD.png
    app.plant1 = app.loadImage('p1.png')
    app.p1 = app.scaleImage(app.plant1, 4/5)

    #https://www.redbubble.com/i/sticker/Peashooter-from-Plants-vs-Zombies-by-Jonnyman/27899095.EJUG5#&gid=1&pid=3
    app.plant2 = app.loadImage('p2.png')
    app.p2 = app.scaleImage(app.plant2, 4/5)

    #https://soundcloud.com/therealsomething/plants-vs-zombies-walnut-mini-game-theme-trap-remix
    app.plant3 = app.loadImage('p3.png')
    app.p3 = app.scaleImage(app.plant3, 4/5)

    #https://plantsvszombies.fandom.com/wiki/Kernel-pult/Gallery
    app.plant4 = app.loadImage('p4.png')
    app.p4 = app.scaleImage(app.plant4, 4/5)

    #https://www.deviantart.com/illustation16/art/Plants-vs-Zombies-2-Potato-Mine-451312893
    app.plant5 = app.loadImage('p5.png')
    app.p5 = app.scaleImage(app.plant5, 4/5)

    #https://plantsvszombies.fandom.com/wiki/Cattail?file=Cattail2009HD.png
    app.cat1 = app.loadImage('cat.png')
    app.cat2 = app.scaleImage(app.cat1, 4/5)

    #link of the potatoMineInit and potatoMineExplode are below:
    #https://plantsvszombies.fandom.com/wiki/Potato_Mine/Gallery?file=UnarmedPotatoMine.png
    app.potato = app.loadImage('potatoMineInit.png')
    app.p51 = app.scaleImage(app.potato, 4/5)

    app.potatoMineEx = app.loadImage('potatoMineExplode.png')
    app.p52 = app.scaleImage(app.potatoMineEx, 4/5)

    #https://custom-cursor.com/en/collection/plants-vs-zombies/pvz-cattail
    app.cattailBullet = app.loadImage('spike.png')
    app.catBullet = app.scaleImage(app.cattailBullet, 1)


    #zombie images 
    #https://static.wikia.nocookie.net/villains/images/8/8c/Zombie1plant.png/revision/latest?cb=20180629011517
    app.normal = app.loadImage('zombie.png')
    app.normal2 = app.scaleImage(app.normal, 4/5)

    #https://plantsvszombies.fandom.com/wiki/Conehead_Zombie?file=Conehead2009HD.png
    app.conehead = app.loadImage('conehead.png')
    app.conehead2 = app.scaleImage(app.conehead, 4/5)

    #https://plantsvszombies.fandom.com/wiki/Buckethead_Zombie/Gallery
    app.buckethead = app.loadImage('buckethead.png')
    app.buckethead2 = app.scaleImage(app.buckethead, 4/5)

    #zombie images eating
    #images taken from the screenshots of this video: https://www.youtube.com/watch?v=zvqAXpSRUUM
    app.normalEat = app.loadImage('zombieEat.png')
    app.normalEat2 = app.scaleImage(app.normalEat, 4/5)

    app.coneEat = app.loadImage('coneheadEat.png')
    app.coneEat2 = app.scaleImage(app.coneEat, 4/5)

    app.bucketEat = app.loadImage('bucketheadEat.png')
    app.bucketEat2 = app.scaleImage(app.bucketEat, 4/5)
  
    