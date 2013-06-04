# -*- coding: utf-8 -*-
import pygame


class LayeredView(pygame.sprite.LayeredUpdates):
    """
    manage the different layers of the game, display or hide them when required

    layers
    0 : background
    1 : elements
    2 : menu
    3 : more text

    """
    def __init__(self):
        pygame.sprite.LayeredUpdates.__init__(self)
        self.font = pygame.font.SysFont("helvetica", 20)
        # blank_label = pygame.sprite.Sprite()
        # blank_label.image = pygame.Surface((400, 30), flags=pygame.SRCALPHA)
        # blank_label.rect = (20, 400, 400, 30)
        # self.add(blank_label, layer=3)  # initialize void text
        self.reset()

    def reset(self):  ## debug ?
        self.empty()
        blank_label = pygame.sprite.Sprite()
        blank_label.image = pygame.Surface((400, 30), flags=pygame.SRCALPHA)
        blank_label.rect = (20, 200, 400, 30)
        self.add(blank_label, layer=3)  # initialize void text

    def loadArea(self, area):
        """
        Charge une zone en fond (couche 0)
        et tous ses objets en mid (couche 1)

        """
        self.empty()  # don't forget to reset!
        self.add(area, layer=0)
        self.add(area.clickable_group.sprites(), layer=1)
        print 'loaded area'

    def remove_item(self, item):
        self.remove(item)

    def clearMenuLayer(self):
        pass

    def fillMenuLayer(self, menu):
        # same layer but what is added after is above
        self.add(menu, layer=2)
        for button in menu.buttons:
            self.add(button, layer=2)

    def displayText(self, text, rect, textcolor, bgcolor):
        print 'display Text'
        label_image = self.font.render(text, True, textcolor, bgcolor)
        label = self.get_sprites_from_layer(3)[0]
        label.image = label_image
        label.rect = rect
        # rect may be preserved by default or something (static text)

    def clearText(self):
        pass

    def displayCursor(self):
        pass

    def hideCursor(self):
        pass
