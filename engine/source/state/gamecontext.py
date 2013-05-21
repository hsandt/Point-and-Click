# -*- coding: utf-8 -*-

from gamestate import GameState
from menustate import MenuState
from adventurestate import AdventureState
from exception.exception import InputException

class GameContext(object):
    """
    Contexte du state pattern appliqué aux gamestates
    Remarque : si d'autres states, ne pas hésiter utiliser des héritages ou des décorateurs

    Attributs:
    state   --      état actuel
    """

    def __init__(self, initial_state_name = "menu"):
        """Initialise les gamestates et lance le state initial"""
        self.states = {
            'menu': MenuState(),
            'adventure': AdventureState()
        }
        if initial_state_name in self.states:
            self.state = self.states[initial_state_name]
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
