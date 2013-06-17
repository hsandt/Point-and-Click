# -*- coding: utf-8 -*-

import pygame
from .observer import Observer
from ..helper import load_image
from ..exception import AbstractMethodError


class ElementView(pygame.sprite.DirtySprite, Observer):
    """
    Vue associée à un modèle (sujet) (classe abstraite)

    Attributs hérités :
        image       -- image du sprite utilisé (à initialiser soi-même)
        rect        -- rect du sprite utilisé (à initialiser)
        visible     -- visibilité du sprite
        dirty       -- salissure du sprite
        mask        -- masque pour la détection de clics (à initialiser)

    Attributs propres :
        subject_list -- liste des sujets d'observation

    """

    def __init__(self, image_path, position, visible):
        """Initialise les attributs visuels et d'observation"""
        pygame.sprite.DirtySprite.__init__(self)
        Observer.__init__(self)
        # monochromatic surface instead of images may be allowed later
        self.image = load_image(image_path)
        self.rect = pygame.Rect(position, self.image.get_size())
        self.mask = pygame.mask.from_surface(self.image)  # use it!
        self.visible = visible  # TODO: should affect detection

        self.subject_list = []

    def change_image(self, image_path):
        self.image = load_image(image_path)
        self.dirty = 1  # TODO: check if a smaller image works
        self.rect.size = self.image.get_size()

    def update_visibility(self):
        """update for the aspect of visibility"""
        for subject in self.subject_list:
            if not subject.visible:
                self.visible = 0
        self.visible = 1

    def update_position(self):
        """update for the aspect of positioning by summing all the relative positions to the next parent"""
        self.rect.topleft = (0, 0)
        for subject in self.subject_list:
            self.rect.move_ip(*subject.view_position)

    def bind_subject(self, subject):
        self.subject_list.append(subject)
        subject.attach(self)

    def recursive_bind_subject(self, subject):
        """Bind recursively to the subject and all its parents"""
        self.bind_subject(subject)
        if subject.parent is not None:
            self.recursive_bind_subject(subject.parent)

    def cutoff_subject(self, subject):
        self.subject_list.remove(subject)
        subject.detach(self)

    def clear_subjects(self):
        for subject in self.subject_list:
            self.cutoff_subject(subject)

    def destroy(self):
        # call mother classes' destructors
        self.kill()  # remove references from all groups containing this sprite
        self.clear_subjects()  # remove references (bidirectional) as an observer


class Clickable(ElementView):
    """
    ElementView disposant d'un comportement face au clic (classe abstraite)

    Attributs hérités :
        image       -- image du sprite utilisé (à initialiser soi-même)
        rect        -- rect du sprite utilisé (à initialiser)
        visible     -- visibilité du sprite
        dirty       -- salissure du sprite
        mask        -- masque pour la détection de clics (à initialiser)

    Attributs propres :
        default_right_verb    -- verbe appelé par défaut sur un clic droit

    """

    def __init__(self, image_path, position, visible):
        """Initialise les attributs visuels et d'obervation"""
        ElementView.__init__(self, image_path, position, visible)
        self.default_right_verb = None

    def on_click(self, adventurestate, button):
        """Opération déclenchée sur un clic avec le bouton 'button' :
        button == 1 : clic gauche
        button == 2 : clic droit

        Doit être overridden

        """
        raise AbstractMethodError(self.__class__.__name__, "on_click")


class ItemClickable(Clickable):
    """
    Sprite associé à un objet (class abstraite)

    Attributs hérités :
        image
        rect
        visible
        dirty
        mask
        subject

    Attributs propres :
        item          -- objet observé (sujet)
        specific_verb -- verbe appelé automatiquement sur un clic droit

    """
    def __init__(self, item, visible):
        Clickable.__init__(self, image_path=item.area_image_path, position=item.area_position, visible=visible)
        self.recursive_bind_subject(item)

        self.specific_verb = None

    def on_click(self, adventurestate, button):

        # on distingue les types de clic pour trouver le verbe approprié
        if button == 1:  # clic gauche
            # on vérifie si un verbe a été sélectionné au préalable
            if adventurestate.verb is None:
                # si aucun verbe n'est précisé, on utilise le verbe par défaut comme verbe courant
                adventurestate.verb = self.adventure_state.default_verb
            # sinon, le verbe courant est déjà le bon
        else:
            # pour un clic droit, le verbe spécifique de l'objet est toujours choisi comme verbe courant
            adventurestate.verb = self.specific_verb
        
        # on applique le verbe ainsi obtenu
        if hasattr(self.item, adventurestate.verb):
            # si l'action est connue de la part de l'item,
            # on applique la méthode éponyme de l'objet
            if getattr(self.item, adventurestate.verb)(adventurestate):
                # si True est renvoyé, l'action a été complétée (elle n'exige pas de complément supplémentaire)
                del adventurestate.verb
                del adventurestate.complement
        else:
            # si l'action est inconnue, c'est le message 'rien à faire' par défaut
            adventurestate.display_description("I cannot %s %s." % (adventurestate.verb, self.item.fullname))
            del adventurestate.verb
            del adventurestate.complement

    @property
    def item(self):
        return self.subject_list[0]


class AreaItemClickable(ItemClickable):
    """
    Sprite associé à un objet, apparaissant dans la zone

    Attributs hérités :
        image         -- image de l'objet dans la zone
        rect
        visible
        dirty
        mask
        subject
        item          -- objet observé (sujet)
        specific_verb -- verbe appelé automatiquement sur un clic droit

    """
    def __init__(self, item, visible=1):
        ItemClickable.__init__(self, item, visible)

        if hasattr(item, 'open'):
            # un conteneur duck-typed est par défaut ouvert/fermé sur clic droit, selon son état actuel
            if item.open_state:
                self.specific_verb = 'close'
            else:
                self.specific_verb = 'open'
        elif hasattr(item, 'take'):
            # un autre objet pouvant être pris sera pris
            self.specific_verb = 'take'
        else:
            # sinon, on se ramènera au verbe par défaut pour les clics gauches
            self.specific_verb = None

    def update(self):
        self.update_visibility()
        # duck-type conteneurs
        if hasattr(self.item, 'open_state'):
            self.update_open_state()
        self.update_parent()

    def update_open_state(self):
        if self.item.open_state:
            self.change_image(self.item.area_open_image_path)
        else:
            # area_image_path est l'image de l'objet fermée dans la zone
            self.change_image(self.item.area_image_path)

    def update_parent(self):
        if self.item.parent.tag == 'inventory':
            self.destroy()  # no need for an area view anymore


class InventoryItemClickable(ItemClickable):
    """
    Sprite associé à un objet, apparaissant dans l'inventaire

    Attributs hérités :
        image         -- image de l'objet dans l'inventaire
        rect
        visible
        dirty
        mask
        subject

    Attributs propres :
        item          -- objet observé (sujet)
        specific_verb -- verbe appelé automatiquement sur un clic droit

    """
    def __init__(self, item):
        ItemClickable.__init__(self, item, visible=1)  # toujours visible dans l'inventaire

        if hasattr(item, 'open'):
            # un conteneur duck-typed est par défaut ouvert/fermé sur clic droit, selon son état actuel
            if item.open_state:
                self.specific_verb = 'close'
            else:
                self.specific_verb = 'open'
        else:
            # sinon, on observe l'objet (étant dans l'inventaire, pas de déplacement ni de re-prise de l'objet envisagée)
            self.specific_verb = 'look_at'

    def update(self):
        # duck-type conteneurs
        if hasattr(self.item, 'open_state'):
            if self.item.open_state:
                self.change_image(self.item.inventory_open_image_path)
            else:
                # area_image_path est l'image de l'objet fermée dans la zone
                self.change_image(self.item.inventory_image_path)


class GateClickable(Clickable):
    """Vue d'une porte"""
    def __init__(self, gate, visible=1):
        """Initialise la porte avec l'area passée en argument"""
        Clickable.__init__(self, gate.image_path, gate.view_position, visible)
        self.bind_subject(gate)

    def on_click(self, adventurestate, button):
        gate = self.subject_list[0]
        if button == 1:
            adventurestate.enter_area(gate.target_area_name)
            del adventurestate.verb
            del adventurestate.complement
        else:
            # clic droit : observer vers où mène cette porte (une interdiction de regarder peut être mise en place)
            adventurestate.display_description("Cette porte semble mener à %s." % adventurestate.areas[self.target_area_name].fullname)
            # peut-être faire passer directement une référence vers l'area ciblée...


class InventoryView(ElementView):
    """Vue pour l'inventaire

    Attributs hérités :
        image
        rect
        visible
        dirty
        mask
        subject

    Attributs propres :
        item_group    -- groupe de srites pour les objets de l'inventaire

    Propriété :
        inventory     -- inventaire observé

    """
    def __init__(self, inventory, visible=1):
        ElementView.__init__(self, inventory.image_path, inventory.view_position, visible)
        self.bind_subject(inventory)
        # maybe we should also bind the items IN the inventory,
        # for now every item takes care of its own image

        self.item_group = pygame.sprite.RenderUpdates()

    def update(self):
        self.update_visibility()
        self.update_position()
        self.update_content()  # add content aspect

    def update_content(self):
        print "Inventory view: update content"

        # destroy all sprites but the first, which is the inventory background
        for item_view in self.item_group:
            item_view.destroy()

        # (we could also remove them from the view to reuse the observer sprites later):
        # self.remove(self.get_sprites_from_layer(self.inventory_layer)[1:])

        # add the views for every item ion the inventory
        # TODO: arrow system for more than 4 items
        for index, item in enumerate(self.inventory.children):
            # dans cette version, on recrée la vue à chaque fois:
            item_view = InventoryItemClickable(item)
            item_view.rect.topleft = self.rect.topleft
            # print get_relative_position_for(index)
            item_view.rect.move_ip(*get_relative_position_for(index))
            # print "after: " + str(item.inventory_clickable.rect.topleft)
            self.item_group.add(item_view)
            print "added view of %s in item_group of inventory at %s, %s" % (item.codename, item_view.rect.x, item_view.rect.y)
            self.dirty = 1

    @property
    def inventory(self):
        return self.subject_list[0]

def get_relative_position_for(index):
    return (40 * index, 20)

class MenuButtonClickable(Clickable):
    """Vue d'un bouton (classe abstraite)"""
    def __init__(self, button, visible):
        """Initialise la vue du bouton passé en argument"""
        Clickable.__init__(self, button.image_path, button.relative_rect.topleft, visible)
        self.bind_subject(button)


class VerbButtonClickable(MenuButtonClickable):
    """Vue d'un bouton de verbe"""
    def __init__(self, button, visible=1):
        """Initialise la vue du bouton passé en argument"""
        MenuButtonClickable.__init__(self, button, visible)
        
    def on_click(self, adventurestate, button):
        # l'enfant situé le plus bas parmi les sujets est le modèle observé à l'origine, i.e. le bouton de verbe
        verb_button = self.subject_list[0]
        adventurestate.verb = verb_button.codename
        del adventurestate.complement


class AdventureMenuView(ElementView):
    """
    Menu contextuel s'affichant lorsque le joueur clique sur un element

    Attributs hérités :
        image
        rect
        visible
        dirty
        mask

    """
    def __init__(self, menu, visible=1):
        ElementView.__init__(self, menu.image_path, menu.view_position, visible)
        self.bind_subject(menu)


    # # may be generalized to other views containing other views: inventory, etc.
    # @property
    # def all_visible(self):
    #     """Visibility property of self plus all clickables under self"""
    #     return self.visible

    # @all_visible.setter
    # def all_visible(self, value):
    #     print 'using my visible setter'
    #     self.visible = value
    #     for button in self.buttons:
    #         button.visible = value


# BETA: switch between both methods to activate query mode

def _on_click_for_interactive_button(self, adventurestate):
    adventurestate.verb = self.codename
    del adventurestate.complement

def _on_click_for_query_interactive_button(self, adventurestate):
    adventurestate.verb = self.codename  # opt. ici mais pratique en mouse-over pour voir ce qu'on fait
    # direct link to item with a method 'get_by_name'? but this ensures the item is in the current area...
    # the item could also be linked to the parent menu, but one link is necessary in both cases
    item = adventurestate.area.get_item_by_name(adventurestate.complement)
    # that's some decoration
    if hasattr(item, adventurestate.verb):
        print "now calling query action %s for item %s" % (adventurestate.verb, item.fullname)
        if getattr(item, adventurestate.verb)(adventurestate):
            # if True is returned, the action has been completed
            # hide the dynamic menu again (includes action to default)
            print "hiding menu again"
            adventurestate.hide_menu()
    else:
        # si l'action est inconnue, c'est le message 'rien à faire' par défaut
        print "Hum, je ne peux pas " + adventurestate.verb + " l'objet " + item.fullname + ". (action inconnue)"
        del adventurestate.verb


# TODO: furnitures (éléments ayant une description mais appartenent purement au décor)
