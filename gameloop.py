import pygame
import graphics as gp

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

        self.playerSprite = gp.getPlayerSprite()
        self.speed = 5
        self.playerSprite.rect.y = 505

    def __repr__(self):
        return f"Health: {self.health}, Stam: {self.stamina}, Level: {self.level}"
    
    #Player movement
    def move (self):
        dx = 0
        dy = 0

        if moveLeft:
            dx = -self.speed
        if moveRight:
            dx = self.speed

        self.playerSprite.rect.x += dx
        self.playerSprite.rect.y += dy

#Item within the game, that is not part of the background (sprite)
class GameItem:
    def __init__(self,name,scale):
        self.decSprite = gp.InteractiveSprite(scale,name)
        self.decSprite.rect.x = 0
        self.decSprite.rect.y = 0

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
    
    
#Variables for various purposes in the loop
gameRun = True

#Gamescreen setup
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('HackerMan64')
player = Player(100, 100, 1)
bgArray = gp.backgroundArrayLoader('bg')

#Puzzleitems
chest = GameItem('chest3', 0.5)

#Spritegrouping
spritegroup1 = pygame.sprite.Group()
spritegroup1.add(player.playerSprite)
#spritegroup1.add(chest.decSprite)
    
#Main gameloop
while gameRun:
    
    #Sets tickrate to the game (caps it rather)
    clock.tick(fps)

    #Setting playscreen background and drawing sprites
    screen.blit(bgArray[currentBg], (0,0))
    spritegroup1.draw(screen)

    #Button press / release events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRun = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moveLeft = True
            if event.key == pygame.K_d:
                moveRight = True

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
            spritegroup1.add(chest.decSprite)
    
    #-||- from the left side
    if player.playerSprite.rect.x <= -1 and currentBg != 0:
        lastBg = currentBg
        currentBg = currentBg - 1
        player.playerSprite.rect.x = 754
        if currentBg == 1 and lastBg == 2:
            spritegroup1.add(chest.decSprite)

    #Blocking player from moving left in starting screen
    if player.playerSprite.rect.x < 0 and currentBg == 0:
        player.playerSprite.rect.x = 0
    
    #Removing sprites that are not part of current screen
    if currentBg != 1:
        spritegroup1.remove(chest.decSprite)

    print(currentBg)
    pygame.display.flip()

pygame.quit()
    


