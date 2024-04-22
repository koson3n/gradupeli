import pygame
import graphics as gp
import sounds as snd

pygame.init()

#Hardcoded screensize, to keep it relatively simple
SCREENWIDTH = 800
SCREENHEIGHT = 600

#Action variables
moveRight = False
moveLeft = False
jumping = False

gamewon = False

#Gameplay variables
currentBg = 0
lastBg = 0
startIcon = 50

time = 0
points = 100000

#List of backgrounds that have puzzles (nums)
#params: [background number, puzzle type, combination]
puzzleList = [[1, 'lockpuzzle', [1, 4, 4]]]

#List of lock combos
lockCombinations = [[1, 4, 4]]

#Gamesettings (60 normal, higher for testing purposes, cos the dude moves quicker)
clock = pygame.time.Clock()
fps = 60

#Hanoi puzzle global variables
somethingSelected = False

class Game:
    def __init__(self):
        self.gameRun = True

#Character that is controlled by the player
class Player:
    def __init__(self, health, stamina, level):
        self.health = health
        self.stamina = stamina
        self.level = level
        self.colWithGameobject = False
        self.inventory = []
        self.points = 0
        self.deaths = 0
        self.sprite = gp.MovableSprite()
        self.speed = 5
        self.sprite.rect.y = 505

    def __repr__(self):
        return f"Health: {self.health}, Stam: {self.stamina}, Level: {self.level}"
    
    #Player movement
    def move (self):
        #delta x and y. the proposed difference in position
        dx = 0
        dy = 0

        if moveLeft:
            dx = -self.speed
        if moveRight:
            dx = self.speed

        self.sprite.rect.x += dx
        self.sprite.rect.y += dy

    def setColWithObj (self, bol):
        self.colWithGameobject = bol

    def getColWithObj(self):
        return self.colWithGameobject
    
    def collidingWithPlatform(self):
        self.sprite.rect.y = 410

    def notCollidingWithPlatform(self):
        self.sprite.rect.y = 505

    def fallDown(self):
        if self.sprite.rect.y < 505:
            self.sprite.rect.y = self.sprite.rect.y + 5

#Item within the game, that is not part of the background (sprite)
class GameItem:
    def __init__(self,name,scale):
        self.sprite = gp.ObjectSprite(scale,name)
        self.sprite.rect.x = 0
        self.sprite.rect.y = 0
        self.drawn = False

    def getDrawn(self):
        return self.drawn
    
    def setDrawn (self,bol):
        self.drawn = bol

class PuzzleIcon:
    def __init__(self,name):
        self.sprite = gp.ObjectSprite(0.6,name)
        self.sprite.rect.x = 0
        self.sprite.rect.y = 250
        self.drawn = False
        self.id = self.getId(name)

    def getDrawn(self):
        return self.drawn
    
    def setDrawn (self,bol):
        self.drawn = bol

    def getId(self,name):
        if name == 'left_arrow':
            return 'l'
        elif name == 'right_arrow':
            return 'r'
        elif name == '5sek':
            return '5'
        else:
            return 'loop'

class PlatformItem:
    def __init__(self,name,scale):
        self.sprite = gp.ObjectSprite(scale, name)
        self.sprite.rect.x
        self.sprite.rect.y
        self.drawn = False
        self.movingL = False
        self.movingR = False
        self.waiting = False
        self.looping = False
        self.tickStop = 200
    
    def move(self, direction):
        if direction == 'left':
            self.sprite.rect.x = self.sprite.rect.x - 4
        elif direction == 'right':
            self.sprite.rect.x = self.sprite.rect.x + 4

    def toggleLooping(self):
        if self.looping:
            self.looping = False
        else:
            self.looping = True

    def reset(self):
        self.movingL = False
        self.movingR = False
        self.looping = False
        self.waiting = False
        self.tickStop = 200
        self.sprite.rect.x = 300


class LockPuzzle3:   
    def __init__(self, comb, crrbg):   
        self.sprite = gp.ObjectSprite(1, 'taskbase')
        self.lockwheel1 = Button(1, 'wheel', 100, 70)
        self.lockwheel2 = Button(1, 'wheel', 200, 70)
        self.lockwheel3 = Button(1, 'wheel', 300, 70)
        self.openChest = gp.ObjectSprite(1, 'chest_open')
        self.hint = GameItem('hint', 1)
        self.done = False
        self.notifShown = False
        self.soundPlayed = False
        self.bgNumber = crrbg
        self.puzzleActive = False
        self.text = 'Chest has a combination lock'
        self.textSurf = getTextSurface(self.text)
        self.backbutton = Button(1, 'back_btn', 230, 330)
        self.hintBackButton = Button(1, 'back_btn', 550, 450) 
        self.hints = 0
        self.comb1 = comb[0]
        self.comb2 = comb[1]
        self.comb3 = comb[2]
        self.notif = Notification("The chest opens! You found a key from the chest!", 'notification_lockpuzzle3')

    def checkIfDone (self):
        if self.lockwheel1.currNum == self.comb1 and self.lockwheel2.currNum == self.comb2 and self.lockwheel3.currNum == self.comb3:
            if self.soundPlayed == False:
                chestSnd.play()
                self.soundPlayed = True
            self.closeLockPuzzle()
            self.done = True
            self.notif.openNotification()
            

    def openLockPuzzle(self):
        self.setPuzzleState(True)
        spritegroup3.add(self.sprite)      
        spritegroup3.add(self.backbutton.sprite)
        spritegroup3.add(self.lockwheel1.sprite)
        spritegroup3.add(self.lockwheel2.sprite)
        spritegroup3.add(self.lockwheel3.sprite)

    def closeLockPuzzle(self):
        self.setPuzzleState(False)
        spritegroup3.empty()

    def openHint(self):
        self.hint.sprite.rect.x = 200
        self.hint.sprite.rect.y = 100
        spritegroup2.add(self.hint.sprite)
        spritegroup2.add(self.hintBackButton.sprite)

    def closeHint(self):
        spritegroup2.remove(self.hint.sprite)
        spritegroup2.remove(self.hintBackButton.sprite)

    def setPuzzleState (self, active):
        self.puzzleActive = active

    def getPuzzleState (self):
        return self.puzzleActive
    
class BridgePuzzle:
    def __init__(self):
        self.sprite = gp.ObjectSprite(1, 'taskbase')
        self.puzzleActive = False
        self.backbutton = Button(1, 'back_btn', 230, 330)
        self.rightArr = Button(1, 'right_arrow', 50, 100)
        self.leftArr = Button(1, 'left_arrow', 150, 100)
        self.loopArr = Button(1, 'loop_arrow', 250, 100)
        self.loopArrAct = Button(1, 'loop_arrow_active', 250, 100)
        self.fivesecArr = Button(1, '5sek', 350, 100)
        self.ansBox = GameItem('ans_box', 1)
        self.execBtn = Button(0.8, 'exec_btn', 425, 220)
        self.resetBtn = Button(0.7, 'reset_btn', 440, 30)
        self.slots = []
        self.slotsph = []
        self.currSlot = 0
        self.comExecuting = False
        self.iconSpacing = 50
        self.iconSlots = [50,120,190,260,330]
        self.executing = False

        self.ansBox.sprite.rect.x = 30
        self.ansBox.sprite.rect.y = 200

    def openPuzzle(self):
        spritegroup3.add(self.sprite)
        spritegroup3.add(self.backbutton.sprite)
        spritegroup3.add(self.rightArr.sprite)
        spritegroup3.add(self.leftArr.sprite)
        spritegroup3.add(self.ansBox.sprite)
        spritegroup3.add(self.execBtn.sprite)
        spritegroup3.add(self.loopArr.sprite)
        spritegroup3.add(self.fivesecArr.sprite)
        spritegroup3.add(self.resetBtn.sprite)
        self.puzzleActive = True

        if len(self.slotsph) > 0:
            for i in range(len(self.slotsph)):
                self.addIconToAnsbar(self.slotsph[i])
            self.slotsph = []

    def closePuzzle(self):
        spritegroup3.empty()
        self.slotsph = self.slots
        self.puzzleActive = False

    def addIconToAnsbar(self, icon):
        iconLeftArrow = PuzzleIcon('left_arrow')
        iconRightArrow = PuzzleIcon('right_arrow')
        iconLoopArrow = PuzzleIcon('loop_arrow')
        iconFivesecArrow = PuzzleIcon('5sek')

        if len(self.slots) >= 5:
            return

        if icon == '5s':
            self.slots.append(iconFivesecArrow)
        elif icon == 'left':
            self.slots.append(iconLeftArrow)
        elif icon == 'right':
            self.slots.append(iconRightArrow)

        for i in range(len(self.slots)):
            self.slots[i].sprite.rect.x = self.iconSlots[i]
            spritegroup3.add(self.slots[i].sprite)

    def emptyAnsBar(self):
        self.slots.clear()

    def reset(self):
        self.currSlot = 0
        for i in range(len(self.slots)):
            spritegroup3.remove(self.slots[i].sprite)
        self.emptyAnsBar()
        

class Hanoi:
    def __init__(self):
        self.leftPillar = [5,4,3,2,1]
        self.midPillar = []
        self.rightPillar = [] 
        self.winCon = [5,4,3,2,1]
        self.done = False
        self.selectedDisk = 0
        self.talkedToTheFactoryMan = False
        self.pillarSt = 0
        self.pillarDs = 0
        self.pillarsSelected = 0
        self.moves = 0
        self.dial1 = GameItem('factorydialog1', 1)
        self.dial2 = GameItem('factorydialog2', 1)   
        self.dial1done = False
        self.dial2done = False
        self.dial1back = Button(1, 'back_btn', 550, 450)
        self.dial2back =  Button(1, 'back_btn', 550, 450)
        self.remote = GameItem('remote', 1)
        self.remoteDrawn = False

    def checkIfWon(self):
        return self.rightPillar == self.winCon
    
    def move(self):
        if self.validMove():
            d = self.getPillar(self.pillarSt).pop()
            self.getPillar(self.pillarDs).append(d)
            self.unselect()
            self.moves += 1
        else:
            self.unselect()
        if self.checkIfWon():
            self.done = True
    
    
    def movePossible(self, startPillar, destPillar):
        if startPillar[0] < destPillar[0] or len(destPillar) == 0:
            return True
        else:
            return False

    def getPillar(self, p):
        if p == 1:
            return self.leftPillar
        if p == 2:
            return self.midPillar
        if p == 3:
            return self.rightPillar
        

    def moveDisk(self, startPillar, destPillar):
        destPillar.append(startPillar[-1])
        startPillar.pop()

    def validMove(self):
        st = self.getPillar(self.pillarSt)
        dt = self.getPillar(self.pillarDs)

        if len(dt) > 0:
            if dt[-1] < st[-1]:
                return False
            else:
                return True
        else:
            return True

    def unselect(self):
        self.pillarSt = 0
        self.pillarDs = 0
        self.pillarsSelected = 0    

    def openDial1(self):
        self.dial1.sprite.rect.x = 200
        self.dial1.sprite.rect.y = 100
        spritegroup2.add(self.dial1.sprite)
        spritegroup2.add(self.dial1back.sprite)
        self.talkedToTheFactoryMan = True

    def closeDial1(self):
        spritegroup2.remove(self.dial1.sprite)
        spritegroup2.remove(self.dial1back.sprite) 

    def openDial2(self):
        self.dial2.sprite.rect.x = 200
        self.dial2.sprite.rect.y = 100
        spritegroup2.add(self.dial2.sprite)
        spritegroup2.add(self.dial2back.sprite)

    def closeDial2(self):
        spritegroup2.remove(self.dial2.sprite)
        spritegroup2.remove(self.dial2back.sprite)   

    def drawRemote(self):
        self.remote.sprite.rect.x = 500
        self.remote.sprite.rect.y = 550
        spritegroup2.add(self.remote.sprite)
        self.remoteDrawn = True

    def undrawRemote(self):
        spritegroup2.remove(self.remote.sprite)

class Notification:
    def __init__(self, txt, name):
        self.text = txt
        self.sprite = gp.ObjectSprite(1, name)
        self.active = False
        self.textSurf = getTextSurface(self.text)
        self.backbutton = Button(1, 'back_btn', 230, 330)

    def openNotification(self):
        self.active = True
        spritegroup3.add(self.sprite)
        spritegroup3.add(self.backbutton.sprite)

    def closeNotification(self):
        self.active = False
        lockPuzzle3.notifShown = True
        spritegroup3.empty()
        

#Placeholder class for possible settings
class Game: 
    #For future pre-launch settings
    def __init__(self, x):
        self.x = x        
    def __repr__(self):
       return f"x = {self.x}"  

#UI elements    
class Button:
    def __init__(self,scale=1,name='',x=0,y=0):
        self.name = name
        self.scale = scale
        self.sprite = gp.ObjectSprite(scale, name,x,y)
        self.currNum = 0
        self.text = str(self.currNum)
        self.textSurf = getTextSurface(self.text)

    def isClicked(self):
        mousePos = pygame.mouse.get_pos()
        return self.sprite.rect.collidepoint(mousePos)
    
    def getCurrentNumberAsSurface (self):
        return getTextSurface(str(self.currNum))
    
    def update(self):
        self.currNum = lockPuzzleCalc(self.currNum)
        self.textSurf = self.getCurrentNumberAsSurface()

class ButtonHanoiDisk:
    def __init__(self,scale=1,name='',x=0,y=0):
        self.name = name
        self.scale = scale
        self.sprite = gp.ObjectSprite(scale, name,x,y)
        self.id = 0
        self.selected = False
        self.diskNumber = 0

    def isClicked(self):
        mousePos = pygame.mouse.get_pos()
        return self.sprite.rect.collidepoint(mousePos)
    



class ButtonHanoiPillar:
    def __init__(self,scale=1,name='',x=0,y=0):
        self.name = name
        self.scale = scale
        self.sprite = gp.ObjectSprite(scale, name,x,y)
        self.id = 0
        self.selected = False
        self.disks = []
        self.pillarNumber = 0
        self.selected = False

    def isClicked(self):
        mousePos = pygame.mouse.get_pos()
        return self.sprite.rect.collidepoint(mousePos)
 
def unselectDisk():
    disk1.selected = False
    disk2.selected = False
    disk3.selected = False
    disk4.selected = False
    disk5.selected = False

def unselectPillars():
    pillar1.selected = False

def getTextSurface(text):
    font = pygame.font.SysFont(None, 30)
    return font.render(text, True, (0, 0, 0))

def lockPuzzleCalc (curr):
    if curr < 9:
        curr += 1
    else:
        curr = 0
    return curr

def moveBridge(plat, direction):
    if direction == 'left':
        plat.sprite.rect.x = plat.sprite.rect.x - 1
    elif direction == 'right':
        plat.sprite.rect.x = plat.sprite.rect.x + 1

def execBridge(plat, com):
    if com.id == 'r':
        plat.movingL = False
        plat.waiting = False
        plat.movingR = True
    if com.id == 'l':
        plat.movingR = False
        plat.waiting = False
        plat.movingL = True
    if com.id == '5':
        plat.movingR = False
        plat.movingL = False
        plat.waiting = True
    if com.id == 'loop':
        plat.looping = True

def checkPosition(plat):
    if plat.movingR and plat.sprite.rect.x >= 550:
        plat.movingR = False
        return True
    if plat.movingL and plat.sprite.rect.x <= 300:
        plat.movingL = False
        return True
    
def changeIconToLooping(pzl):
    spritegroup3.remove(pzl.loopArr.sprite)
    spritegroup3.add(pzl.loopArrAct.sprite)

def changeIconToNotLooping(pzl):
    spritegroup3.remove(pzl.loopArrAct.sprite)
    spritegroup3.add(pzl.loopArr.sprite)    

def drawDisks(p1, p2, p3, d1, d2, d3, d4, d5):
    ypos = 520
    xpos = 170

    for i in range(len(p1)):
        if p1[i] == 5:
            d5.sprite.rect.y = ypos
            d5.sprite.rect.x = xpos
            ypos -= 30
        if p1[i] == 4:
            d4.sprite.rect.y = ypos
            d4.sprite.rect.x = xpos
            ypos -= 30
        if p1[i] == 3:
            d3.sprite.rect.y = ypos
            d3.sprite.rect.x = xpos
            ypos -= 30
        if p1[i] == 2:
            d2.sprite.rect.y = ypos
            d2.sprite.rect.x = xpos
            ypos -= 30
        if p1[i] == 1:
            d1.sprite.rect.y = ypos
            d1.sprite.rect.x = xpos
            ypos -= 30

    ypos = 520
    xpos = 320

    for i in range(len(p2)):
        if p2[i] == 5:
            d5.sprite.rect.y = ypos
            d5.sprite.rect.x = xpos
            ypos -= 30
        if p2[i] == 4:
            d4.sprite.rect.y = ypos
            d4.sprite.rect.x = xpos
            ypos -= 30
        if p2[i] == 3:
            d3.sprite.rect.y = ypos
            d3.sprite.rect.x = xpos
            ypos -= 30
        if p2[i] == 2:
            d2.sprite.rect.y = ypos
            d2.sprite.rect.x = xpos
            ypos -= 30
        if p2[i] == 1:
            d1.sprite.rect.y = ypos
            d1.sprite.rect.x = xpos
            ypos -= 30

    ypos = 520
    xpos = 470

    for i in range(len(p3)):
        if p3[i] == 5:
            d5.sprite.rect.y = ypos
            d5.sprite.rect.x = xpos
            ypos -= 30
        if p3[i] == 4:
            d4.sprite.rect.y = ypos
            d4.sprite.rect.x = xpos
            ypos -= 30
        if p3[i] == 3:
            d3.sprite.rect.y = ypos
            d3.sprite.rect.x = xpos
            ypos -= 30
        if p3[i] == 2:
            d2.sprite.rect.y = ypos
            d2.sprite.rect.x = xpos
            ypos -= 30
        if p3[i] == 1:
            d1.sprite.rect.y = ypos
            d1.sprite.rect.x = xpos
            ypos -= 30
        
def allPillarsUnselect(p1, p2, p3):
    p1.sprite.update('pillar')
    p2.sprite.update('pillar')
    p3.sprite.update('pillar')

def gameWin():
    hanoiPuzzle.done = True

def is_value_in_array(array, value):
    return value in array

def displayKeyPromp():
    spritegroup2.add(keyprompt.sprite)

def showHint(i):
    if i == 0:
        spritegroup2.add(hint0.sprite)
        spritegroup2.add(hintback.sprite)
        spritegroup2.add(hintnext.sprite)
    elif i == 1:
        spritegroup2.add(hint1.sprite)
        spritegroup2.add(hintback.sprite)
        spritegroup2.add(hintnext.sprite)
    elif i == 2:
        spritegroup2.add(hint2.sprite)
        spritegroup2.add(hintback.sprite)
        spritegroup2.add(hintnext.sprite)
    else:
        spritegroup2.add(hint3.sprite)
        spritegroup2.add(hintback.sprite)
        spritegroup2.add(hintnext.sprite)

def unshowHint():
    spritegroup2.remove(hint0.sprite)
    spritegroup2.remove(hint1.sprite)
    spritegroup2.remove(hint2.sprite)
    spritegroup2.remove(hint3.sprite)
    spritegroup2.remove(hintnext.sprite)
    spritegroup2.remove(hintback.sprite)

def calculatePoints(p, lp3, hp, t, d):
    return p / ((lp3.hints * 10000) + (hp.moves * 1000) + (d * 20000) + (t / 60))

def statScreen(p, lp3, hp, t, d):
    intro = "You won the game! Here are your stats"
    text1 = "Deaths: " + str(d)
    text2 = "Hints: " + str(lp3.hints)
    text3 = "Disk moves: " + str(hp.moves)
    text4 = "Total points: " + str(p)
    text5 = "Time: " + str(round(t))

    intros = getTextSurface(intro)
    text1s = getTextSurface(text1)
    text2s = getTextSurface(text2)
    text3s = getTextSurface(text3)
    text4s = getTextSurface(text4)
    text5s = getTextSurface(text5)

    screen.blit(intros, (120, 100))
    screen.blit(text1s, (150, 140))
    screen.blit(text2s, (150, 180))
    screen.blit(text3s, (150, 220))
    screen.blit(text5s, (150, 260))
    screen.blit(text4s, (150, 300))

    spritegroup2.add(exit.sprite)
    
#Variables for various purposes in the loop
gameRun = False

#Gamescreen setup
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('SpeedRunning Challenge')
player = Player(100, 100, 1)
bgArray = gp.backgroundArrayLoader('bg')


#Puzzleitems for BACKGR 1
chest = GameItem('env_chest3', 0.5)
chest.sprite.rect.x = 250
chest.sprite.rect.y = 500
open_chest = GameItem('chest_open', 0.3)
open_chest.sprite.rect.x = 250
open_chest.sprite.rect.y = 465
paper = GameItem('paper', 1)
paper.sprite.rect.x = 450
paper.sprite.rect.y = 550
lockPuzzle3 = LockPuzzle3([1,4,4], 1)
keyprompt = GameItem('key_prompt', 1)
keyprompt.sprite.rect.x = 400
keyprompt.sprite.rect.y = 300
hintbutton = Button(1, 'hintbtn', 650, 50)
hint0 = GameItem('lockhint0', 1)
hint0.sprite.rect.x = 500
hint0.sprite.rect.y = 100
hint1 = GameItem('lockhint1', 1)
hint1.sprite.rect.x = 500
hint1.sprite.rect.y = 100
hint2 = GameItem('lockhint2', 1)
hint2.sprite.rect.x = 500
hint2.sprite.rect.y = 100
hint3 = GameItem('lockhint3', 1)
hint3.sprite.rect.x = 500
hint3.sprite.rect.y = 100
hintback = Button(1, 'back_btn', 490, 280)
hintnext = Button(1, 'hint_next_btn', 640, 280)

#Puzzleitems for BACKGR 3
bridge = PlatformItem('bridge', 1)
bridge.sprite.rect.y = 500
bridge.sprite.rect.x = 300
floorLeft = PlatformItem('fac_floor_long', 1)
floorLeft.sprite.rect.y = 500
floorLeft.sprite.rect.x = 0
floorRight = PlatformItem('fac_floor_short', 1)
floorRight.sprite.rect.y = 500
floorRight.sprite.rect.x = 650
terminal = GameItem('terminal', 1)
terminal.sprite.rect.x = 200
terminal.sprite.rect.y = 400
spikes = GameItem('spikes', 1)
spikes.sprite.rect.y = 560
spikes.sprite.rect.x = 330
bridgePuzzle = BridgePuzzle()
cautionSign = GameItem('sign', 1)
cautionSign.sprite.rect.x = 400
cautionSign.sprite.rect.y = 300


#Puzzleitems for BACKGR 4
npc = GameItem('tehdasaia', 1)
npc.sprite.rect.x = 100
npc.sprite.rect.y = 505
pilPlat = GameItem('pillar_platform', 1)
pilPlat.sprite.rect.y = 550
pilPlat.sprite.rect.x = 200
pillar1 = ButtonHanoiPillar(1, 'pillar')
pillar1.sprite.rect.y = 300
pillar1.sprite.rect.x = 225
pillar1.pillarNumber = 1
pillar2 = ButtonHanoiPillar(1, 'pillar')
pillar2.sprite.rect.y = 300
pillar2.sprite.rect.x = 375
pillar2.pillarNumber = 2
pillar3 = ButtonHanoiPillar(1, 'pillar')
pillar3.sprite.rect.y = 300
pillar3.sprite.rect.x = 525
pillar3.pillarNumber = 3
disk1 = ButtonHanoiDisk(1, 'disk1')
disk1.diskNumber = 1
disk1.sprite.rect.y = 400
disk1.sprite.rect.x = 210
disk2 = ButtonHanoiDisk(1, 'disk2')
disk2.diskNumber = 2
disk2.sprite.rect.y = 430
disk2.sprite.rect.x = 200
disk3 = ButtonHanoiDisk(1, 'disk3')
disk3.diskNumber = 3
disk3.sprite.rect.y = 460
disk3.sprite.rect.x = 190
disk4 = ButtonHanoiDisk(1, 'disk4')
disk4.diskNumber = 4
disk4.sprite.rect.y = 490
disk4.sprite.rect.x = 180
disk5 = ButtonHanoiDisk(1, 'disk5')
disk5.diskNumber = 5
disk5.sprite.rect.y = 520
disk5.sprite.rect.x = 170
hanoiPuzzle = Hanoi()



#Spritegrouping
#group 1: player (drawn last = on top)
spritegroup1 = pygame.sprite.Group()
spritegroup1.add(player.sprite)

#group 2: interactive items
spritegroup2 = pygame.sprite.Group()

#group 3: puzzle stuff
spritegroup3 = pygame.sprite.Group()

#Sound effects
chestSnd = snd.loadSound("chest_open_snd")
splatSnd = snd.loadSound("splat")
pick = snd.loadSound("pickup")
splatSnd.set_volume(0.75)

#titlescreen stuff
title = True
start = Button(1, 'startbtn', 600, 400)
exit = Button(1, 'exitbtn', 600, 500)
titleback = gp.ObjectSprite(1, 'titlescreen', 0, 0)
titlegroup = pygame.sprite.Group()
titlegroup.add(start.sprite)
titlegroup.add(exit.sprite)

while title:

    screen.blit(gp.loadSpriteImage('titlescreen'), (0,0))
    titlegroup.draw(screen)
    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
                gameRun = False
                pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start.isClicked():
                gameRun = True
            if exit.isClicked():
                title = False

    #Main gameloop
    while gameRun:
        
        #Sets tickrate to the game (capping fps to 60)
        clock.tick(fps)
        
        if gamewon == False:
            time += 1

        if currentBg == 1 and not chest.drawn:
            spritegroup2.add(chest.sprite)
            spritegroup2.add(paper.sprite)
            spritegroup2.add(hintbutton.sprite)
            chest.drawn = True
        elif currentBg != 1 and chest.drawn:
            spritegroup2.remove(chest.sprite)
            spritegroup2.remove(paper.sprite)
            spritegroup2.remove(hintbutton.sprite)
            chest.drawn = False

        if currentBg == 3 and floorLeft.drawn == False:
            spritegroup2.add(bridge.sprite)
            spritegroup2.add(floorLeft.sprite)
            spritegroup2.add(floorRight.sprite)
            spritegroup2.add(terminal.sprite)
            spritegroup2.add(spikes.sprite)
            spritegroup2.add(cautionSign.sprite)
            floorLeft.drawn = True
            floorRight.drawn = True
            bridge.drawn = True
            spikes.drawn = True
        elif currentBg != 3 and floorLeft.drawn:
            spritegroup2.remove(bridge.sprite)
            spritegroup2.remove(floorLeft.sprite)
            spritegroup2.remove(floorRight.sprite)
            spritegroup2.remove(terminal.sprite)
            spritegroup2.remove(spikes.sprite)
            spritegroup2.remove(cautionSign.sprite)
            floorLeft.drawn = False
            floorRight.drawn = False
            bridge.drawn = False
            spikes.drawn = False

        if currentBg == 4 and npc.drawn == False:
            spritegroup2.add(npc.sprite)
            spritegroup2.add(pilPlat.sprite)
            spritegroup2.add(pillar1.sprite)
            spritegroup2.add(pillar2.sprite)
            spritegroup2.add(pillar3.sprite)
            spritegroup2.add(disk1.sprite)
            spritegroup2.add(disk2.sprite)
            spritegroup2.add(disk3.sprite)
            spritegroup2.add(disk4.sprite)
            spritegroup2.add(disk5.sprite)
            npc.drawn = True
        elif currentBg != 4 and npc.drawn:
            spritegroup2.remove(npc.sprite)
            spritegroup2.remove(pilPlat.sprite)
            spritegroup2.remove(pillar1.sprite)
            spritegroup2.remove(pillar2.sprite)
            spritegroup2.remove(pillar3.sprite)
            spritegroup2.remove(disk1.sprite)
            spritegroup2.remove(disk2.sprite)
            spritegroup2.remove(disk3.sprite)
            spritegroup2.remove(disk4.sprite)
            spritegroup2.remove(disk5.sprite)
            npc.drawn = False

        if currentBg == 0 and hanoiPuzzle.talkedToTheFactoryMan and is_value_in_array(player.inventory, "remote") == False:
            hanoiPuzzle.drawRemote()

        #Setting playscreen background and drawing sprites
        screen.blit(bgArray[currentBg], (0,0))
        
        spritegroup2.draw(screen)
        spritegroup3.draw(screen)
        spritegroup1.draw(screen)
        

        if lockPuzzle3.getPuzzleState():
            screen.blit(lockPuzzle3.textSurf, (20,20))
            screen.blit(lockPuzzle3.lockwheel1.textSurf, (140,180))
            screen.blit(lockPuzzle3.lockwheel2.textSurf, (240,180))
            screen.blit(lockPuzzle3.lockwheel3.textSurf, (340,180))

        if lockPuzzle3.done and lockPuzzle3.notifShown == False:
            lockPuzzle3.notif.openNotification()
            player.inventory.append('factory_key')
        
        #Button press / release events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRun = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    moveLeft = True
                if event.key == pygame.K_d:
                    moveRight = True
                if event.key == pygame.K_ESCAPE and lockPuzzle3.getPuzzleState():
                    lockPuzzle3.closePuzzle()
                if event.key == pygame.K_f:
                    if lockPuzzle3.getPuzzleState() == False and player.sprite.rect.colliderect(chest.sprite) and not lockPuzzle3.done:
                        lockPuzzle3.setPuzzleState(True)
                        lockPuzzle3.openLockPuzzle()
                    if bridgePuzzle.puzzleActive == False and player.sprite.rect.colliderect(terminal.sprite):
                        bridgePuzzle.puzzleActive = True
                        bridgePuzzle.openPuzzle()
                    if lockPuzzle3.done == False and currentBg == 1 and player.sprite.rect.colliderect(paper.sprite):
                        lockPuzzle3.openHint()
                    if hanoiPuzzle.done == False and currentBg == 4 and hanoiPuzzle.dial1done == False:
                        hanoiPuzzle.openDial1()
                    if hanoiPuzzle.done == False and currentBg == 4 and hanoiPuzzle.dial1done:
                        hanoiPuzzle.openDial2()
                    if hanoiPuzzle.remoteDrawn and currentBg == 0 and player.sprite.rect.colliderect(hanoiPuzzle.remote.sprite):
                        player.inventory.append("remote")
                        pick.play()
                        hanoiPuzzle.undrawRemote()
                        hanoiPuzzle.dial1done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if currentBg == 1:
                    #Lockpuzzle3 buttons
                    if lockPuzzle3.backbutton.isClicked():
                        lockPuzzle3.closeLockPuzzle()
                    if lockPuzzle3.notif.backbutton.isClicked():
                        lockPuzzle3.notif.closeNotification()
                    if lockPuzzle3.lockwheel1.isClicked():
                        lockPuzzle3.lockwheel1.update()
                    if lockPuzzle3.lockwheel2.isClicked():
                        lockPuzzle3.lockwheel2.update()
                    if lockPuzzle3.lockwheel3.isClicked():
                        lockPuzzle3.lockwheel3.update()
                    if lockPuzzle3.hintBackButton.isClicked():
                        lockPuzzle3.closeHint()
                    if hintbutton.isClicked() and currentBg == 1:
                        showHint(lockPuzzle3.hints)
                    if hintback.isClicked():
                        unshowHint()
                    if hintnext.isClicked():
                        if lockPuzzle3.hints < 3:
                            lockPuzzle3.hints += 1
                        unshowHint()
                        showHint(lockPuzzle3.hints)
                if exit.isClicked():
                    gameRun = False
                    title = False

                #Bridgepuzzle buttons
                
                if currentBg == 3:
                    if bridgePuzzle.backbutton.isClicked():
                        bridgePuzzle.closePuzzle()
                    if bridgePuzzle.leftArr.isClicked():
                        bridgePuzzle.addIconToAnsbar('left')
                    if bridgePuzzle.rightArr.isClicked():
                        bridgePuzzle.addIconToAnsbar('right')
                    if bridgePuzzle.fivesecArr.isClicked():
                        bridgePuzzle.addIconToAnsbar('5s')
                    if bridgePuzzle.loopArr.isClicked() and not bridge.looping:
                        bridge.looping = True
                        spritegroup3.remove(bridgePuzzle.loopArr.sprite)
                        spritegroup3.add(bridgePuzzle.loopArrAct.sprite)
                    elif bridgePuzzle.loopArrAct.isClicked():
                        bridge.looping = False
                        spritegroup3.remove(bridgePuzzle.loopArrAct.sprite)
                        spritegroup3.add(bridgePuzzle.loopArr.sprite)
                    if bridgePuzzle.execBtn.isClicked():
                        bridgePuzzle.executing = True  
                    if bridgePuzzle.resetBtn.isClicked():
                        bridgePuzzle.reset() 
                        bridge.reset()

                
                #Hanoipuzzle
                if not hanoiPuzzle.done and currentBg == 4 and is_value_in_array( player.inventory, 'remote'):
                    if pillar1.isClicked():
                        if hanoiPuzzle.pillarsSelected == 0 and len(hanoiPuzzle.leftPillar) > 0:
                            hanoiPuzzle.pillarSt = 1
                            hanoiPuzzle.pillarsSelected += 1
                            pillar1.sprite.update('pillar_selected')
                        elif hanoiPuzzle.pillarsSelected == 1 and hanoiPuzzle.pillarSt != 1:
                            hanoiPuzzle.pillarDs = 1
                            hanoiPuzzle.pillarsSelected += 1
                            allPillarsUnselect(pillar1, pillar2, pillar3)
                        else:
                            hanoiPuzzle.unselect()
                            allPillarsUnselect(pillar1, pillar2, pillar3)
                    if pillar2.isClicked():
                        if hanoiPuzzle.pillarsSelected == 0 and len(hanoiPuzzle.midPillar) > 0:
                            hanoiPuzzle.pillarSt = 2
                            hanoiPuzzle.pillarsSelected += 1
                            pillar2.sprite.update('pillar_selected')
                        elif hanoiPuzzle.pillarsSelected == 1 and hanoiPuzzle.pillarSt != 2:
                            hanoiPuzzle.pillarDs = 2
                            hanoiPuzzle.pillarsSelected += 1
                            allPillarsUnselect(pillar1, pillar2, pillar3)
                        else:
                            hanoiPuzzle.unselect()
                            allPillarsUnselect(pillar1, pillar2, pillar3)    
                    if pillar3.isClicked():
                        if hanoiPuzzle.pillarsSelected == 0 and len(hanoiPuzzle.rightPillar) > 0:
                            hanoiPuzzle.pillarSt = 3
                            hanoiPuzzle.pillarsSelected += 1
                            pillar3.sprite.update('pillar_selected')
                        elif hanoiPuzzle.pillarsSelected == 1 and hanoiPuzzle.pillarSt != 3:
                            hanoiPuzzle.pillarDs = 3
                            hanoiPuzzle.pillarsSelected += 1
                            allPillarsUnselect(pillar1, pillar2, pillar3)
                        else:
                            hanoiPuzzle.unselect()
                            allPillarsUnselect(pillar1, pillar2, pillar3)
                    
                    if hanoiPuzzle.pillarsSelected == 2:
                        hanoiPuzzle.move()
                        pillar1.disks = hanoiPuzzle.leftPillar
                        pillar2.disks = hanoiPuzzle.midPillar
                        pillar3.disks = hanoiPuzzle.rightPillar

                if hanoiPuzzle.dial1back.isClicked():
                    hanoiPuzzle.closeDial1()
                if hanoiPuzzle.dial2back.isClicked():
                    hanoiPuzzle.closeDial2()
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moveLeft = False
                if event.key == pygame.K_d:
                    moveRight = False

        if currentBg != 1:
            unshowHint()
            spritegroup2.remove(hintbutton.sprite)

        if currentBg != 4:
            hanoiPuzzle.closeDial1()
            hanoiPuzzle.closeDial2()

        if currentBg == 4:
            drawDisks(hanoiPuzzle.leftPillar, hanoiPuzzle.midPillar, hanoiPuzzle.rightPillar, disk1, disk2, disk3, disk4, disk5)

        if bridgePuzzle.executing and bridgePuzzle.currSlot < len(bridgePuzzle.slots):
            if not bridge.waiting:
                execBridge(bridge, bridgePuzzle.slots[bridgePuzzle.currSlot])
                if checkPosition(bridge):
                    bridgePuzzle.currSlot = bridgePuzzle.currSlot + 1
            elif bridge.waiting:
                if bridge.tickStop == 0:
                    bridgePuzzle.currSlot += 1
                    bridge.waiting = False
                    bridge.tickStop = 200
                else:
                    bridge.tickStop -= 1
            else:
                bridgePuzzle.currSlot += 1   
        elif bridgePuzzle.executing and bridgePuzzle.currSlot == len(bridgePuzzle.slots) and bridge.looping:
            bridgePuzzle.currSlot = 0
        else:
            bridgePuzzle.executing = False
            bridgePuzzle.currSlot = 0
            
        if bridge.movingR and bridge.sprite.rect.x <= 550:
            moveBridge(bridge, 'right')
        else:
            bridge.movingR = False

        if bridge.movingL and bridge.sprite.rect.x >= 300:
            moveBridge(bridge, 'left')
        else:
            bridge.movingL = False

        if lockPuzzle3.puzzleActive:
                lockPuzzle3.checkIfDone()
                if lockPuzzle3.done:
                    player.inventory.append("factory_key")

        #Player sprite movement and background checks
        player.move()

        #Changing background if player moves over from the right side
        if player.sprite.rect.x >= 755 and currentBg < 4:
            if currentBg == 2 and not is_value_in_array(player.inventory, 'factory_key'):
                spritegroup2.add(keyprompt.sprite)
                player.sprite.rect.x = 755
            else:
                lastBg = currentBg
                currentBg = currentBg + 1
                player.sprite.rect.x = 0
        else:
            spritegroup2.remove(keyprompt.sprite)

        if player.sprite.rect.x >= 755 and currentBg == 4:
            player.sprite.rect.x = 754
        
        #-||- from the left side
        if player.sprite.rect.x <= -1 and currentBg != 0:
            lastBg = currentBg
            currentBg = currentBg - 1
            player.sprite.rect.x = 754
        

        #print(player.sprite.rect.y, " - ", currentBg)
        #Resetting player if under over certain depth in backgr3
        if player.sprite.rect.y >= 450 and player.sprite.rect.x > 20 and player.sprite.rect.x < 700 and currentBg == 3:
            splatSnd.play()
            player.sprite.rect.y = 380
            player.sprite.rect.x = 20
            player.deaths += 1

        #Blocking player from moving left in starting screen
        if player.sprite.rect.x < 0 and currentBg == 0:
            player.sprite.rect.x = 0
        
        #Removing sprites that are not part of current screen
        if currentBg != 1 or lockPuzzle3.done:
            spritegroup2.remove(chest.sprite)
            spritegroup2.remove(paper.sprite)
            chest.setDrawn(False)

        #Check if player is colliding with chest sprite
        if player.sprite.rect.colliderect(chest.sprite.rect) and chest.getDrawn():
            player.setColWithObj(True)
        elif player.getColWithObj:
            player.setColWithObj(False)

        #Check if player is colliding with factory floor sprite
        if player.sprite.rect.colliderect(floorRight.sprite.rect) and floorRight.drawn:
            player.collidingWithPlatform()
        elif player.sprite.rect.colliderect(floorLeft.sprite.rect) and floorLeft.drawn:
            player.collidingWithPlatform()
        elif player.sprite.rect.colliderect(bridge.sprite.rect) and bridge.drawn:
            player.collidingWithPlatform()
        else:
            player.fallDown()

        #Closing the lockpuzzle if player changes the screen
        if lockPuzzle3.getPuzzleState():
            if currentBg != lockPuzzle3.bgNumber:
                lockPuzzle3.closeLockPuzzle()

        #Displaying the right chest sprite in lockpuzzle screen
        if currentBg == 1 and lockPuzzle3.done:
            spritegroup2.add(open_chest.sprite)
        else:
            spritegroup2.remove(open_chest.sprite)

        if currentBg == 4 and hanoiPuzzle.done and gamewon == False:
            currentBg = currentBg + 1
            spritegroup2.empty()
            spritegroup3.empty()
            hanoiPuzzle.done = True
            totalPoints = calculatePoints(100000000, lockPuzzle3, hanoiPuzzle, time, player.deaths)
            player.points = totalPoints
            gamewon = True

        if gamewon:
            statScreen(round(player.points), lockPuzzle3, hanoiPuzzle, (time / 60), player.deaths)


        #print(currentBg)
        pygame.display.flip()
    gameRun = False


pygame.quit()
    


