# -*- coding: utf-8 -*-

import pygame
from menustate import MenuState
from adventurestate import AdventureState
from ..exception.exception import InputError

class PaCGame(object):
    """
    Jeu "point and click"
    A instancier pour démarrer le jeu
    Gère la boucle event-update-render centrée sur le Game Context

    Attributs:
        screen      --      pygame.Surface représentant l'écran de jeu
    
    """

    def __init__(self, window_size = (600, 400), FPS = 60):
        """Initialisation du jeu : moteur, fenêtre et game states"""

        # initialisation de pygame et de la fenêtre de jeu
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        self.FPS = FPS

        # création du game context (inclut la création des game states)
        self.context = GameContext()

    def run(self):
        """Lance le jeu"""
        clock = pygame.time.Clock()
        while 1:
            self.context.handle_input()
            self.context.update()
            self.context.render(screen)

            if self.context.incoming_state_name == 0:
                # signal de sortie détecté
                return

                # sortie du jeu
                if next_state == "exit":
                    return
                # autre changement de state
                context.change_state(context.next_state)

            clock.tick(self.FPS)


class GameContext(object):
    """
    Contexte du state pattern appliqué aux gamestates
    Remarque : si d'autres states, ne pas hésiter utiliser des héritages ou des décorateurs

    Attributs:
    state       --      état actuel
    next_state  --      prochain state à venir, affecté dès la fin de la boucle (None pour garder le même state)

    """

    def __init__(self):
        """Initialise les gamestates et lance le state initial"""

        # on stocke les states en mémoire en leur associant réciproquement le game context 'self'
        self.states = {
            'menu': MenuState(self),
            'adventure': AdventureState(self)
        }

        self.state = None
        self.incoming_state_name = None
        
    def enter_state(self, state_name):
        """Change le gamestate actuel en appliquant les pre/post-conditions si applicables"""
        
        # pre-condition (sortie du state précédent)
        if self.state is not None:
            self.state.on_exit()

        # vérification du state name proposé
        if state_name not in self.states:
            raise InputError(state_name, "Entrée vers un state name qui n'est pas dans la liste")
        
        # changement de state
        self.state = self.states[state_name]

        # post-condition (entrée dans le state suivant)
        self.state.on_enter()

    def enter_incoming_state(self):
        """helper permettant d'entrer dans le state suivant, prévu au cours d'un update"""
        
        # state_name particulier ne correspondant à aucun state : sortie du jeu
        if next_state == "exit":
            return 0 # signal de sortie

        # sinon, vérifier que state_name est bien dans la liste
        if self.incoming_state_name not in self.states:
            raise InputError(self.incoming_state_name, "Entrée vers un incoming state name qui n'est ni 'exit' ni dans la liste")
        
        # changement de state approprié
        self.enter_state(self.incoming_state)
        return 1 # pas de sortie

    def handle_input(self):
        self.state.handle_input()

    def update(self):
        self.state.update()

    def render(self):
        self.state.render()
