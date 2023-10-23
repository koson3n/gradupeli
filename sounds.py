import os
import pygame

ASSET_FOLDER = 'assets/'

def loadSound (fname):
    snd = pygame.mixer.Sound(f"{ASSET_FOLDER}/{fname}.wav")
    return snd