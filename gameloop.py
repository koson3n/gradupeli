import pygame
import graphics as gp

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

#Gamesettings
clock = pygame.time.Clock()
fps = 60

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

class PuzzleScreen:
    def __init__(self, bgNumber):
        self.sprite = gp.ObjectSprite(1, 'taskbase')
        self.puzzleActive = False
        self.bgNumber = bgNumber
        self.text = "moi"
        self.backbutton = Button(1, 'back_btn', 230, 330)

    def closePuzzle(self):
        spritegroup3.empty()
        self.puzzleActive = False

    def openPuzzle(self):
        spritegroup3.add(self.sprite)
        spritegroup3.add(self.backbutton.sprite)
        self.puzzleActive = True


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

    def isClicked(self):
        mousePos = pygame.mouse.get_pos()
        return self.sprite.rect.collidepoint(mousePos)

def drawText(text):
    font = pygame.font.SysFont(None, 30)
    return font.render(text, True, (0, 0, 0))

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

puzzleScreen = PuzzleScreen(1)
#backbtn = Button(1, 'back_btn', 230, 330)

#Spritegrouping
#group 1: player (drawn last = on top)
spritegroup1 = pygame.sprite.Group()
spritegroup1.add(player.playerSprite)

#group 2: interactive items
spritegroup2 = pygame.sprite.Group()

#group 3: decoration 
spritegroup3 = pygame.sprite.Group()

#Main gameloop
while gameRun:
    
    #Sets tickrate to the game (capping fps to 60)
    clock.tick(fps)

    if puzzleScreen.puzzleActive:
        screen.blit(drawText("Moi"), (10,10))

    #Setting playscreen background and drawing sprites
    screen.blit(bgArray[currentBg], (0,0))
    spritegroup2.draw(screen)
    spritegroup1.draw(screen)
    spritegroup3.draw(screen)

    if puzzleScreen.puzzleActive:
        screen.blit(drawText("Moi"), (30,30))
    
    #Button press / release events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRun = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moveLeft = True
            if event.key == pygame.K_d:
                moveRight = True
            if event.key == pygame.K_ESCAPE and puzzleScreen.puzzleActive:
                puzzleScreen.closePuzzle()
            if event.key == pygame.K_f and player.getColWithObj and puzzleScreen.puzzleActive == False:
                puzzleScreen.openPuzzle()

        if event.type == pygame.MOUSEMOTION:
            print(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONDOWN:
            if puzzleScreen.backbutton.isClicked():
                puzzleScreen.closePuzzle()

            

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moveLeft = False
            if event.key == pygame.K_d:
                moveRight = False

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
    if currentBg != puzzleScreen.bgNumber:
        spritegroup3.remove(puzzleScreen.sprite)
        puzzleScreen.puzzleActive = False

    #print(currentBg)
    pygame.display.flip()

pygame.quit()
    


