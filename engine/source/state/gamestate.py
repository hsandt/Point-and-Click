# -*- coding: utf-8 -*-

from ..view.layeredview import LayeredView
from ..exception.exception import AbstractMethodError

class GameState(object):
    """
    Gamestate abstrait

    Attributs:
        gc			game context supervisant ce game state
        view      vue en couches associée au game state
    
    """

    def __init__(self, gc):
        self.gc = gc
        self.view = LayeredView()

    def on_enter(self):
        pass

    def on_exit(self):
    	pass

    def handle_input(self):
        pass

    def update(self):
        raise AbstractMethodError(self)

    def render(self):
        raise AbstractMethodError(self)