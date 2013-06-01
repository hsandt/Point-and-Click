# -*- coding: utf-8 -*-

import os, sys
import pygame
from ..exception.exception import LoadError

def load_image(image_path, colorkey=None):
    """helper to load images with transparency"""
    
    try:
        image = pygame.image.load(image_path)
    except pygame.error as message:
        print 'Cannot load image at:', image_path
        # never reached, pygame stops it here!
        raise LoadError(image_path, message)
    else:
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
                # print(colorkey)
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        else:
            image.convert_alpha()
        return image