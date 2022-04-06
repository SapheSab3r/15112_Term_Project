from cmu_112_graphics import *
from tkinter import * 
from zombies import * 
from images import * 
import math
import random 

def restart(app):
    #constant value 
    app.cols = 9
    app.rows = 5 
    app.marginX = 160
    app.marginY = 40 
    app.crossingLine = 140
    app.gap = 40
    app.cards = 5

    #game setting
    app.sun = 0 
    app.quit = False
    app.textAppear = True 
    app.releaseZombie = False
    app.shovelSelected = False
    app.paused = False 
    app.timer = 10
    app.timer0 = 0
    app.zombieCount = 20 
    app.zombieCountN = 30
    app.killCount = 0
    app.selected = False 
    app.shovelMoved = False
    app.attack = False 
    app.clicked = False
    app.result = {}

    #grid for scoring 
    app.scoreBoard = [[0] * app.cols for row in range(app.rows)]

    #grid for placing the plants
    app.board = [[[0]] * app.cols for row in range(app.rows)]

    #bullet radius 
    app.bR = 10

    #sun list 
    app.sunStore = []
    app.r = 20 
    app.sunX = -100
    app.sunY = -100

    #zombie list
    app.zombieList = []
    app.zombieX = app.width + 5
    app.zombieY = -100
    app.zombieType = 0 # get a zombie 
    
    #plant card store
    app.plantCard = 0
    app.cardSelected = False

    #projectile point 
    app.x = -1
    app.y = -1

    drawImage(app) 

def appStarted(app):
    restart(app)
    app.mode = 'startingMode'


#check the distance between two points 
def distance(x0, y0, x1, y1):
    return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
    
def getCells(app, x, y):
    width = app.width - app.marginX - app.gap
    height = app.height - app.marginY - 10

    cellWidth = width / app.cols 
    cellHeight = height / app.rows

    col = int((x - app.marginX) / cellWidth)
    row = int((y - app.marginY) / cellHeight)
    return row, col

def getCellBounds(app, row, col):
    width = app.width - app.marginX - app.gap
    height = app.height - app.marginY - 10

    cellWidth = width / app.cols 
    cellHeight = height / app.rows

    x0 = app.marginX + cellWidth * col
    y0 = app.marginY + cellHeight * row 
    x1 = app.marginX + cellWidth * (col + 1)
    y1 = app.marginY + cellHeight * (row + 1)
    return x0, y0, x1, y1 


def nightLevelMode_timerFired(app):
    if app.paused == True:
        return 

    elif app.killCount == 20:
        app.win = True  

    app.timer0 += app.timer

    if app.timer0 % 400 == 0:
        app.sunX = random.randint(app.marginX, app.width - app.r)
        app.sunY = random.randint(app.marginY, app.height - app.r)

        if len(app.sunStore) < 10:
            app.sunStore.append((app.sunX, app.sunY))

        elif len(app.sunStore) >= 10:
            app.sunStore.pop(0)
            app.sunStore.append((app.sunX, app.sunY)) 

    #produce sun from sunflower
    produceSun(app)
    
    #if a zombie is on the row, the plant can attack, else not 
    checkPlantAndZombieOnRow(app)
    checkCattailAndZombie(app)
                    
    #check if zombie collide with a bullet 
    checkForCollsion(app)
   
    #zombies move
    if app.timer0 >= 500:
        app.releaseZombie = True
        
    if app.releaseZombie == True and app.zombieCountN > 0:
        if app.timer0 % 200 == 0: 
            generateZombies(app)

    #zombie's action
    zombieActionAndState(app)

    #check if the bomb can explode 
    checkForReadyToExplosion(app)

def generateZombies(app):
    yposition = [77, 151, 225, 299, 373]
    for row in range(len(app.scoreBoard)):

        rowSun = sum(app.scoreBoard[row])

        if row not in app.result:
            app.result[row] = 0
        else:
            app.result[row] = rowSun

    if app.result[0] == app.result[1] == app.result[2] == app.result[3] == app.result[4]:    
        bestRow = random.choice(yposition)
        app.zombieType = random.randint(1, 3)
        app.zombieY = bestRow - 20
        health, zType = addZombies(app)

    
    elif app.result[1] == app.result[2] == app.result[3] == app.result[4]: 
        yposition = [151, 225, 299, 373]
        bestRow = random.choice(yposition)
        app.zombieType = random.randint(1, 3)
        app.zombieY = bestRow - 20
        health, zType = addZombies(app)

    elif app.result[2] == app.result[3] == app.result[4]:
        yposition = [225, 299, 373]
        bestRow = random.choice(yposition)
        app.zombieType = random.randint(1, 3)
        app.zombieY = bestRow - 20
        health, zType = addZombies(app)

    elif app.result[3] == app.result[4]:
        yposition = [299, 373]
        bestRow = random.choice(yposition)
        app.zombieType = random.randint(1, 3)
        app.zombieY = bestRow - 20
        health, zType = addZombies(app)

    else:
        bestRow = min(app.result, key = app.result.get)
        app.zombieType = random.randint(1, 3)
        app.zombieY = yposition[bestRow] - 20
        health, zType = addZombies(app)
    
    if len(app.zombieList) <= 10:
        app.zombieList.append([app.zombieX, app.zombieY, health, zType])
        app.zombieCount -= 1


def produceSun(app):
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            if app.board[row][col][0] == 1:
                app.board[row][col][4] += 1

                if app.board[row][col][4] % 10 == 0:
                    x0, y0, x1, y1 = getCellBounds(app, row, col)
                    halfX = (x1 - x0) / 2
                    halfY = (y1 - y0) / 2 + 10
                    app.sunStore.append((x0 + halfX, y0 + halfY))

def checkPlantAndZombieOnRow(app):
    for row in range(len(app.board)):
        for col in range(len(app.board[row])):
            for zombie in app.zombieList:
                if zombie[0] < app.width - app.gap:
                    zRow = zombie[0]
                    zCol = zombie[1]
                    r, c = getCells(app, zRow, zCol)

                    if r == row and c >= col: 
                        if app.board[row][col][0] == 2:
                            x0, y0, x1, y1 = getCellBounds(app, row, col)
                            halfX = (x1 - x0) / 2 + 22
                            halfY = (y1 - y0) / 2 - 12
                            app.board[row][col][3] += 20
                            print(app.board[row][col])


def checkCattailAndZombie(app):
    for row in range(len(app.board)):
        for col in range(len(app.board[row])):
            if app.board[row][col][0] == 4:
                x0, y0, x1, y1 = getCellBounds(app, row, col)
                halfX = (x1 - x0) / 2 + 22
                halfY = (y1 - y0) / 2 - 12
                app.x = x0 + halfX
                app.y = y0 + halfY

                bestLine = app.width - app.gap # best template to find the best attack line
                bestRow = 0
                bestCol = 0 
                for zombie in app.zombieList:
                    if zombie[0] < app.width - app.gap:
                        zRow = zombie[0]
                        zCol = zombie[1]
                        r, c = getCells(app, zRow, zCol)

                        if (r == row - 1 or r == row + 1 or r == row) and c >= col: 
                            #find the three points to draw the parabolic graph 
                            zx = zRow - 12
                            zy = zCol 

                            if distance(zx, zy, app.x, app.y) < bestLine:
                                bestLine = distance(zx, zy, app.x, app.y)
                                bestRow = zx
                                bestCol = zy

                mx = app.x + (bestRow - app.x) / 2
                my = app.y - 40

                a, b, c = calcParabolaVertex(app.x, app.y, mx, my, bestRow, bestCol)
                app.board[row][col][5] = a
                app.board[row][col][6] = b
                app.board[row][col][7] = c
   
            if (app.board[row][col][0] == 4 and app.board[row][col][5] != -100 
                and app.board[row][col][6] != -100 and app.board[row][col][7] != -100):
                a = app.board[row][col][5]
                b = app.board[row][col][6]
                c = app.board[row][col][7]
                
                app.board[row][col][3] += 30
                app.board[row][col][4] = a * app.board[row][col][3] ** 2 + b * app.board[row][col][3] + c 


def zombieActionAndState(app):
    for zombie in app.zombieList: 
        if zombie[0] > app.width - app.gap:
            zombie[0] -= 2
        
        #check if there is a plant on the grid 
        if zombie[0] < app.width - app.gap:
            row, col = getCells(app, zombie[0], zombie[1])
            
            #if there is a plant in front, stop and eat the plant
            if app.board[row][col] != [0]:
                zombie[0] -= 0

                if zombie[3] == app.normal2:
                    zombie[3] = app.normalEat2

                elif zombie[3] == app.conehead2:
                    zombie[3] = app.coneEat2

                elif zombie[3] == app.buckethead2:
                    zombie[3] = app.bucketEat2

                app.board[row][col][1] -= 10

                #check if zombie make contact with the bomb  
                if app.board[row][col][0] == 5 and app.board[row][col][3] == True:
                    app.zombieList.remove(zombie)
                    app.killCount += 1
                    app.board[row][col] = [0]
                
                if app.board[row][col] != [0] and app.board[row][col][1] <= 0:
                    app.board[row][col] = [0]

        
            if app.board[row][col] == [0]:
                zombie[0] -= 2
                if zombie[3] == app.normalEat2:
                    zombie[3] = app.normal2

                elif zombie[3] == app.coneEat2:
                    zombie[3] = app.conehead2

                elif zombie[3] == app.bucketEat2:
                    zombie[3] = app.buckethead2

            if zombie[0] < app.marginX:
                app.mode = 'gameOverMode'

def checkForCollsion(app):
    for zombie in app.zombieList:
        x = zombie[0]
        y = zombie[1]

        for row in range(len(app.board)):
            for col in range(len(app.board[0])):
                if app.board[row][col][0] == 2:
                    x1 = app.board[row][col][3]
                    y1 = app.board[row][col][4]

                    if distance(x, y, x1, y1) <= app.bR + 20:
                        x0, y0, x1, y1 = getCellBounds(app, row, col)
                        halfX = (x1 - x0) / 2 + 22
                        halfY = (y1 - y0) / 2 - 12
                        app.board[row][col][3] = x0 + halfX
                        app.board[row][col][4] = y0 + halfY
                        zombie[2] -= 20

                        if zombie[2] <= 0:
                            app.zombieList.remove(zombie)
                            app.killCount += 1
                            app.board[row][col][3] = x0 + halfX
                            app.board[row][col][4] = y0 + halfY
                            break

                    elif x1 > app.width:
                        x0, y0, x1, y1 = getCellBounds(app, row, col)
                        halfX = (x1 - x0) / 2 + 22
                        halfY = (y1 - y0) / 2 - 12
                        app.board[row][col][3] = x0 + halfX
                        app.board[row][col][4] = y0 + halfY

                elif app.board[row][col][0] == 4:
                    x1 = app.board[row][col][3]
                    y1 = app.board[row][col][4]

                    if distance(x, y, x1, y1) <= app.bR + 20:
                        x0, y0, x1, y1 = getCellBounds(app, row, col)
                        halfX = (x1 - x0) / 2 + 22
                        halfY = (y1 - y0) / 2 - 12
                        app.board[row][col][3] = x0 + halfX
                        app.board[row][col][4] = y0 + halfY
                        zombie[2] -= 30

                        if zombie[2] <= 0:
                            app.zombieList.remove(zombie)
                            app.killCount += 1
                            app.board[row][col][3] = x0 + halfX
                            app.board[row][col][4] = y0 + halfY
                            app.board[row][col][5] = -100
                            app.board[row][col][6] = -100
                            app.board[row][col][7] = -100
                            break
                            
                    elif x1 > app.width or y1 > app.height:
                        x0, y0, x1, y1 = getCellBounds(app, row, col)
                        halfX = (x1 - x0) / 2 + 22
                        halfY = (y1 - y0) / 2 - 12
                        app.board[row][col][3] = x0 + halfX
                        app.board[row][col][4] = y0 + halfY


def nightLevelMode_mousePressed(app, event):
    if app.paused == True:
        return 

    else:
        x, y = event.x, event.y  
        
        #collect the suns
        for i in range(len(app.sunStore)):
            x1, y1 = app.sunStore[i]
            if distance(x, y, x1, y1) < app.r:
                app.sun += 25
                app.sunStore.pop(i)
                app.plantCard = 0 
                app.cardSelected = False 
                break 
        
        #select the shovel
        if 340 < x < 415 and 5 < y < 30:
            app.cardSelected = False
            app.shovelSelected = not app.shovelSelected

        #select the card 
        #sunflower = 1; peashooter = 2; wallnut = 3; cattail = 4; potatomine = 5
        if 9 < x < 110 and 20 < y < 85:
            app.cardSelected = True
            app.shovelSelected = False
            app.plantCard = 1

        elif 9 < x < 110 and 100 < y < 165:
            app.cardSelected = True
            app.shovelSelected = False
            app.plantCard = 2

        elif 9 < x < 110 and 180 < y < 245:
            app.cardSelected = True
            app.shovelSelected = False
            app.plantCard = 3

        elif 9 < x < 110 and 260 < y < 325:
            app.cardSelected = True
            app.shovelSelected = False
            app.plantCard = 4

        elif 9 < x < 110 and 340 < y < 405:
            app.cardSelected = True
            app.shovelSelected = False
            app.plantCard = 5

        #select the grid to plant 
        #the board will store [plant, health, state, attack, time]
        if app.cardSelected == True: 
            if app.marginX <= x <= app.width - app.gap and app.marginY <= y <= app.height - 10:
                row, col = getCells(app, x, y)
                x0, y0, x1, y1 = getCellBounds(app, row, col)
                halfX = (x1 - x0) / 2 + 22
                halfY = (y1 - y0) / 2 - 12
            
                if app.board[row][col] == [0] and app.sun >= 50:
                    if app.plantCard == 1:
                        app.board[row][col] = [1, 40, app.p1, False, 1]
                        app.sun -= 50
                        app.scoreBoard[row][col] = 1

                    elif app.plantCard == 3:
                        app.board[row][col] = [3, 200, app.p3, False, 1]
                        app.sun -= 50
                        app.scoreBoard[row][col] = 15

                if app.board[row][col] == [0] and app.sun >= 100:
                    if app.plantCard == 2:
                        app.board[row][col] = [2, 60, app.p2, x0 + halfX, y0 + halfY]
                        app.sun -= 100
                        app.scoreBoard[row][col] = 5
                    
                    elif app.plantCard == 4:
                        app.board[row][col] = [4, 60, app.cat2, x0 + halfX, y0 + halfY, -100, -100, -100]
                        app.sun -= 150              
                        app.scoreBoard[row][col] = 10 

                if app.plantCard == 5 and app.board[row][col] == [0] and app.sun >= 25:
                    app.board[row][col] = [5, 20, app.p51, False, 1]
                    app.sun -= 25
                    app.scoreBoard[row][col] = 20

                else:
                    app.plantCard = 0 
                    app.cardSelected = False 

                app.plantCard = 0 
                app.cardSelected = False   
        
        #remove the plant 
        if app.marginX <= x <= app.width - app.gap and app.marginY <= y <= app.height - 10:
            row, col = getCells(app, x, y)
            if app.shovelSelected == True and app.cardSelected == False:
                if app.board[row][col][0] != [0]:
                    app.shovelMoved == True
                    app.board[row][col] = [0]
                    app.scoreBoard[row][col] = 0
                    app.shovelSelected = False

    
def nightLevelMode_keyPressed(app, event):
    if event.key == 'Q' or event.key == 'q':
        restart(app)
        app.mode = 'startingMode' 

    elif event.key == 'W' or event.key == 'w':
        app.mode = 'winMode' 

    elif event.key == 'L' or event.key == 'l':
        app.mode = 'gameOverMode'

    elif event.key == 'P' or event.key == 'p':
        app.paused = not app.paused

def gameOverMode_keyPressed(app, event):
    if event.key == 'R' or event.key == 'r':
        restart(app)


# formula for finding the a, b, c values of a parabolic function 
#source: http://chris35wills.github.io/parabola_python/
def calcParabolaVertex(x1, y1, x2, y2, x3, y3):
    denom = (x1-x2) * (x1-x3) * (x2-x3)
    a = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / denom
    b = (x3 ** 2 * (y1-y2) + x2 ** 2 * (y3 - y1) + x1 * x1 * (y2 - y3)) / denom
    c = (x2 * x3 * (x2-x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3) / denom

    return a, b, c

def checkForReadyToExplosion(app):
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            if app.board[row][col][0] == 5 and app.board[row][col][1] > 0:
                app.board[row][col][4] += 1

                if app.board[row][col][4] == 12:
                    app.board[row][col][3] = True 
                    app.board[row][col][2] = app.p5
