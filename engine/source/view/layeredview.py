# -*- coding: utf-8 -*-
import pygame

from ..view import views
from ..model import models
from ..helper.load import load_image
from ..exception import GetError


class LayeredView(pygame.sprite.LayeredDirty):
    """
    manage the different layers of the game, display or hide them when required

    layers
    # OLD: 0 : background
    -> now, background has a special place in LayeredDirty
    1 : elements
    2 : inventory
    3 : menu
    4 : text (including pause menu)

    """

    background_layer = 0
    item_layer = 1
    inventory_layer = 2
    menu_layer = 3
    text_layer = 4
    pause_layer = 5

    def __init__(self):
        pygame.sprite.LayeredDirty.__init__(self)
        self.font = pygame.font.SysFont("helvetica", 20)
        self.reset()

    def reset(self):  ## debug ?
        self.empty()  # warning, does not cut observers off
        # le label de description pourrait éventuellement observer un modèle contenu les infos texte...
        self.display_text("Description here", (280, 250), (255,255,255), (0,0,0))

    def load_area(self, area):
        """
        Charge une zone en fond (couche 0)
        et crée les vues pour les objets et portes en mid (couche 1)

        """
        self.remove_sprites_of_layer(self.background_layer)  # clear bg layer
        self.remove_sprites_of_layer(self.item_layer)  # clear item layer
        background = pygame.sprite.DirtySprite()
        background.image = load_image(area.image_path)
        background.rect = background.image.get_rect()
        self.add(background, layer=self.background_layer)
        ## OR: the background is a sprite at layer 0, and is dirtied when changing area
        for sprite in self:
            sprite.dirty = 1  # when changing background, load everything again
        # self.add(area.clickable_group.sprites(), layer=1)
        # well, we could ALSO use sprite groups, even for the console
        for element in area.children:
            if element.tag == 'item':
                # on crée la vue de l'objet dans la zone, qui est
                # automatiquement associée à l'objet dans les deux sens,
                # et on l'ajoute à la couche des objets et portes
                self.add(views.AreaItemClickable(element), layer=self.item_layer)
                # also show contained items if it is a container and it is open
                if hasattr(element, 'content'):  # duck-typing
                    # even if the container is closed, load its content
                    # they will simply be hidden for now
                    self.load_content(element)
            else:
                # il doit s'agir d'une porte
                self.add(views.GateClickable(element), layer=self.item_layer)

        print 'loaded area'

    def load_content(self, container):
        for contained_elt in container.content:
            self.add(models.AreaItemClickable(contained_elt), layer=self.item_layer)
            # be careful, content is drawn above!

    def load_menu(self, menu):
        # menu and buttons on the same layer, but what is added after is above
        self.add(views.AdventureMenuView(menu), layer=self.menu_layer)
        for button in menu.buttons:
            # uniquement des verb buttons pour l'instant
            self.add(views.VerbButtonClickable(button), layer=self.menu_layer)

    def load_action_label(self, action_subject, image_path, position, textcolor, bgcolor, visible):
        self.add(views.ActionLabel(action_subject, image_path, position, visible, textcolor, bgcolor), layer=self.text_layer)

    def load_inventory(self, inventory):
        """Load the inventory (call it once)"""
        inventory_view = views.InventoryView(inventory)
        print "now on inventory layer: %s", self.get_sprites_from_layer(self.inventory_layer)
        self.add(inventory_view, layer=self.inventory_layer)
        print "now on inventory layer: %s", self.get_sprites_from_layer(self.inventory_layer)
        print "inventory has been loaded, now on inventory layer: %s", self.get_sprites_from_layer(self.inventory_layer)

    def add_item_view_to_inventory(self, item):
        self.add(views.InventoryItemClickable(item), layer=self.inventory_layer)

    def add_item_view_to_area(self, item):
        self.add(views.AreaItemClickable(item), layer=self.item_layer)

    # warning: adds text without properly indexing, needs improvement
    def display_text(self, text, position, textcolor, bgcolor, layer=None):
        """Affiche du texte dans la couche dédiée."""
        text_sprite = pygame.sprite.DirtySprite()  # initially dirty
        text_sprite.image = None
        text_sprite.rect = pygame.rect.Rect(0,0,0,0)
        # any sprite in layer 3 but of index 0 is considered as a non action-descriptive text
        if layer is None:
            # par défaut, la couche des textes
            layer = self.text_layer
        self.add(text_sprite, layer=layer)  # add the mock sprite
        # then give it substance
        self.set_text(text, position, -1, textcolor, bgcolor)

    # use it only for custom text such as descriptions, use an observer for anything bound to a model
    def set_text(self, text, position, index, textcolor, bgcolor):
        label_image = self.font.render(text, True, textcolor, bgcolor)
        label = self.get_sprites_from_layer(self.text_layer)[index]
        label.image = label_image
        label.dirty = 1
        if position is not None:
            label.rect.topleft = position
        label.rect.size = label_image.get_size()
        # attention, les textes changeant de taille, la détection des dirty sprites peut être erronée

    # same remark
    def move_text(self, position, index):
        label = self.get_sprites_from_layer(self.text_layer)[index]
        label.rect.topleft = position
        label.dirty = 1

    def displayCursor(self):
        """en développement"""
        pass

    def hideCursor(self):
        """en développement"""
        pass

    # deprecated (or have ANY sprite have a name)
    def get_sprite_by_name(self, sprite_name):
        print "looking for sprite with name: " + sprite_name
        for sprite in self:
            print sprite
            if sprite.codename == sprite_name:
                return sprite
        raise GetError(sprite_name, "layered view")

    # deprecated (or have ANY sprite have a name)
    def get_sprite_by_name_in_layer(self, sprite_name, layer):
        print "looking for sprite with name: " + sprite_name
        for sprite in self.get_sprites_from_layer(layer):
            print sprite
            if sprite.codename == sprite_name:
                return sprite
        raise GetError(sprite_name, "layered view")

    def hide_layer(self, layer):
        for sprite in self.get_sprites_from_layer(layer):
            sprite.visible = 0

    def display_layer(self, layer):
        for sprite in self.get_sprites_from_layer(layer):
            sprite.visible = 1

def get_relative_position_for(index):
    """Helper donnant la position relative dans l'inventaire"""
    # TODO : module (plusieurs lignes) et flèches (pour plus d'objets que l'espace ne le permet) + personnalisation par le concepteur
    return (40 + 100 * index, 20)