# -*- coding: utf-8 -*-

import pygame

from gamestate import GameState
from ..adventure.models import Area, InteractiveMenu, Inventory, Item
from ..adventure import models
from ..exception.exception import OverwriteError, GetError

from ..helper.load import load_descriptions


class AdventureState(GameState):
    """Gamestate du mode principal de jeu

    Attributs :
        gc          --  game context supervisant ce game state
        view        --  conteneur des couches de vue (propre à chaque state)
        areas       --  ensemble des zones en jeu
        area        --  zone en cours de visite
        inventory   --  inventaire de l'avatar
        menu        --  menu interactif
        default_verb-- verbe par défaut (comme 'move' ou 'look_at')
        verb     --  verbe en cours de sélection dans le cas d'un menu à la Monkey Island voire à la Goonies
        complement --  1° complément de l'action utiliser un hash ou une liste piur la version finale)
        description_hash -- hash des descriptions (pour l'instant, n'est pas initialisé automatiquement)

    """

    def __init__(self, gc):
        """Initialisation des ressources et des modèles qui ne doivent être initialisés qu'une seule fois"""
        GameState.__init__(self, gc)
        self.areas = {}
        self.area = None
        self.inventory = Inventory()
        self.description_hash = {}
        # self.default_verb = 'look_at'  # inside set_query_mode()
        self._verb = None  # may not be needed
        self._complement = None
        self.set_query_mode(False)  # ok??

    def on_enter(self):

        self.cursor = None
        self.label = None
        self.mouse_command = {'left': [0, None], 'right': [0, None]}
        del self.verb  # ok this way?
        del self.complement

    def on_exit(self):
        pass

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.gc.set_incoming_state('exit')  # changement toléré exceptionnellement dans le handle...
                # en fait, on pourrait fusionner handle et update
                # mais la séparation évite d'après plusieurs events -> actions en même temps
                # pour peu que plusieurs events attendent dans la file

            # détection clics souris : entrée -> assigner le sprite cliqué (situé le plus haut)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # we should add a security to check that view is not void, especially when
                # only clickable are considered (otherwise bg has oods to be clicked on)
                if event.button == 1:
                    if self.mouse_command['left'][0] == 0:  #  if mouse button has just been set down
                        self.mouse_command['left'][:] = [1, event.pos]  # 1 for 'new click' (may be called several times due to looping)
                elif event.button == 2:
                    if self.mouse_command['right'][0] == 0:  #  if mouse button has just been set down
                        self.mouse_command['right'][:] = [1, event.pos]  # 1 for 'new click'

            # détection clics souris : sortie
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_command['left'][0] = 0  # means no clicks, you can keep old mouse position
                elif event.button == 2:
                    self.mouse_command['right'][0] = 0

    def update(self):
        # print("update adventure state")
        # print("self mouse command is : " + str(self.mouse_command))

        # on regarde si on a cliqué (clic gauche) sur un élément du jeu
        # print("valeur mouse_cmd left: {0}, {1}".format(self.mouse_command['left'][0], 2))
        if self.mouse_command['left'][0] == 1:  # only consider new clicks for action clicks
            print "click detected on " + str(self.mouse_command['left'][1])

            self.mouse_command['left'][0] = 2  # say it's now in 'hold mode'
            ## TODO : customize with mask collision

            if self.view.get_sprites_at(self.mouse_command['left'][1]):
                # attention, le décor n'est plus un sprite donc on vérifie que le clic ne tombe pas dessus
                elt = self.view.get_sprites_at(self.mouse_command['left'][1])[-1]  # [-1] for last position, ie the sprite at the very top

                # sinon, il faut vérifier que self.view.get_sprites_at(...) n'est pas vide

                print ("elt : %s, rect : %s" % (str(elt), str(elt.rect)))

                # on teste manuellement si on_click existe (duck-typing)
                # mais on devrait peut-être dissocier les vues cliquables et non-cliquables
                # dans self.view, et uniquement détecter les clics sur les premières
                if hasattr(elt, 'on_click'):
                    print ("the clicked elt has an on_click()")
                    elt.on_click(self)
                else:
                    print ("elt detected has no on_click")
                    del self.verb
                    del self.complement
            else:
                # on a cliqué dans le décor
                print("click detected on the background")
                del self.verb
                del self.complement

    def render(self, screen):
        # tempo : on refait tout pour être à jour !
        # self.view.reset()
        # self.view.loadArea(self.area)
        # self.set_menu(self.menu)
        # self.view.displayText(self.action, (20, 400, 400, 30), (255, 255, 255), (0, 0, 0))
        self.view.draw(screen)  # for now, bg and all
        ## only draws when necessary

    ##
    ## peut-être décorer toute la suite pour le caser dans le init
    ## ainsi, même si le développeur construit son jeu, rien ne se passe
    ## avant le run !

    def add_area(self, area):
        """
        Attache la zone area à l'AdventureState sous l'entrée codename dans le dictionnaire

        Le nom de code permet d'avoir des noms simplifiés et toujours distincts.
        Si le nom de code proposé a déjà été entré, la méthode lance une exception.
        Exemple : "Laboratoire" -> "labo", une autre salle nommée "Laboratoire" -> "labo2"

        """
        if area.codename in self.areas:
            raise OverwriteError(area.codename, "Could not overwrite preexisting area codename: " + area.codename)
        self.areas[area.codename] = area
        print "added area"

    def remove_area(self, codename):
        if codename not in self.areas:
            raise GetError(codename, "Could not remove area because of unexisting codename: " + codename)
        del self.areas[codename]  # mutates the dictionary
        print "removed area"

    def enter_area(self, area_codename):
        # area on_exit ?
        print "entering area..." + area_codename
        self.area = self.areas[area_codename]
        self.view.loadArea(self.area)
        screen = pygame.display.get_surface()
        screen.blit(self.area.image, (0, 0))  # pas très conventionnel mais bon
        # area on_enter ?

    # un peu pour le debug, un peu pour "on_exit"
    def leave_area(self):
        self.area = None
        self.view.empty()

    # gère modèles et vues, évite les rafraîchissements inutiles
    def remove_item_from_area(self, item, area):
        """Retire un item d'une zone donnée"""
        self.area.remove_item(item)
        self.view.remove_item(item)

    def remove_item_by_name_from_area(self, item_name, area):
        """Retire un item d'une zone donnée"""
        self.area.remove_item_by_name(item_name)
        self.view.remove_item_by_name(item_name)

    def remove_item(self, item):
        """Retire un item de la zone active"""
        self.remove_item_from_area(item, self.area)

    def remove_item_by_name(self, item_name):
        """Retire un item de la zone active"""
        self.remove_item_by_name_from_area(item_name, self.area)

    def set_menu(self, menu):
        self.menu = menu
        self.view.fillMenuLayer(menu)

    def set_default_verb(self, verb):
        self.default_verb = verb

    @property
    def verb(self):
        """Verbe de l'action en cours"""
        return self._verb

    @verb.setter
    def verb(self, value):
        self._verb = value
        self.refresh_action_label()

    @verb.deleter
    def verb(self):
        self._verb = self.default_verb
        # pour l'instant, on suppose que le complément reste
        self.refresh_action_label()

    @property
    def complement(self):
        """Verbe de l'action en cours"""
        return self._complement

    @complement.setter
    def complement(self, value):
        self._complement = value
        self.refresh_action_label()

    @complement.deleter
    def complement(self):
        self._complement = None
        # on suppose que le verbe reste
        self.refresh_action_label()

    def refresh_action_label(self):
        """
        Rafraîchit l'indication de l'action en cours

        Plutôt dans l'adventure state que la vue car supposé
        'haut niveau', dépend du jeu et peut être overridée (avec la bonne doc)

        """
        # pour l'instant, la préposition par défaut est 'avec'
        if self.complement is None:
            action_str = self.verb
        else:
            action_str = " %s %s (avec) ..." % (self.verb, self.complement)
        self.view.displayText(action_str, None, (255, 255, 255), (0, 0, 0))

    def display_menu_for(self, complement_object):
        self.verb = '???'  # action still undefined
        self.complement = complement_object.codename  # but complement is for a dynamic menu
        self.view.display_menu()

    def hide_menu(self):
        """Masque le menu dynamique ET rétablit l'action par défaut"""
        del self.verb
        del self.complement
        self.view.hide_menu()

    def set_descriptions_from_file(self, file_path):
        self.description_hash = load_descriptions(file_path)

    def set_query_mode(self, query_mode=True):
        """Active le mode 'query' pour tous les modèles
        !! modification structurelle (classes) et non seulement pour les instances de state adventure
        """
        if query_mode:
            self.default_verb = 'query'
            Item.query = lambda self, adventurestate: adventurestate.display_menu_for(self)
            models.InteractiveButton.on_click = models._on_click_for_query_interactive_button
        else:
            self.default_verb = 'look_at'
            if hasattr(Item, 'query'):
                del Item.query
            models.InteractiveButton.on_click = models._on_click_for_interactive_button

    # peut-être ajouter .name pour accéder au nom plus facilement (et faire des tests)
    def __str__(self):
        return "Adventure State"
