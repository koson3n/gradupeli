import os
import pygame

ASSET_FOLDER = 'assets/'

environmentSprites = []

#Moving sprites, eg players and enemies
class MovableSprite (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = loadSpriteImage('char0')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

#Sprites that have are non-moving and non-interactable    
class DecorationSprite (pygame.sprite.Sprite):
    def __init__(self, scale, name):
        super().__init__()
        self.scale = scale
        self.name = name

    def __repr__(self):
        return f"Scale: {self.scale}, name: {self.name}"

#Sprites that have some amount of interaction
class InteractiveSprite (pygame.sprite.Sprite):
    def __init__(self,scale,name):
        super().__init__()
        self.image = loadEnvironmentSpriteImage(name)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.name = name
        
        #Scaling the object to desired size
        self.scale = scale
        self.image = pygame.transform.scale_by(self.image, scale)

    def __repr__(self):
        return f"Scale: {self.scale}, Rarity: {self.rarity}"
    
def getPlayerSprite():   
    sprite = MovableSprite()
    return sprite
    
def loadImage(fname):
    imgpath = f"{ASSET_FOLDER}/{fname}"
    img = pygame.image.load(imgpath).convert()
    return img

def loadSpriteImage(fname):
    imgpath = f"{ASSET_FOLDER}/{fname}.png"
    img = pygame.image.load(imgpath).convert_alpha()
    return img

def backgroundArrayLoader(fname):
    bgImageArray = []
    for i in range(2):
        imgpath = f"{ASSET_FOLDER}/{fname}{i}.png"
        img = pygame.image.load(imgpath).convert()
        bgImageArray.append(img)
    return bgImageArray

def loadEnvironmentSpriteImage(fname):
    imgpath = f"{ASSET_FOLDER}/env_{fname}.png"
    img = pygame.image.load(imgpath).convert_alpha()
    return img




        
        
