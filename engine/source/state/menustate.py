# -*- coding: utf-8 -*-

import pygame

from gamestate import GameState

class MenuState(GameState):
    """Gamestate du menu de pause

    Attributs :
        gc        game context supervisant ce game state
    
    """

    def __init__(self, gc):
        GameState.__init__(self, gc)

    def on_enter(self):
        pass

    def on_exit(self):
       pass

    def handle_input(self):
        pass

    def render(self, screen):
        pass

    def __str__(self):
        return "Menu State"
