class World(object):
    """
    Monde : il réunit les éléments présents dans le jeu.

    Ses méthodes consistent à altérer son contenu.

    Attributs :
        areas       --  dictionnaire des zones
        inventory   --  inventaire du joueur

    """

    def __init__(self, field_filename):
        self.areas = {}
        self.inventory = Inventory()

    def update(self, state):
        """
        Appelle la méthode 'update' pour tous ses éléments.

        Les sprites de self.field disposent d'un update() vide.

        """

        # for entity in self.__dict__.values():
        # deprecated, some entities are repeated!

        # map is above all updated in view, but model and view may merge later
        for entity in [self.field, self.bases, self.pms, self.balls, self.players]:
            entity.update(state)

    def __str__(self):
        world_str = "Monde - contenu :\n"
        world_str += "Zones :\n" + "".join([str(area) for area in self.areas.values()])
        world_str += "Inventaire :\n".str(self.inventory)