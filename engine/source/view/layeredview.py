# -*- coding: utf-8 -*-
import pygame

from ..exception import GetError


class LayeredView(pygame.sprite.LayeredDirty):
    """
    manage the different layers of the game, display or hide them when required

    layers
    ##0 : background
    now, background is a special entity of LayeredDirty
    1 : elements
    2 : inventory
    3 : menu
    4 : more text

    """

    background_layer = 0
    element_layer = 1
    inventory_layer = 2
    menu_layer = 3
    text_layer = 4

    def __init__(self):
        pygame.sprite.LayeredDirty.__init__(self)
        # self._use_update = True  # apparemment nécessaire, ah non...
        self.font = pygame.font.SysFont("helvetica", 20)
        # blank_label = pygame.sprite.DirtySprite()
        # blank_label.image = pygame.Surface((400, 30), flags=pygame.SRCALPHA)
        # blank_label.rect = (20, 400, 400, 30)
        # self.add(blank_label, layer=3)  # initialize void text
        self.reset()

    def reset(self):  ## debug ?
        self.empty()
        # hors reset ? si on affiche le menu pause, ne disparaîtra pas...
        # ou même dans le __init__ d'adventurestate pour indiquer les params (et modifiables par user!)
        # this should be set manually (at least position)
        blank_label = pygame.sprite.DirtySprite()
        # blank_label.image = pygame.Surface((400, 30), flags=pygame.SRCALPHA)
        blank_label.image = pygame.Surface((400, 30))  # to see it more easily
        blank_label.rect = pygame.rect.Rect(20, 290, 100, 30)
        self.add(blank_label, layer=self.text_layer)  # initialize void text
        # donner un nom au label pour l'identifier plus facilement ?
        self.display_text("Description here", (280, 300), (255,255,255), (0,0,0))

    def loadArea(self, area):
        """
        Charge une zone en fond (couche 0)
        et tous ses objets en mid (couche 1)

        """
        self.remove_sprites_of_layer(self.background_layer)  # clear bg layer
        self.remove_sprites_of_layer(self.element_layer)  # clear item layer
        self.clear(None, area.image)  # oldie prototype
        ## OR: the background is a sprite at layer 0, and is dirtied when changing area
        for sprite in self:
            sprite.dirty = 1  # when changing background, load everything again
        # self.add(area.clickable_group.sprites(), layer=1)
        # well, we could ALSO use sprite groups, even for the console
        for item in area.item_group:
            self.add(item.area_clickable, layer=self.element_layer)
            # also show contained items if it is a container and it is open
            if hasattr(item, 'open_state') and item.open_state:  # duck-typing
                assert hasattr(item, 'content')  # no open_state without content!
                self.load_content(item)
        self.add(area.clickable_group, layer=self.element_layer) #ajout des portes

        print 'loaded area'

    def load_content(self, container):
        for contained_elt in container.content:
            self.add(contained_elt.area_clickable, layer=self.element_layer)
            # be careful, content is drawn above!

    def remove_item(self, item):
        self.remove(item)

    def remove_item_by_name(self, item_name):
        self.remove(self.get_sprite_by_name(item_name))  # or in two steps to ensure it exists

    def clearMenuLayer(self):
        self.remove_sprites_of_layer(self.menu_layer)

    def fillMenuLayer(self, menu):
        # same layer but what is added after is above
        self.add(menu, layer=self.menu_layer)
        for button in menu.buttons:
            self.add(button, layer=self.menu_layer)

    def display_menu(self):
        self.get_sprites_from_layer(self.menu_layer)[0].all_visible = 1

    def hide_menu(self):
        self.get_sprites_from_layer(self.menu_layer)[0].all_visible = 0

    def setActionText(self, text, position=None, textcolor=(255, 255, 255), bgcolor=(0, 0, 0)):
        label_image = self.font.render(text, True, textcolor, bgcolor)
        label = self.get_sprites_from_layer(self.text_layer)[0]
        label.image = label_image
        label.dirty = 1
        # if rect is not None:  # if no rect is passed, keep it!
        #     label.rect = rect
        # rect may be preserved by default or something (static text)
        # for now, let's adjust the rect whatever
        if position is not None:
            label.rect.topleft = position
        label.rect.size = label_image.get_size()

    def display_text(self, text, position, textcolor, bgcolor):
        """Affiche du texte dans la couche dédiée."""
        text_surface = self.font.render(text, True, textcolor, bgcolor)
        text_sprite = pygame.sprite.DirtySprite()  # initillay dirty
        text_sprite.image = text_surface
        text_sprite.rect = pygame.rect.Rect(position, text_surface.get_size())
        text_sprite.rect.w = 100
        self.add(text_sprite, layer=self.text_layer)  # any sprite in layer 3 but of index 0 is considered as a non action-descriptive text

    def set_text(self, text, position, index, textcolor, bgcolor):
        label_image = self.font.render(text, True, textcolor, bgcolor)
        label = self.get_sprites_from_layer(self.text_layer)[index]
        label.image = label_image
        label.dirty = 1
        if position is not None:
            label.rect.topleft = position
        label.rect.size = label_image.get_size()

    def clear_text(self):
        pass

    def displayCursor(self):
        pass

    def hideCursor(self):
        pass

    def get_sprite_by_name(self, sprite_name):
        for sprite in self:
            if sprite.codename == sprite_name:
                return sprite
        raise GetError(sprite_name, "layered view")

    def display_inventory(self):
        #self.self.get_sprites_from_layer(self.inventory_layer)[0].all_visible = 1
        pass
