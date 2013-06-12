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
        if colorkey is not None:
            image = image.convert()
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
                # print(colorkey)
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        else:
            image.convert_alpha()
        return image


def load_descriptions(file_path):
    """
    Load a hash of codename: description for all the items,
    and return it.

    """
    description_hash = {}
    with open(file_path) as f:
        for line in f:
            info = line.strip().split(None, 1)  # format: %item_name%<tab>%description%\n
            description_hash[info[0]] = info[1]
    return description_hash
