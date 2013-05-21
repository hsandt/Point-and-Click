# -*- coding: utf-8 -*-

import os, sys
import pygame
from files import get_full_path

def load_image(name, colorkey=None):
    """helper to load images with transparency"""
    fullname = os.path.join(get_full_path('resource', name))
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print 'Cannot load image:', name
        raise LoadException (message) # pas ultra
    else:
        image = image.convert()

        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
                # print(colorkey)
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        else:
            image.convert_alpha()

