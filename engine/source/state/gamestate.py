# -*- coding: utf-8 -*-

class GameState(object):
    """
    Gamestate abstrait

    Attributs:

    gc		--	game context supervisant ce game state
    """

    def __init__(self, gc):
        self.gc = gc

    def on_enter(self):
        pass

    def on_exit(self):
    	pass

    def handle_input(self):
        pass

    def render(self):
        pass
