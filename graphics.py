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
class ObjectSprite (pygame.sprite.Sprite):
    def __init__(self, scale: int = 1, name: str = '', x: int = 0, y: int = 0):
        super().__init__()
        self.scale = scale
        self.name = name
        self.image = loadSpriteImage(name)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.scale = scale
        self.image = pygame.transform.scale_by(self.image, scale)
        self.rect.x = x
        self.rect.y = y
        
    def __repr__(self):
        return f"Scale: {self.scale}, name: {self.name}"
    
    def update(self, new_image_file):
        self.image = loadSpriteImage(new_image_file)
    
def getPlayerSprite():   
    sprite = MovableSprite()
    return sprite

def loadSpriteImage(fname):
    imgpath = f"{ASSET_FOLDER}/{fname}.png"
    img = pygame.image.load(imgpath).convert_alpha()
    return img

def backgroundArrayLoader(fname):
    bgImageArray = []
    for i in range(6):
        imgpath = f"{ASSET_FOLDER}/{fname}{i}.png"
        img = pygame.image.load(imgpath).convert()
        bgImageArray.append(img)
    return bgImageArray

def loadSound (fname):
    snd = pygame.mixer.Sound(f"{ASSET_FOLDER}/{fname}.wav")
    return snd


        
        
