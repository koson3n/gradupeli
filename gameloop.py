import pygame
import graphics as gp

SCREENWIDTH = 800
SCREENHEIGHT = 600

class Player:
    def __init__(self, health, stamina, level):
        self.health = health
        self.stamina = stamina
        self.level = level
        self.playerSprite = gp.getPlayerSprite()
    def __repr__(self):
        return f"Health: {self.health}, Stam: {self.stamina}, Level: {self.level}"

class Enemy:
    def __init__(self):
        print("nothing here yet")

class Game: 

    #For future pre-launch settings
    def __init__(self, x):
        self.x = x        
    def __repr__(self):
       return f"x = {self.x}"
    
    
#Variables for various purposes in the loop
gameRun = True
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('HackerMan64')
player = Player(100, 100, 1)
background = gp.loadImage('bg0.png')
#background = pygame.transform.smoothscale(background, screen.get_size())

spritegroup1 = pygame.sprite.Group()
spritegroup1.add(player.playerSprite)
    

#Main gameloop
while gameRun:
    
    screen.blit(background, (0,0))
    spritegroup1.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRun = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        print(player)

    pygame.display.flip()


pygame.quit()
    


