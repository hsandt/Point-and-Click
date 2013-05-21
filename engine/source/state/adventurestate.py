# -*- coding: utf-8 -*-

from gamestate import GameState
from view import LayeredView

class AdventureState(GameState):
    """Gamestate du menu de pause

    Attributs:

    view    --  conteneur des couches de vue
    area    --  aire visitée


    """

    def __init__(self):
        """Initialisation des ressources et des modèles qui ne doivent être initialisés qu'une seule fois"""
        GameState.__init__(self)

    def on_enter(self):
        self.view = LayeredView()
        # area = Area()

    def on_exit(self):
    	pass

    def handle_input(self):
        pass

    def render(self):
        pass
