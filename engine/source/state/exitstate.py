# -*- coding: utf-8 -*-

from gamestate import GameState

class ExitState(GameState):
    """Gamestate temporaire de sortie

    Attributs :
        gc      --  game context supervisant ce game state

    """

    def __init__(self, gc):
        """Initialisation des ressources et des modèles qui ne doivent être initialisés qu'une seule fois"""
        GameState.__init__(self, gc)

    def on_enter(self):
        pass

    def on_exit(self):
    	pass

    def handle_input(self):
        pass

    def render(self, screen):
        pass