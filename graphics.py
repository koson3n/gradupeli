import os
import pygame

ASSET_FOLDER = 'assets/'

class MovableSprite (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = loadSpriteImage('char0.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
    
class DecorationSprite:
    def __init__(self, scale):
        self.scale = scale

    def __repr__(self):
        return f"Scale: {self.scale}"
    
class InteractiveSprite:
    def __init__(self,scale,rarity):
        self.scale = scale
        self.rarity = rarity

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
    imgpath = f"{ASSET_FOLDER}/{fname}"
    img = pygame.image.load(imgpath).convert_alpha()
    return img




        
        
