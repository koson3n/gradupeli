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

#Gameplay variables
currentBg = 0
lastBg = 0
startIcon = 50

#List of backgrounds that have puzzles (nums)
#params: [background number, puzzle type, combination]
puzzleList = [[1, 'lockpuzzle', [1, 2, 3]]]

#List of lock combos
lockCombinations = [[1, 2, 3]]

#Gamesettings (60 normal, higher for testing purposes, cos the dude moves quicker)
clock = pygame.time.Clock()
fps = 400
#Character that is controlled by the player
class Player:
    def __init__(self, health, stamina, level):
        self.health = health
        self.stamina = stamina
        self.level = level
        self.colWithGameobject = False
        self.inventory = []

        self.playerSprite = gp.MovableSprite()
        self.speed = 5
        self.playerSprite.rect.y = 505

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

        self.playerSprite.rect.x += dx
        self.playerSprite.rect.y += dy

    def setColWithObj (self, bol):
        self.colWithGameobject = bol

    def getColWithObj(self):
        return self.colWithGameobject
    
    def collidingWithPlatform(self):
        self.playerSprite.rect.y = 410

    def notCollidingWithPlatform(self):
        self.playerSprite.rect.y = 505

    def fallDown(self):
        if self.playerSprite.rect.y < 505:
            self.playerSprite.rect.y = self.playerSprite.rect.y + 4

#Item within the game, that is not part of the background (sprite)
class GameItem:
    def __init__(self,name,scale):
        self.decSprite = gp.ObjectSprite(scale,name)
        self.decSprite.rect.x = 0
        self.decSprite.rect.y = 0
        self.drawn = False

    def getDrawn(self):
        return self.drawn
    
    def setDrawn (self,bol):
        self.drawn = bol

class PuzzleIcon:
    def __init__(self,name):
        self.decSprite = gp.ObjectSprite(0.6,name)
        self.decSprite.rect.x = 0
        self.decSprite.rect.y = 250
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
        self.sprite.rect.x = 200


class LockPuzzle3:   
    def __init__(self, comb, crrbg):   
        self.sprite = gp.ObjectSprite(1, 'taskbase')
        self.lockwheel1 = Button(1, 'wheel', 100, 70)
        self.lockwheel2 = Button(1, 'wheel', 200, 70)
        self.lockwheel3 = Button(1, 'wheel', 300, 70)
        self.openChest = gp.ObjectSprite(1, 'chest_open')
        #DONE = TRUE FOR TESTING PURPOSES ONLY!!!!
        self.done = False
        self.notifShown = False
        self.soundPlayed = False
        self.bgNumber = crrbg
        self.puzzleActive = False
        self.text = 'Chest has a combination lock'
        self.textSurf = getTextSurface(self.text)
        self.backbutton = Button(1, 'back_btn', 230, 330) 
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
        self.currSlot = 0
        self.comExecuting = False
        self.iconSpacing = 50
        self.iconSlots = [50,120,190,260,330]
        self.executing = False

        self.ansBox.decSprite.rect.x = 30
        self.ansBox.decSprite.rect.y = 200

    def openPuzzle(self):
        spritegroup3.add(self.sprite)
        spritegroup3.add(self.backbutton.sprite)
        spritegroup3.add(self.rightArr.sprite)
        spritegroup3.add(self.leftArr.sprite)
        spritegroup3.add(self.ansBox.decSprite)
        spritegroup3.add(self.execBtn.sprite)
        spritegroup3.add(self.loopArr.sprite)
        spritegroup3.add(self.fivesecArr.sprite)
        spritegroup3.add(self.resetBtn.sprite)
        self.puzzleActive = True

    def closePuzzle(self):
        spritegroup3.empty()
        self.emptyAnsBar()
        self.puzzleActive = False

    def addIconToAnsbar(self, icon):
        iconLeftArrow = PuzzleIcon('left_arrow')
        iconRightArrow = PuzzleIcon('right_arrow')
        iconLoopArrow = PuzzleIcon('loop_arrow')
        iconFivesecArrow = PuzzleIcon('5sek')

        if len(self.slots) >= 5:
            print('ans bar full')
            return

        if icon == '5s':
            self.slots.append(iconFivesecArrow)
        elif icon == 'left':
            self.slots.append(iconLeftArrow)
        elif icon == 'right':
            self.slots.append(iconRightArrow)
        else:
            self.slots.append(iconLoopArrow)

        for i in range(len(self.slots)):
            self.slots[i].decSprite.rect.x = self.iconSlots[i]
            spritegroup3.add(self.slots[i].decSprite)

    def emptyAnsBar(self):
        self.slots.clear()

    def reset(self):
        self.currSlot = 0
        for i in range(len(self.slots)):
            spritegroup3.remove(self.slots[i].decSprite)
        self.emptyAnsBar()
        



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
        
#Future development
class Enemy:
    def __init__(self):
        print("nothing here yet")

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
    
#Variables for various purposes in the loop
gameRun = True

#Gamescreen setup
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Placeholder_videogame_name')
player = Player(100, 100, 1)
bgArray = gp.backgroundArrayLoader('bg')


#Puzzleitems for BACKGR 1
chest = GameItem('env_chest3', 0.5)
chest.decSprite.rect.x = 250
chest.decSprite.rect.y = 500
open_chest = GameItem('chest_open', 0.3)
open_chest.decSprite.rect.x = 250
open_chest.decSprite.rect.y = 465
lockPuzzle3 = LockPuzzle3([1,2,3], 1)

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
terminal.decSprite.rect.x = 200
terminal.decSprite.rect.y = 400
bridgePuzzle = BridgePuzzle()

#Spritegrouping
#group 1: player (drawn last = on top)
spritegroup1 = pygame.sprite.Group()
spritegroup1.add(player.playerSprite)

#group 2: interactive items
spritegroup2 = pygame.sprite.Group()

#group 3: puzzle stuff
spritegroup3 = pygame.sprite.Group()

chestSnd = snd.loadSound("chest_open_snd")

#Main gameloop
while gameRun:
    
    #Sets tickrate to the game (capping fps to 60)
    clock.tick(fps)

    if currentBg == 3 and floorLeft.drawn == False:
        spritegroup2.add(bridge.sprite)
        spritegroup2.add(floorLeft.sprite)
        spritegroup2.add(floorRight.sprite)
        spritegroup2.add(terminal.decSprite)
        floorLeft.drawn = True
        floorRight.drawn = True
        bridge.drawn = True
    elif currentBg != 3 and floorLeft.drawn:
        spritegroup2.remove(bridge.sprite)
        spritegroup2.remove(floorLeft.sprite)
        spritegroup2.remove(floorRight.sprite)
        spritegroup2.remove(terminal.decSprite)
        floorLeft.drawn = False
        floorRight.drawn = False
        bridge.drawn = False

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
                if lockPuzzle3.getPuzzleState() == False and player.playerSprite.rect.colliderect(chest.decSprite) and not lockPuzzle3.done:
                    lockPuzzle3.setPuzzleState(True)
                    lockPuzzle3.openLockPuzzle()
                if bridgePuzzle.puzzleActive == False and player.playerSprite.rect.colliderect(terminal.decSprite):
                    bridgePuzzle.puzzleActive = True
                    bridgePuzzle.openPuzzle()

        if event.type == pygame.MOUSEBUTTONDOWN:
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

            #Bridgepuzzle buttons
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
             
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moveLeft = False
            if event.key == pygame.K_d:
                moveRight = False

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

    #Player sprite movement and background checks
    player.move()

    #Changing background if player moves over from the right side
    if player.playerSprite.rect.x >= 755:
        lastBg = currentBg
        currentBg = currentBg + 1
        player.playerSprite.rect.x = 0
        if currentBg == 1 and lastBg == 0:
            spritegroup2.add(chest.decSprite)
            chest.setDrawn(True)
    
    #-||- from the left side
    if player.playerSprite.rect.x <= -1 and currentBg != 0:
        lastBg = currentBg
        currentBg = currentBg - 1
        player.playerSprite.rect.x = 754
        if currentBg == 1 and lastBg == 2:
            spritegroup2.add(chest.decSprite)
            chest.setDrawn(True)

    #Blocking player from moving left in starting screen
    if player.playerSprite.rect.x < 0 and currentBg == 0:
        player.playerSprite.rect.x = 0
    
    #Removing sprites that are not part of current screen
    if currentBg != 1 or lockPuzzle3.done:
        spritegroup2.remove(chest.decSprite)
        chest.setDrawn(False)

    #Check if player is colliding with chest sprite
    if player.playerSprite.rect.colliderect(chest.decSprite.rect) and chest.getDrawn():
        player.setColWithObj(True)
    elif player.getColWithObj:
        player.setColWithObj(False)

    #Check if player is colliding with factory floor sprite
    if player.playerSprite.rect.colliderect(floorRight.sprite.rect) and floorRight.drawn:
        player.collidingWithPlatform()
    elif player.playerSprite.rect.colliderect(floorLeft.sprite.rect) and floorLeft.drawn:
        player.collidingWithPlatform()
    elif player.playerSprite.rect.colliderect(bridge.sprite.rect) and bridge.drawn:
        player.collidingWithPlatform()
    else:
        player.fallDown()

    #Closing the lockpuzzle if player changes the screen
    if lockPuzzle3.getPuzzleState():
        if currentBg != lockPuzzle3.bgNumber:
            lockPuzzle3.closeLockPuzzle()

    #Displaying the right chest sprite in lockpuzzle screen
    if currentBg == 1 and lockPuzzle3.done:
        spritegroup2.add(open_chest.decSprite)
    else:
        spritegroup2.remove(open_chest.decSprite)

    #print(currentBg)
    pygame.display.flip()

pygame.quit()
    


