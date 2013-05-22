# -*- coding: utf-8 -*-

from gamestate import GameState

class MenuState(GameState):
    """Gamestate du menu de pause"""

    def __init__(self, gc):
        GameState.__init__(self, gc)

    def on_enter(self):
        pass

    def on_exit(self):
    	pass

    def handle_input(self):
        pass

    def render(self):
        pass
