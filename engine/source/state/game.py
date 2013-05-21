# -*- coding: utf-8 -*-

from menustate import MenuState
from adventurestate import AdventureState
from exception.exception import InputException

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

        # création du game context (inclut la création des game states)
        gc = GameContext()
        self.next_state_name = None

    def run(self):
        """Lance le jeu"""
        clock = pygame.time.Clock()
        while 1:
            gc.handle_input()
            gc.update()
            gc.render(screen)

            if gc.next_state_name is not None:

                # sortie du jeu
                if next_state == "exit":
                    return
                # changement de state normal
                gc.change_state(next_state)

            clock.tick(FPS)


class GameContext(object):
    """
    Contexte du state pattern appliqué aux gamestates
    Remarque : si d'autres states, ne pas hésiter utiliser des héritages ou des décorateurs

    Attributs:
    state       --      état actuel
    next_state  --      prochain state à venir, affecté dès la fin de la boucle (None pour garder le même state)

    """

    def __init__(self, initial_state_name = "menu"):
        """Initialise les gamestates et lance le state initial"""

        # on stocke les states en mémoire
        self.states = {
            'menu': MenuState(self),
            'adventure': AdventureState(self)
        }

        # on lance tout de suite le premier state
        if init_state_name in self.states:
            self.state = self.states[init_state_name]
            self.state.on_enter()
        else:
            raise InputException
        
    def change_state(self, state_name):
        """Change le gamestate actuel en appliquant les pre/post-conditions"""
        self.state.on_exit()
        self.state = self.states[initial_state_name]
        self.state.on_enter()

    def handle_input(self):
        self.state.handle_input()

    def update(self):
        self.state.update()

    def render(self):
        self.state.render()
