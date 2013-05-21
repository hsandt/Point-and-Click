# -*- coding: utf-8 -*-

from gamestate import GameState
from menustate import MenuState
from adventurestate import AdventureState

class GameContext(object):
    """
    Contexte du state pattern appliqué aux gamestates
    Remarque : si d'autres states, ne pas hésiter utiliser des héritages oudes décorateurs

    Keywords:
    state   --      état actuel
    """

    def __init__(self, initial_state_name = "menu"):
        # deux attributs menustate et adventurestate
        self.states = {
            'menu': MenuState()
            'adventure': AdventureState()
        }
        if initial_state_name in self.states:
            self.state = self.states[initial_state_name]
            self.state.on_enter()
        else:
            raise InputError
        

    def change_state(self, gamestate):
        pass

    def handle_input(self):
        pass

    def update(self):
        pass

    def render(self):
        pass
