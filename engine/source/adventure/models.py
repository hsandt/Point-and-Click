# -*-coding:Latin-1 -*
import pygame
from pygame import sprite

class Area(object):
    """Zone : lieu contenant des Elements, et où le protagoniste peut se déplacer"""

    def __init__(self, name, image_path):
        """blablabla...
        >>> room = Area("blue screen of death", "../test_resource/background.png")
        >>> teapot = Element("teapot", "../test_resource/teapot.png", (15,30), (60,40))
        >>> room.add(teapot, "a teapot")
        >>> print room
        >>> room.get_element('a teapot').take()
        """
        self.name = name
        # pour l'instant, je laisse le développeur entrer le path complet...
        self.image = pygame.image.load(image_path)
        self.elements = ElementGroup()              # on commence avec un groupe d'Eléments vide

    def add(self, element, name):
        self.elements.add_element(element, name)

    # def get_element(self, name):
    #     """get element by name (should it be precised in the method name?)"""
    #     return self.elements.get_element(name)

    def remove(self):
        pass

    def __str__(self):
        room_str = "Dans " + self.name + " il y a :"
        room_str += room_str.join([("-" + element + "\n") for element in self.elements.dict])
        return room_str

class Element(sprite.Sprite):
    """Elément : Personnage ou Objet situé dans une Zone, avec lequel le protagoniste peut interagir"""

    def __init__(self, name, image_path, position, size):
        sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.image.load(image_path)
        self.rect = pygame.Rect((position, size))
        self.clickBox = pygame.Rect((position, size)) #zone cliquable, par défaut égale au rect précédent, pour l'instant ...

    # def take(self):
    #     print "taken " + self.name

    def on_click(self):
        #que se passe-t-il lorsqu'on clique sur l'objet?
        pass

# class ElementGroup(sprite.Group):
#     """
#     Groupe d'éléments : sprite group contenant tous les éléments d'une zone,
#     avec des propriétés supplémentaires
#     """

#     def __init__(self):
#         sprite.Group.__init__(self)
#         self.dict = {}

#     def add_element(self, element, name):
#         """Override en ajoutant la modification du dictionnaire"""
#         # petite différence : si deux éléments ont le même nom, le premier sera écrasé (à éviter ou à traiter)
#         self.dict[name] = element
#         self.add(element)
#         # ajouter des méthodes similaires à Group pour le supplanter
#         # ou bien charger tous elts du jeu dans un super dictionnaire pour tout

#     def get_element(self, name):
#         return self.dict[name]

class Entity(Element):
    """Elements du jeu autre que les portes avec lesquels, le joueur peut interagir"""
    def __init__(self, description, visibility):
        Element.__init__()
        self.description = description #petit texte descriptif de l'element
        self.visibility = True

    def examine(self):
        """Affiche la description de l'objet"""
        pass

    def on_click(self):
        #Que se passe-t-il lorsqu'on clique sur l'élément?
        pass


# test unitaire
if __name__ == '__main__':

    # a room should
    room = Area("blue screen of death", "../test_resource/background.png")
    teapot = Element("teapot", "../test_resource/teapot.png", (15,30), (60,40)) # later an item
    room.add_element(teapot, "a teapot")
    print room
    room.get_element('a teapot').take()
