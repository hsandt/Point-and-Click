# -*- coding: utf-8 -*-

import pygame

from gamestate import GameState
from ..adventure.models import Area
from ..exception.exception import OverwriteError, GetError


class AdventureState(GameState):
    """Gamestate du mode principal de jeu

    Attributs :
        gc      --  game context supervisant ce game state
        view    --  conteneur des couches de vue
        area    --  aire visitée

    """

    def __init__(self, gc):
        """Initialisation des ressources et des modèles qui ne doivent être initialisés qu'une seule fois"""
        GameState.__init__(self, gc)
        self.areas = {}
        self.area = None

    def on_enter(self):

        self.inventory = None
        self.cursor = None
        self.label = None

    def on_exit(self):
        pass

    def handle_input(self):
        pass

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.gc.set_incoming_state('exit')

    def render(self, screen):
        self.view.draw(screen)

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

    # peut-être ajouter .name pour accéder au nom plus facilement (et faire des tests)
    def __str__(self):
        return "Adventure State"
