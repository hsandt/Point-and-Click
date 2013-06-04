# -*- coding: utf-8 -*-

import pygame

from gamestate import GameState
from ..adventure.models import Area, InteractiveMenu, Inventory
from ..exception.exception import OverwriteError, GetError


class AdventureState(GameState):
    """Gamestate du mode principal de jeu

    Attributs :
        gc          --  game context supervisant ce game state
        view        --  conteneur des couches de vue
        areas       --  ensemble des zones en jeu
        area        --  zone en cours de visite
        inventory   --  inventaire de l'avatar
        menu        --  menu interactif
        #action     --  action en cours de sélection dans le cas d'un menu à la Monkey Island voire à la Goonies

    """

    def __init__(self, gc):
        """Initialisation des ressources et des modèles qui ne doivent être initialisés qu'une seule fois"""
        GameState.__init__(self, gc)
        self.areas = {}
        self.area = None
        self.inventory = Inventory()

    def on_enter(self):

        self.cursor = None
        self.label = None
        self.mouse_command = {'left': None, 'right': None}
        self.action = "look at"

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
                    self.mouse_command['left'] = self.view.get_sprites_at(event.pos)[-1]
                elif event.button == 2:
                    self.mouse_command['right'] = self.view.get_sprites_at(event.pos)[-1]

            # détection clics souris : sortie
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_command['left'] = None
                elif event.button == 2:
                    self.mouse_command['right'] = None

    def update(self):
        # print("update adventure state")
        # print("self mouse command is : " + str(self.mouse_command))
        
        # on regarde si on a cliqué (clic gauche) sur un élément du jeu
        elt = self.mouse_command['left']
        if elt is not None:
            # on teste manuellement si on_click existe (duck-typing)
            # mais on devrait peut-être dissocier les vues cliquables et non-cliquables
            # dans self.view, et uniquement détecter les clics sur les premières
            if hasattr(elt, 'on_click'):
                print ("the clicked elt has an on_click()")
                elt.on_click(self)

    def render(self, screen):
        # tempo : on refait tout pour être à jour !
        # self.view.reset()
        # self.view.loadArea(self.area)
        # self.set_menu(self.menu)
        # self.view.displayText(self.action, (20, 400, 400, 30), (255, 255, 255), (0, 0, 0))
        self.view.draw(screen)  # for now, bg and all

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
        # area on_enter ?

    # un peu pour le debug, un peu pour "on_exit"
    def leave_area(self):
        self.area = None
        self.view.empty()

    # gère modèles et vues, évite les rafraîchissements inutiles
    def remove_item_from_area(self, item, area):
        """Retire un item d'une zone donnée"""
        self.area.remove(item)
        self.view.remove_item(item)

    def remove_item(self, item):
        """Retire un item de la zone active"""
        self.remove_item_from_area(item, self.area)

    def set_menu(self, menu):
        self.menu = menu
        self.view.fillMenuLayer(menu)

    # developer-defined ? (propre au jeu et non au moteur ; il faut alors donner accès à adventure state (classe dérivée))
    # ou au moins donner une action 'script' à l'objet ??
    def set_action(self, action):
        self.action = action
        self.view.displayText(action, (20, 400, 400, 30), (255, 255, 255), (0, 0, 0))

    # peut-être ajouter .name pour accéder au nom plus facilement (et faire des tests)
    def __str__(self):
        return "Adventure State"
