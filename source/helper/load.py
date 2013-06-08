# -*- coding: utf-8 -*-

import os, sys
import pygame
from files import get_full_path
from ..exception.exception import LoadError


<<<<<<< HEAD:source/helper/load.py
def load_image(name, colorkey=None):
    """helper to load images with transparency"""
    fullname = os.path.join(get_full_path('test_resource', name))
=======
def load_image(image_path, colorkey=None):
    """helper to load images with transparency"""

>>>>>>> ee77143d4afc8f0aaa9f75b5692f9d56ca47118f:engine/source/helper/load.py
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print 'Cannot load image:', name
        raise LoadError(name, message)
    else:
        image = image.convert()

        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
                # print(colorkey)
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        else:
            image.convert_alpha()
<<<<<<< HEAD:source/helper/load.py

=======
        return image


def load_descriptions(file_path):
    """
    Load a hash of codename: description for all the items,
    and return it.

    """
    description_hash = {}
    with open(file_path) as f:
        for line in f:
            info = line.split(None, 1)  # format: %item_name%<tab>%description%
            description_hash[info[0]] = info[1]
    return description_hash
>>>>>>> ee77143d4afc8f0aaa9f75b5692f9d56ca47118f:engine/source/helper/load.py
