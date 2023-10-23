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

#List of backgrounds that have puzzles (nums)
#params: [background number, puzzle type, combination]
puzzleList = [[1, 'lockpuzzle', [1, 2, 3]]]

#List of lock combos
lockCombinations = [[1, 2, 3]]

#Gamesettings (60 normal, higher for testing purposes, cos the dude moves quicker)
clock = pygame.time.Clock()
fps = 200

#Character that is controlled by the player
class Player:
    def __init__(self, health, stamina, level):
        self.health = health
        self.stamina = stamina
        self.level = level
        self.colWithGameobject = False

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

class LockPuzzle3:   
    def __init__(self, comb, crrbg):   
        self.sprite = gp.ObjectSprite(1, 'taskbase')
        self.lockwheel1 = Button(1, 'wheel', 100, 70)
        self.lockwheel2 = Button(1, 'wheel', 200, 70)
        self.lockwheel3 = Button(1, 'wheel', 300, 70)
        self.openChest = gp.ObjectSprite(1, 'chest_open')
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

    def checkIfDone (self):
        if self.lockwheel1.currNum == self.comb1 and self.lockwheel2.currNum == self.comb2 and self.lockwheel3.currNum == self.comb3:
            if self.soundPlayed == False:
                chestSnd.play()
                self.soundPlayed = True
            self.closeLockPuzzle()
            self.done = True

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
    
class Notification:
    def __init__(self, txt):
        self.text = txt
        self.sprite = gp.ObjectSprite(1, 'notificationbase')
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
    def __init__(self,scale,name,x,y):
        self.name = name
        self.scale = scale
        self.sprite = gp.ObjectSprite(1, name,x,y)
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

#Variables for various purposes in the loop
gameRun = True

#Gamescreen setup
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Placeholder_videogame_name')
player = Player(100, 100, 1)
bgArray = gp.backgroundArrayLoader('bg')

#Puzzleitems
chest = GameItem('env_chest3', 0.5)
chest.decSprite.rect.x = 250
chest.decSprite.rect.y = 500

lockPuzzle3 = LockPuzzle3([1,2,3], 1)

doneNotif = Notification("The chest opens! You found a key from the chest!")

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

    #Setting playscreen background and drawing sprites
    screen.blit(bgArray[currentBg], (0,0))
    spritegroup2.draw(screen)
    spritegroup1.draw(screen)
    spritegroup3.draw(screen)

    if lockPuzzle3.getPuzzleState():
        screen.blit(lockPuzzle3.textSurf, (20,20))
        screen.blit(lockPuzzle3.lockwheel1.textSurf, (140,180))
        screen.blit(lockPuzzle3.lockwheel2.textSurf, (240,180))
        screen.blit(lockPuzzle3.lockwheel3.textSurf, (340,180))

    if lockPuzzle3.done and (lockPuzzle3.notifShown == False):
        doneNotif.openNotification()
        screen.blit(doneNotif.textSurf, (20,20))
    
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
            if event.key == pygame.K_f and player.getColWithObj and lockPuzzle3.getPuzzleState() == False:
                lockPuzzle3.setPuzzleState(True)
                lockPuzzle3.openLockPuzzle()
                

        if event.type == pygame.MOUSEMOTION:
            #print(pygame.mouse.get_pos())
            print(lockPuzzle3.getPuzzleState())

        if event.type == pygame.MOUSEBUTTONDOWN:
            if lockPuzzle3.backbutton.isClicked():
                lockPuzzle3.closeLockPuzzle()
            if doneNotif.backbutton.isClicked():
                doneNotif.closeNotification()
            if lockPuzzle3.lockwheel1.isClicked():
                lockPuzzle3.lockwheel1.update()
            if lockPuzzle3.lockwheel2.isClicked():
                lockPuzzle3.lockwheel2.update()
            if lockPuzzle3.lockwheel3.isClicked():
                lockPuzzle3.lockwheel3.update()
             
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moveLeft = False
            if event.key == pygame.K_d:
                moveRight = False

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
    if currentBg != 1:
        spritegroup2.remove(chest.decSprite)
        chest.setDrawn(False)

    #Check if player is colliding with another sprite
    if player.playerSprite.rect.colliderect(chest.decSprite.rect) and chest.getDrawn():
        player.setColWithObj(True)
    elif player.getColWithObj:
        player.setColWithObj(False)

    #Closing the puzzle if player changes the screen
    if lockPuzzle3.getPuzzleState():
        if currentBg != lockPuzzle3.bgNumber:
            lockPuzzle3.closeLockPuzzle()

    #print(currentBg)
    pygame.display.flip()

pygame.quit()
    


