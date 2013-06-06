# -*-coding:Latin-1 -*
import pygame
from pygame import sprite
from ..helper.load import load_image
from ..exception.exception import GetError, AbstractMethodError


class Area(sprite.Sprite):
    """
    Zone de jeu.
    Elle possède son propre décor de fond et contient des élements.

    Attributs :
        codename         --  chaîne servant d'identifiant (minuscules, sans espace)
        fullname         --  nom descriptif de la zone ; par défaut, égal au codename
        image            --  image du décor de fond
        clickable_group  --  groupe des éléments cliquables contenus

    """

    def __init__(self, codename, fullname, image_path):
        """
        """
        sprite.Sprite.__init__(self)
        set_names(self, codename, fullname)

        self.image = load_image(image_path)
        print image_path
        self.rect = (0, 0, 800, 600)  # à étudier...

        self.clickable_group = pygame.sprite.Group()

    def add(self, element):
        self.clickable_group.add(element)
        print 'element added ' + element.codename

    def add_acitem(self, acitem, position):
        acitem.rect.topleft = position
        self.clickable_group.add(acitem)
        print 'item ' + acitem.fullname + ' added to area ' + str(self)

    def get_element(self, codename):
        """get element by name (should it be precised in the method name?)"""
        for element in self.clickable_group.sprites():
            if element.codename == codename:
                return element
        raise GetError(codename, "Element codename was wrong.")

    def remove_item(self, element):
        if self.clickable_group.has(element):
            self.clickable_group.remove(element)
            print 'element removed : ' + element.codename
        else:
            print("La salle ne contient pas " + element.codename)

    def remove_item_by_name(self, element_name):
        try:
            element = self.get_element(element_name)
        except:
            print("La salle ne contient pas " + element_name)
        else:
            self.clickable_group.remove(element)
            print 'element removed : ' + element.codename

    def add_gate(self, gate):
        self.clickable_group.add(gate)

    def __str__(self):
        # return self.fullname
        room_str = "Dans " + self.fullname + " il y a :"
        room_str += room_str.join([("-" + str(element) + "\n") for element in self.clickable_group.sprites()])
        return room_str


class Clickable(pygame.sprite.Sprite):
    """
    Elément cliquable : sprite disposant d'un comportement face au clic

    Attributs :
        Dérivés :
            image
            rect
        Nouveaux :
            codename    -- identifiant
            fullname    -- nom descriptif
            mask        -- masque pour la détection de clics

    """

    def __init__(self, codename, fullname, image_path, position, visibility=True):
        sprite.Sprite.__init__(self)
        set_names(self, codename, fullname)
        self.image = load_image(image_path)
        self.rect = pygame.Rect(position, self.image.get_size())
        print "%s has rect %s" % (self.fullname, str(self.rect))
        self.mask = pygame.mask.from_surface(self.image)  # use it!
        self.visibility = visibility  # unused, should affect detection

    def on_click(self, adventurestate):
        # opération sur adventurestate déclenchée sur un clic gauche :
        # déléguée à l'instance d'une classe dérivée
        raise AbstractMethodError(self.__class__.__name__, "on_click")

    def change_image(self, image_path):
        self.image = load_image(image_path)

    def __str__(self):
        return "Clickable : " + self.codename + " : " + self.fullname


class InteractiveButton(Clickable):
    """bouton constituant les menus contextuels"""
    def __init__(self, codename, fullname, image_path, position):
        # may use relative coords here (to the menu)
        Clickable.__init__(self, codename, fullname, image_path, position)
        # codename is fine for action_name
        # self.action_name = action_name

    def on_click(self, adventurestate):
        #Que se passe-t-il? Action à définir en fonction du bouton défini
        print("On me clique dessus, que dois-je faire?")
        adventurestate.set_action(self.codename)

    def notify_menu(self, menu):
        pass
        #prévient le menu dont le bouton fait parti qu'il a été cliqué

    def __str__(self):
        return "interactive button: " + self.fullname

        pass


class InteractiveMenu(sprite.Sprite):
    """
    Menu contextuel s'affichant lorsque le joueur clique sur un element

    Attributs :
        buttons     -- boutons utilisés (liste, hash ?)
        visibility  -- booléean indiquant la visibilité (comme pour un élément mais ce n'en est pas tout à fait un)
        image, pos... en fait, pourquoi ne pas dériver d'Element ?
        -> tout est élément cliquable avec comportement
        + introduire des patterns pour faire des jeux ressemblant à MI ou The Goonies !

    """
    def __init__(self, image_path, rect, visibility=False, *buttons):
        sprite.Sprite.__init__(self)
        buttons = list(buttons)
        # for i, button in enumerate(buttons):
        #     self.buttons[i] = button
        # self.buttons = enumerate(buttons)
        self.buttons = buttons  # no enumerate for now
        self.image = load_image(image_path)
        self.rect = rect
        self.visibility = visibility

        # instead, use a link to adventure state
        def notify_adventure(self):
            #Prévient Adventure qu'un des bouttons du menu a été cliqué
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

# class Entity(Element):
#     """Element du jeu autre que les portes avec lesquels, le joueur peut interagir"""
#     def __init__(self, description, visibility = True):
#         Element.__init__()
#         self.description = description #petit texte descriptif de l'element
#         self.visibility = visibility

#     def examine(self):
#         """Affiche la description de l'objet"""
#         pass

#     def on_click(self):
#         #Que se passe-t-il lorsqu'on clique sur l'élément?
#         print("On me clique dessus, je ne sais pas quoi faire!!!")


# use decorated entities!
class Item(object):
    """
    Objet : représente un élément de jeu que le joueur peut prendre, examiner, utiliser

    Il est distinct de sa représentation (sprite) dans la salle et dans l'inventaire.
    Il n'a pas de position définie car c'est l'objet pur en tant que données / comportement

    Attributs :
        codename            -- identifiant
        fullname            -- nom descriptif
        description         -- description
        area_image          -- image utilisée dans la zone
        inventory_image     -- image utilisée dans l'inventaire
        area_clickable      -- clickable utilisé dans la zone (utile pour référencer!)
        inventory_clickable -- clickable utilisé dans l'inventaire

    """
    def __init__(self, codename, fullname, adventurestate, area_image_path, inventory_image_path):
        ## TODO : put resource loading into the adventure state init by 'decorating' it?
        ## this would be done in Area.add_item() method
        set_names(self, codename, fullname)
        self.description = adventurestate.description_hash[codename]
        self.area_image_path = area_image_path
        self.inventory_image_path = inventory_image_path
        self.area_clickable = AreaClickableItem(self, (0,0))
        self.inventory_clickable = InventoryClickableItem(self, (0, 0))

    def look_at(self, adventurestate):
        print self.description

    # pas de différence avec attempt_to_take pour l'instant
    def take(self, adventurestate):
        """Ajoute l'item à l'inventaire"""
        # if already in inventory, forbid
        adventurestate.inventory.add_item(self.inventory_clickable)
        adventurestate.remove_item_by_name(self.codename)

    def use(self, adventurestate):
        print 'using ' + self.fullname

    def __str__(self):
        return self.fullname


class AreaClickableItem(Clickable):  # ??
    """
    Attributs :
        item       -- référence à l'item (modèle)
    """
    def __init__(self, item, position, visibility=True):
        Clickable.__init__(self, item.codename, item.fullname, item.area_image_path, position, visibility)
        self.item = item

    # common for any clickable ? only real elements ?
    def on_click(self, adventurestate):
        # en mode MI 1&2 : action latente
        if hasattr(self.item, adventurestate.action):
            # si l'action est connue de la part de l'item
            print "item name: " + self.item.codename
            getattr(self.item, adventurestate.action)(adventurestate)
        else:
            # si l'action est inconnue, c'est le message 'rien à faire' par défaut
            print "Hum, je ne peux pas " + adventurestate.action + " l'objet " + self.item.fullname + ". (action inconnue)"
        adventurestate.set_action("look_at")


class InventoryClickableItem(Clickable):  # ??
    """
    Attributs :
        item       -- référence à l'item (modèle)
    """
    def __init__(self, item, visibility=True):
        Clickable.__init__(self, item.codename, item.fullname, item.area_image_path, (0, 0), visibility)
        self.item = item

    # common for any clickable ? only real elements ?
    def on_click(self, adventurestate):
        # en mode MI 1&2 : action latente
        if hasattr(self.item, adventurestate.action):
            # si l'action est connue de la part de l'item
            print "item name: " + self.item.codename
            getattr(self.item, adventurestate.action)(adventurestate)
        else:
            # si l'action est inconnue, c'est le message 'rien à faire' par défaut
            print "Hum, je ne peux pas " + adventurestate.action + " l'objet " + self.item.fullname + ". (action inconnue)"
        adventurestate.set_action("look_at")

## + les éléments du décor cliquables mais non obtensibles !

class Character(Clickable):
    """PNJ avec lesquels on peut 'discuter' et plus si affinité (à la discrétion du développeur)"""
    def __init__(self):
        Clickable.__init__(self)

    def talk(self):
        #affiche une boite de dialogue avec un texte (peut-être la descrition)
        print("Bonjour! Je suis un PNJ")


class Gate(Clickable):
    """
    Attributs :
        area          -- zone ciblée par la porte
        position      -- position du sprite
        visibility    -- visibilité
    """
    def __init__(self, area, codename, fullname, image_path, position, visibility=True):
        """Initialise la porte avec l'area passée en argument"""
        Clickable.__init__(self, codename, fullname, image_path, position, visibility)
        self.area = area

    def on_click(self, adventurestate):
        adventurestate.enter_area(self.area.codename)

    def __str__(self):
        return "Gate to " + str(self.area)


# ce n'est pas un groupe de sprites ! enfin si, mais ce sont les sprites "inventaire"
# qui sont utilisés (image et position différentes)
class Inventory(sprite.Group):
    """Inventaire du joueur"""
    def __init__(self):
        sprite.Group.__init__(self)

    ## DON'T USE PREDEFINED NAMES!!
    def add_item(self, item):
        self.add(item)  # group method!
        print("Le joueur prend " + item.fullname)

    def remove(self, item):
        if self.has(item):
            self.remove(item)
            print(item.fullname + " a été retiré de l'inventaire")
        else:
            print(item.fullname + " n'est pas dans l'inventaire")

    def clear(self):
        self.empty()
        print("L'inventaire a été vidé")

    def __str__(self):
        inv_str = "Dans l'inventaire, il y a :"
        inv_str += inv_str.join([("-" + element + "\n") for element in self.pygame.sprite.Group])
        return inv_str

#Souris gérée par Pygame
# class Cursor(pygame.sprite.Sprite):
#     """curseur de la souris"""
#     def __init__(self, position, state, image_path):
#         pygame.sprite.Sprite.__init__(self)
#         self.position = pygame.mouse.get_pos()
#         self.state = pygame.mouse.get_pressed()
#         self.image = load_image(image_path)


# helper pour fournir un nom complet si besoin
# est-ce ok d'appeler le 1° argument self ?
def set_names(self, codename, fullname):
    self.codename = codename
    if fullname is None:
        self.fullname = codename
    else:
        self.fullname = fullname


def get_area_clickable_from_item(item, position):
    return Clickable(item.codename, item.fullname, item.area_image_path, position)


# test unitaire
if __name__ == '__main__':

    # a room should
    room = Area("blue screen of death", "../test_resource/background.png")
    teapot = Clickable("teapot", "../test_resource/teapot.png", (15, 30), (60, 40))  # later an item
    room.add(teapot)
    print room
    # room.get_element('a teapot').take()
    room.remove(teapot)
    inventory = Inventory()
    inventory.add(teapot)
    print inventory
    inventory.remove(teapot)
