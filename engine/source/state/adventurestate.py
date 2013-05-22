# -*- coding: utf-8 -*-

from gamestate import GameState
from view.layeredview import LayeredView
from adventure.models import Area

class AdventureState(GameState):
    """Gamestate du menu de pause

    Attributs:

    view    --  conteneur des couches de vue
    area    --  aire visitée

    """

    def __init__(self, gc):
        """Initialisation des ressources et des modèles qui ne doivent être initialisés qu'une seule fois"""
        GameState.__init__(self, gc)

    def on_enter(self):
        self.view = LayeredView()
        self.area = None # le développeur doit en créer une

    def on_exit(self):
    	pass

    def handle_input(self):
        pass

    def render(self):
        pass

    def addArea(self):
        pass
