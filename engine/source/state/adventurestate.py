# -*- coding: utf-8 -*-

from gamestate import GameState
from ..view.layeredview import LayeredView
from ..adventure.models import Area

class AdventureState(GameState):
    """Gamestate du menu de pause

    Attributs:
        gc      --  game context supervisant ce game state
        view    --  conteneur des couches de vue
        area    --  aire visitée

    """

    def __init__(self, gc):
        """Initialisation des ressources et des modèles qui ne doivent être initialisés qu'une seule fois"""
        GameState.__init__(self, gc)

    def on_enter(self):
        self.view = LayeredView()
        self.area = None # le développeur doit en créer une
        self.areas = {} 
        self.inventory = None
        self.cursor = None
        self.label = None

    def on_exit(self):
    	pass

    def handle_input(self):
        pass

    def render(self):
        pass

    def addArea(self, area, area_codename = None):
        """
        Attache la zone area à l'AdventureState sous l'entrée codename dans le dictionnaire

        Le nom de code permet d'avoir des noms simplifiés et toujours distincts.
        Exemple : "Laboratoire" -> "labo", une autre salle nommée "Laboratoire" -> "labo2"

        """
        
        # en cas d'absence de nom de code, on utilise le nom de la zone
        if area_codename is None:
            area_codename = area.name
        self.areas[area_codename]
