# -*-coding:Latin-1 -*
import pygame
from pygame import sprite
from ..helper.load import load_image
from ..exception.exception import GetError

class Area(sprite.Sprite):
    """
    Zone de jeu.
    Elle possède son propre décor de fond et contient des élements.

    Attributs :
        codename         --  chaîne servant d'identifiant (minuscules, sans espace)
        fullname         --  nom descriptif de la zone ; par défaut, égal au codename
        image            --  image du décor de fond
        element_group    --  groupe des éléments contenus

    """

    def __init__(self, codename, image_path, fullname=None):
        """
        """
        sprite.Sprite.__init__(self)
        self.codename = codename
        if fullname is None:
            self.fullname = codename
        else:
            self.fullname = fullname

        self.image = load_image(image_path)
        print image_path
        self.rect = (0, 0)

        self.element_group = pygame.sprite.Group()

    def add(self, element):
        self.element_group.add(element)
        print 'element added ' + element.codename

    def get_element(self, codename):
        """get element by name (should it be precised in the method name?)"""
        for element in self.element_group.sprites():
            if element.codename == codename:
                return element
        raise GetError(codename, "Element codename was wrong.")

    def remove(self, element):
        if self.element_group.has(element):
            self.element_group.remove(element)
            print 'element removed : ' + element.codename
        else:
            print("La salle ne contient pas " + element.name)


    def __str__(self):
        room_str = "Dans " + self.fullname + " il y a :"
        room_str += room_str.join([("-" + str(element) + "\n") for element in self.element_group.sprites()])
        return room_str

class Element(sprite.Sprite):
    """Elément : Personnage ou Objet situé dans une Zone, avec lequel le protagoniste peut interagir"""

    def __init__(self, codename, image_path, position, size, fullname = None):
        sprite.Sprite.__init__(self)
        self.codename = codename
        if fullname is None:
            self.fullname = codename
        else:
            self.fullname = fullname

        self.image = pygame.image.load(image_path)
        self.rect = pygame.Rect((position, size))
        self.clickBox = pygame.Rect((position, size)) #zone cliquable, par défaut égale au rect précédent, pour l'instant ...

    # def take(self):
    #     print "taken " + self.name

    def on_click(self):
        #que se passe-t-il lorsqu'on clique sur l'objet?-> déléguer la tâche à la classe fille correspondante
        print("On me clique dessus!")

    def __str__(self):
        return self.codename + " : " + self.fullname

class InteractiveButton(Element):
    """bouton constituant les menus contextuels"""
    def __init__(self, codename, image_path, position, size, fullname=None):
        Element.__init__(self, codename, image_path, position, size, fullname)
        # codename is fine for action_name
        # self.action_name = action_name

    def on_click(self):
        #Que se passe-t-il?
        print("On me clique dessus, que dois-je faire?")

    def notify_menu(self,menu):
        #prévient le menu dont le bouton fait parti qu'il a été cliqué
        pass
        
class InteractiveMenu:
    """Menu contextuel s'affichant lorsque le joueur clique"""
    def __init__(self, *buttons):

        pass
        # self.buttons = 
        
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
    """Element du jeu autre que les portes avec lesquels, le joueur peut interagir"""
    def __init__(self, description, visibility = True):
        Element.__init__()
        self.description = description #petit texte descriptif de l'element
        self.visibility = visibility

    def examine(self):
        """Affiche la description de l'objet"""
        pass

    def on_click(self):
        #Que se passe-t-il lorsqu'on clique sur l'élément?
        print("On me clique dessus, je ne sais pas quoi faire!!!")

class Item(Entity):
    """Objets que le joueur peut prendre, examiner, activer"""
    def __init__(self, description, visibility = True):
        Entity.__init__(self, description, visibility)

    def take(self, inventory, room):
        """Ajoute l'item à l'inventaire"""
        inventory.add(self)
        room.remove(self)

    def use(self):
        #Que se passe-t-il?
        pass

class Character(Entity):
    """PNJ avec lesquels on peut 'discuter' et plus si affinité (à la discrétion du développeur)"""
    def __init__(self):
        Entity.__init__(self)

    def talk(self):
        #affiche une boite de dialogue avec un texte (peut-être la descrition)
        pass
        

class Inventory(pygame.sprite.Group):
    """Inventaire du joueur"""
    def __init__(self):
        pygame.sprite.Group.__init__()
    
    def add(self, item):
        self.add(item)
        print("Le joueur prend " + item.fullname)

    def remove(self, item):
        if this.has(item):
            this.remove(item)
            print(item.fullname + " a été retiré de l'inventaire")
        else:
            print(item.fullname + " n'est pas dans l'inventaire")

    def clear(self):
        this.empty()
        print("L'inventaire a été vidé")

    def __str__(self):
        inv_str = "Dans l'inventaire, il y a :"
        inv_str += inv_str.join([("-" + element + "\n") for element in self.sprites])
        return room_str
        
        


# test unitaire
if __name__ == '__main__':

    # a room should
    room = Area("blue screen of death", "../test_resource/background.png")
    teapot = Element("teapot", "../test_resource/teapot.png", (15,30), (60,40)) # later an item
    room.add(teapot)
    print room
    # room.get_element('a teapot').take()
    room.remove(teapot)
    inventory = Inventory()
    inventory.add(teapot)
    print inventory
    inventory.remove(teapot)



