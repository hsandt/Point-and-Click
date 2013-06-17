# -*- coding: utf-8 -*-

from ..view.layeredview import LayeredView
from ..exception.exception import AbstractMethodError

class GameState(object):
    """
    Gamestate abstrait

    Attributs:
        gsm			game state manager supervisant ce game state
        view      vue en couches associée au game state
    
    """

    def __init__(self, gsm, view):
        self.gsm = gsm
        self.view = view

    def on_enter(self):
        pass

    def on_exit(self):
    	pass

    def handle_input(self):
        pass

    def update(self):
        raise AbstractMethodError(self.__class__.__name__, "update")

    def render(self):
        raise AbstractMethodError(self.__class__.__name__, "render")
