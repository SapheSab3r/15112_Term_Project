from cmu_112_graphics import *
from tkinter import * 
from zombies import * 
from images import * 
from night_level import *
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

def startingMode_timerFired(app):
    app.timerDelay = 500

def dayLevelMode_timerFired(app):
    if app.paused == True:
        return 

    elif app.killCount == 20:
        app.mode = 'winMode'  

    app.timer0 += app.timer

    if app.timer0 % 200 == 0:
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
                    
    #increase the x coordinate of bullet each time
    moveBullet(app)
    #check if zombie collide with a bullet 
    checkForCollsion(app)
   
    #zombies move
    if app.timer0 >= 500:
        app.releaseZombie = True
        
    if app.releaseZombie == True and app.zombieCount > 0:
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

    else: #the way to find the min value in: https://www.codegrepper.com/code-examples/python/how+to+find+the+minimum+value+in+a+dictionary+python
        bestRow = min(app.result, key = app.result.get)
        app.zombieType = random.randint(1, 3)
        app.zombieY = yposition[bestRow] - 20
        health, zType = addZombies(app)
    
    if len(app.zombieList) <= 10:
        app.zombieList.append([app.zombieX, app.zombieY, health, zType])
        app.zombieCount -= 1

#function for producing sunlight on the board
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

#check if a zombie is on a row where contains plant
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

                        elif app.board[row][col][0] == 4:
                            x0, y0, x1, y1 = getCellBounds(app, row, col)
                            halfX = (x1 - x0) / 2 + 22
                            halfY = (y1 - y0) / 2 - 12

                            #find the three points to draw the parabolic graph 
                            zx = zRow - 12
                            zy = zCol
                            app.x = x0 + halfX
                            app.y = y0 + halfY 
                            mx = app.x + (zx - app.x) / 2
                            my = app.y - 40
                            a, b, c = calcParabolaVertex(app.x, app.y, mx, my, zx, zy)
                            app.board[row][col][5] = a
                            app.board[row][col][6] = b
                            app.board[row][col][7] = c

#draw the projectile path of the corn bullet          
def moveBullet(app):
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
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



def startingMode_timerFired(app):
    #the text at the starting page
    app.textAppear = not app.textAppear

def startingMode_mousePressed(app, event):
    x, y = event.x, event.y

    if 270 < x < 480 and 320 < y < 380:
        app.mode = 'menuMode'

def menuMode_mousePressed(app, event):
    x, y = event.x, event.y
    if ((app.width / 2) - 80 < x < (app.width / 2) + 80 
            and (app.height / 2) / 2 - 40 < y < (app.height / 2) / 2 + 40):
            app.mode = 'dayLevelMode'
    elif (app.width / 2 - 80 < x < app.width / 2 + 80 
            and (app.height / 2 + 80) - 40 < y < (app.height / 2 + 80) + 40):
            app.mode = 'nightLevelMode'

    elif (app.width - 40 - 50 < x < app.width - 40 + 50 
            and app.height - 40 - 50 < y < app.height - 40 + 50):
            app.mode = 'textMode'

def textMode_mousePressed(app, event):
    if event.x and event.y:
        app.mode = 'menuMode'


def dayLevelMode_mousePressed(app, event):
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
        #sunflower = 1; peashooter = 2; wallnut = 3; kernalpult = 4; potatomine = 5
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
                        app.board[row][col] = [4, 60, app.p4, x0 + halfX, y0 + halfY, -100, -100, -100]
                        app.sun -= 100              
                        app.scoreBoard[row][col] = 6  

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

def winMode_mousePressed(app, event):
    if event.x and event.y:
        appStarted(app) 
        
def winMode_keyPressed(app, event):
    if event.key == 'Enter':
        app.mode = 'scoreBoardMode'
    
def dayLevelMode_keyPressed(app, event):
    if event.key == 'Q' or event.key == 'q':
        appStarted(app)

    elif event.key == 'W' or event.key == 'w':
        app.mode = 'winMode' 

    elif event.key == 'L' or event.key == 'l':
        app.mode = 'gameOverMode'

    if event.key == 'P' or event.key == 'p':
        app.paused = not app.paused

def gameOverMode_keyPressed(app, event):
    if event.key == 'R' or event.key == 'r':
        restart(app)
        app.mode = 'menuMode'


# formula for finding the a, b, c values of a parabolic function 
#source: http://chris35wills.github.io/parabola_python/
def calcParabolaVertex(x1, y1, x2, y2, x3, y3):
    denom = (x1-x2) * (x1-x3) * (x2-x3)
    a = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / denom
    b = (x3 ** 2 * (y1-y2) + x2 ** 2 * (y3 - y1) + x1 * x1 * (y2 - y3)) / denom
    c = (x2 * x3 * (x2-x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3) / denom

    return a, b, c

#check on each row and col to see if the potatobomb is ready to explode 
def checkForReadyToExplosion(app):
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            if app.board[row][col][0] == 5 and app.board[row][col][1] > 0:
                app.board[row][col][4] += 1

                if app.board[row][col][4] == 12:
                    app.board[row][col][3] = True 
                    app.board[row][col][2] = app.p5


#********************#
#Draw Functions# 
#********************#

#draw the lawn in the game 
def drawDayGrid(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            color = 'forest green' 
            x0, y0, x1, y1 = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill = color, width = 2, 
                                    outline = 'dark green')

def drawNightGrid(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            color = 'SteelBlue4' 
            x0, y0, x1, y1 = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, fill = color, width = 2, 
                                    outline = 'black')

#draw board for placing plants
def drawBoard(app, canvas):
    rows, cols = len(app.board), len(app.board[0])
    for row in range(rows):
        for col in range(cols):
            x0, y0, x1, y1 = getCellBounds(app, row, col)
            canvas.create_rectangle(x0, y0, x1, y1, width = 3)

def drawGameStartedPage(app, canvas):
    canvas.create_image(350, 210, image=ImageTk.PhotoImage(app.StartPage2))
    canvas.create_rectangle(270, 320, 480, 380, fill = 'grey15', 
                                width = 4, outline = 'black')
    if app.textAppear:
        canvas.create_text(375, 350, font = 'arial 30 bold', fill = 'white', 
                                text = 'Click to Start')

def drawNight(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image=ImageTk.PhotoImage(app.night2))
    
def drawDay(app, canvas):
    canvas.create_image(500, 210, image=ImageTk.PhotoImage(app.image2))

def drawBackground(app, canvas):
    canvas.create_image(200, 20, image=ImageTk.PhotoImage(app.image4))
    canvas.create_image(380, 20, image=ImageTk.PhotoImage(app.shovel2))

    #draw box when shovel is selected
    if app.shovelSelected == True:
        canvas.create_rectangle(345, 5, 415, 35, width = 5, outline = 'yellow')

def drawCornBullet(app, canvas):
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            if app.board[row][col][0] == 4:
                canvas.create_oval(app.board[row][col][3] - 10, app.board[row][col][4] - 10, app.board[row][col][3] + 10, app.board[row][col][4] + 10, fill = 'orange')

def drawNightCardHolder(app, canvas):
    canvas.create_rectangle(9, 260, 110, 325, fill = 'coral4', 
                                width = 4, outline = 'grey10')
    canvas.create_image(60, 292, image=ImageTk.PhotoImage(app.cattail2))


def drawDayCardHolder(app, canvas):
    #kernalPult 
    canvas.create_rectangle(9, 260, 110, 325, fill = 'coral4', 
                                width = 4, outline = 'grey10')
    canvas.create_image(60, 292, image=ImageTk.PhotoImage(app.kernelpult2))

def drawCardHolder(app, canvas):
    #sunFlower 
    canvas.create_rectangle(9, 20, 110, 85, fill = 'coral4', 
                                width = 4, outline = 'grey10')
    canvas.create_image(60, 52, image=ImageTk.PhotoImage(app.sunflower2))

    #peaShooter 
    canvas.create_rectangle(9, 100, 110, 165, fill = 'coral4', 
                                width = 4, outline = 'grey10')
    canvas.create_image(60, 132, image=ImageTk.PhotoImage(app.peashooter2))

    #wallNut 
    canvas.create_rectangle(9, 180, 110, 245, fill = 'coral4', 
                                width = 4, outline = 'grey10')
    canvas.create_image(60, 212, image=ImageTk.PhotoImage(app.wallnut2))

    #potatoMine
    canvas.create_rectangle(9, 340, 110, 405, fill = 'coral4', 
                                width = 4, outline = 'grey10')
    canvas.create_image(60, 372, image=ImageTk.PhotoImage(app.potatomine2))

def drawSelectCard(app, canvas):
    #if being selected 
    if app.cardSelected == True and app.plantCard == 1:
        canvas.create_rectangle(9, 20, 110, 85, width = 4, outline = 'yellow')

    elif app.cardSelected == True and app.plantCard == 2:
        canvas.create_rectangle(9, 100, 110, 165, width = 4, outline = 'yellow')

    elif app.cardSelected == True and app.plantCard == 3:
        canvas.create_rectangle(9, 180, 110, 245, width = 4, outline = 'yellow')

    elif app.cardSelected == True and app.plantCard == 4:
        canvas.create_rectangle(9, 260, 110, 325, width = 4, outline = 'yellow')

    elif app.cardSelected == True and app.plantCard == 5:
        canvas.create_rectangle(9, 340, 110, 405, width = 4, outline = 'yellow')
           
#draw the bullet for the cattail 
def drawCatBullet(app, canvas):
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            if app.board[row][col][0] == 4:

                canvas.create_oval(app.board[row][col][3] - app.bR, app.board[row][col][4] - app.bR, 
                                    app.board[row][col][3] + app.bR, app.board[row][col][4] + app.bR, 
                                    width = 3, fill = 'red3',
                                    outline = 'red4')

def drawBullet(app, canvas):
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            if app.board[row][col][0] == 2:
                 
                canvas.create_oval(app.board[row][col][3] - app.bR, app.board[row][col][4] - app.bR, 
                                    app.board[row][col][3] + app.bR, app.board[row][col][4] + app.bR, 
                                    width = 3, fill = 'light green',
                                    outline = 'dark green')

def drawDayPlant(app, canvas):
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):   
            if app.shovelMoved == False:
                if app.board[row][col][0] == 4:
                    x0, y0, x1, y1 = getCellBounds(app, row, col)
                    cellWidthHalf = (x1 - x0) / 2
                    cellHeightHalf = (y1 - y0) / 2
                    state = app.board[row][col][2]
                    canvas.create_image(x0 + cellWidthHalf, y0 + cellHeightHalf, image=ImageTk.PhotoImage(state))

def drawNightPlant(app, canvas):
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):   
            if app.shovelMoved == False:
                if app.board[row][col][0] == 4:
                    x0, y0, x1, y1 = getCellBounds(app, row, col)
                    cellWidthHalf = (x1 - x0) / 2
                    cellHeightHalf = (y1 - y0) / 2
                    state = app.board[row][col][2]
                    canvas.create_image(x0 + cellWidthHalf, y0 + cellHeightHalf, image=ImageTk.PhotoImage(state))


def drawPlant(app, canvas):
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):   
                 
            if app.shovelMoved == False:
                if app.board[row][col][0] == 1: 
                    x0, y0, x1, y1 = getCellBounds(app, row, col)
                    cellWidthHalf = (x1 - x0) / 2
                    cellHeightHalf = (y1 - y0) / 2 
                    state = app.board[row][col][2]
                    canvas.create_image(x0 + cellWidthHalf, y0 + cellHeightHalf, image=ImageTk.PhotoImage(state))

                elif app.board[row][col][0] == 2: 
                    x0, y0, x1, y1 = getCellBounds(app, row, col)
                    cellWidthHalf = (x1 - x0) / 2
                    cellHeightHalf = (y1 - y0) / 2
                    state = app.board[row][col][2]
                    canvas.create_image(x0 + cellWidthHalf, y0 + cellHeightHalf, image=ImageTk.PhotoImage(state))
                    
                elif app.board[row][col][0] == 3:
                    x0, y0, x1, y1 = getCellBounds(app, row, col)
                    cellWidthHalf = (x1 - x0) / 2
                    cellHeightHalf = (y1 - y0) / 2
                    state = app.board[row][col][2]
                    canvas.create_image(x0 + cellWidthHalf, y0 + cellHeightHalf, image=ImageTk.PhotoImage(state))

                elif app.board[row][col][0] == 5:
                    x0, y0, x1, y1 = getCellBounds(app, row, col)
                    cellWidthHalf = (x1 - x0) / 2
                    cellHeightHalf = (y1 - y0) / 2
                    state = app.board[row][col][2]
                    canvas.create_image(x0 + cellWidthHalf, y0 + cellHeightHalf, image=ImageTk.PhotoImage(state))
                

def drawText(app, canvas):
    canvas.create_text(210, 18, text = app.sun, font = 'arial 20', 
                        fill = 'black', anchor = 'center')

#draw sun randomly appear on the screen
def drawSun(app, canvas): 
    for sun in app.sunStore:
        row, col = sun
        canvas.create_image(row, col, image=ImageTk.PhotoImage(app.sun2))

#draw the zombie in the list
def drawZombie(app, canvas):
    for zombie in app.zombieList:
        zombieX, zombieY, health, zType = zombie
        canvas.create_image(zombieX, zombieY, image=ImageTk.PhotoImage(zType))

def gameOverMode_redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = 'red4')
    canvas.create_image(app.width / 2, app.height / 2, image=ImageTk.PhotoImage(app.lose2))

    canvas.create_text(app.width / 2, app.height - 50, text = f'Total Kill: {app.killCount}',
                            font = 'arial 24 bold', fill = 'white', anchor = 'center')
 
def menuMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'gray25')

    canvas.create_rectangle((app.width / 2) - 80, (app.height / 2) / 2 - 40, 
                                (app.width / 2) + 80, (app.height / 2) / 2 + 40,
                                fill = 'gray17', width = 4)

    canvas.create_text(app.width / 2, (app.height / 2) / 2, text = 'Day Level', 
                                    fill = 'white', font = 'arial 25 bold')

    canvas.create_rectangle(app.width / 2 - 80, (app.height / 2 + 80) - 40, 
                                app.width / 2 + 80, (app.height / 2 + 80)  + 40,
                                fill = 'gray17', width = 4)

    canvas.create_text(app.width / 2, (app.height / 2 + 80), text = 'Night Level', 
                                    fill = 'white', font = 'arial 25 bold')
    canvas.create_oval(app.width - 40 - 30, app.height - 40 - 30, app.width - 40 + 30, app.height - 40 + 30,
                            fill = 'gray17', width = 4)

    canvas.create_text(app.width - 40, app.height - 40,
                            fill = 'white', font = 'arial 40 bold', text = '?')

def textMode_redrawAll(app, canvas):
    messages = ['Plants vs Zombies is a tower-defend game',
                'Player need to defend zombies using the given plants',
                'Each plant costs different amount of sunlight',
                'And each plant has its own unique feature:',
                'Peashooter: attack the zombie in the row',
                'Kernel Pult: attack the zombie in teh row in a projectile path',
                'Cattail: large attack range (one row above it and one row below it)',
                'Walnut: defend system but cannot attack',
                'Sunflower: generate sunlight to plant each plant',
                '                                            ',
                'Day Level: defeat total 20 zombies',
                'Night Level: defeat total 30 zombies and the time spent to produce sunlight increases',
                ]

    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'gray')
    gap = 20
    for line in messages: 
        canvas.create_text(app.width / 4 + 200, 30 + gap, text = line,
                            font = 'Arial 15 bold', fill = 'white', anchor = 'center')
        gap += 30


def winMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'gold')
    canvas.create_text(app.width / 2, app.height / 2, text = 'You Win!',
                        font = 'arial 50 bold', anchor = 'center')


def dayLevelMode_redrawAll(app, canvas):
    drawDay(app, canvas)
    drawBackground(app, canvas)
    drawDayGrid(app, canvas)
    drawBoard(app, canvas)
    drawCardHolder(app, canvas)
    drawDayCardHolder(app, canvas)
    drawSelectCard(app, canvas)
    drawBullet(app, canvas)
    drawCornBullet(app, canvas)
    drawPlant(app, canvas)
    drawDayPlant(app, canvas)
    drawText(app, canvas)
    drawSun(app, canvas)
    drawZombie(app, canvas)

def nightLevelMode_redrawAll(app, canvas):
    drawNight(app, canvas)
    drawBackground(app, canvas)
    drawNightGrid(app, canvas)
    drawBoard(app, canvas)
    drawCardHolder(app, canvas)
    drawNightCardHolder(app, canvas)
    drawSelectCard(app, canvas)
    drawBullet(app, canvas)
    drawCatBullet(app, canvas)
    drawPlant(app, canvas)
    drawNightPlant(app, canvas)
    drawText(app, canvas)
    drawSun(app, canvas)
    drawZombie(app, canvas)

def startingMode_redrawAll(app, canvas):
    drawGameStartedPage(app, canvas)

runApp(width = 750, height= 420)