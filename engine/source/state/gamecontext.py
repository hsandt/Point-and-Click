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
        self.menustate = MenuState()
        self.adventurestate = AdventureState()
        if initial_state_name == "menu":
            self.state = self.menustate
        elif initial_state_name = "adventure":
            self.state = self.adventurestate
        else:
            raise InputError
        self.state = initial_state_name

    def change_state(self, gamestate):
        pass

    def handle_input(self):
        pass

    def update(self):
        pass

    def render(self):
        pass
