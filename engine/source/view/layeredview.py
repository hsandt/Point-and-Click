# -*- coding: utf-8 -*-
import pygame


class LayeredView(pygame.sprite.LayeredUpdates):
    """manage the different layers of the game, display or hide them when required"""
    def __init__(self):
        pygame.sprite.LayeredUpdates.__init__(self)

    def loadArea(self, area):
        """
        Charge une zone en fond (couche 0)
        et tous ses objets en mid (couche 1)

        """
        self.add(area, layer=0)
        self.add(area.element_group.sprites(), layer=1)
        print 'loaded area'

    def clearMenuLayer(self):
        pass

    def fillMenuLayer(self):
        pass

    def displayText(text):
        pass

    def clearText(self):
        pass

    def displayCursor(self):
        pass

    def hideCursor(self):
        pass
