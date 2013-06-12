# -*-coding:Latin-1 -*
import pygame
from pygame import sprite
from ..helper.load import load_image
from ..exception.exception import GetError, AbstractMethodError


class Area(object):
    """
    Zone de jeu.
    Elle possède son propre décor de fond et contient des élements.
    Le décor est le seul sprite qui ne soit pas dirty.

    Attributs :
        codename         --  chaîne servant d'identifiant (minuscules, sans espace)
        fullname         --  nom descriptif de la zone ; par défaut, égal au codename
        image            --  image du décor de fond
        item_group       --  groupe des items (modèles)
        # gate_group       --  groupe des portes (modèles)
        clickable_group  --  groupe des éléments cliquables contenus

    """

    def __init__(self, codename, fullname, image_path):
        """
        """
        # sprite.Sprite.__init__(self)
        set_names(self, codename, fullname)

        self.image = load_image(image_path)
        # risque de ne pas tracer le background partout la 1° fois !
        # chaotique !!
        print image_path

        self.item_group = []
        # self.gate_group = []
        self.clickable_group = pygame.sprite.Group() # deprecated

    def add(self, element):
        self.clickable_group.add(element)
        print 'element added ' + element.codename

    def add_item(self, item, position):
        item.area_clickable.rect.topleft = position
        self.item_group.append(item)
        print 'item ' + item.fullname + ' added to area ' + str(self)

    # deprecated
    def add_acitem(self, acitem, position):
        acitem.rect.topleft = position
        self.clickable_group.add(acitem)
        print 'item ' + acitem.fullname + ' added to area ' + str(self)

    def get_clickable(self, codename):
        """get element by name (should it be precised in the method name?)"""
        for element in self.clickable_group.sprites():
            if element.codename == codename:
                return element
        raise GetError(codename, "[Area] " + self.fullname)

    def get_item_by_name(self, codename):
        """get item by name"""
        for item in self.item_group:
            if item.codename == codename:
                return item
        raise GetError(codename, "[Area] " + self.fullname)

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

    # def add_gate(self, gate):
    #     self.gate_group.append(gate)

    def add_gate(self, gate):
        self.clickable_group.add(gate)

    def __str__(self):
        # return self.fullname
        room_str = "Dans " + self.fullname + " il y a :"
        room_str += room_str.join([("-" + str(element) + "\n") for element in self.clickable_group.sprites()])
        return room_str


class Clickable(sprite.DirtySprite):
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

    def __init__(self, codename, fullname, image_path, position, visible=1):
        sprite.DirtySprite.__init__(self)
        set_names(self, codename, fullname)
        self.image = load_image(image_path)
        self.rect = pygame.Rect(position, self.image.get_size())
        print "%s has rect %s" % (self.fullname, str(self.rect))
        self.mask = pygame.mask.from_surface(self.image)  # use it!
        self.visible = visible  # unused, should affect detection

    def on_click(self, adventurestate):
        # opération sur adventurestate déclenchée sur un clic gauche :
        # déléguée à l'instance d'une classe dérivée
        raise AbstractMethodError(self.__class__.__name__, "on_click")

    def change_image(self, image_path):
        self.image = load_image(image_path)
        self.dirty = 1
        self.rect.size = self.image.get_size()

    def __str__(self):
        return "Clickable : " + self.codename + " : " + self.fullname


class InteractiveButton(Clickable):
    """bouton constituant les menus non contextuels"""
    def __init__(self, codename, fullname, image_path, position):
        # may use relative coords here (to the menu)
        Clickable.__init__(self, codename, fullname, image_path, position)
        # codename is fine for action_name
        # self.action_name = action_name

    def notify_menu(self, menu):
        pass
        #prévient le menu dont le bouton fait parti qu'il a été cliqué

    def __str__(self):
        return "interactive button: " + self.fullname

        pass



class InteractiveMenu(sprite.DirtySprite):
    """
    Menu contextuel s'affichant lorsque le joueur clique sur un element

    Attributs :
        buttons     -- boutons utilisés (liste, hash ?)
        visible  -- booléean indiquant la visibilité (comme pour un élément mais ce n'en est pas tout à fait un)
        image, pos... en fait, pourquoi ne pas dériver d'Element ?
        -> tout est élément cliquable avec comportement
        + introduire des patterns pour faire des jeux ressemblant à MI ou The Goonies !

    """
    def __init__(self, image_path, rect, visible=0, relative_positioning=True, *buttons):
        sprite.DirtySprite.__init__(self)
        buttons = list(buttons)
        # for i, button in enumerate(buttons):
        #     self.buttons[i] = button
        # self.buttons = enumerate(buttons)

        self.image = load_image(image_path)
        self.rect = pygame.rect.Rect(rect)  # rect can be either a tuple or a Rect (copy constructor)
        


        if relative_positioning:  # on peut travailler en absolu si on veut
            for button in buttons:
                button.rect.move_ip(*self.rect.topleft)  # use relative positions for the buttons
        self.buttons = buttons  # no enumerate for now

        print 'calling set of visible'
        # must be called *after* the buttons have been attached
        self.all_visible = visible

    # instead, use a link to adventure state
    def notify_adventure(self):
        #Prévient Adventure qu'un des bouttons du menu a été cliqué
        pass

    # may be generalized to other views containing other views: inventory, etc.
    @property
    def all_visible(self):
        """Visibility property of self plus all clickables under self"""
        return self.visible

    @all_visible.setter
    def all_visible(self, value):
        print 'using my visible setter'
        self.visible = value
        for button in self.buttons:
            button.visible = value



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
#     def __init__(self, description, visible = True):
#         Element.__init__()
#         self.description = description #petit texte descriptif de l'element
#         self.visible = visible

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
        area_image_path          -- image path utilisée dans la zone
        inventory_image_path     -- image path utilisée dans l'inventaire
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
        self.area_clickable = AreaClickableItem(self, (0, 0))
        self.inventory_clickable = InventoryClickableItem(self, (0, 0))

    def look_at(self, adventurestate):
        print self.description
        # view
        adventurestate.display_text(self.description, (280, 300))

    # pas de différence avec attempt_to_take pour l'instant
    def take(self, adventurestate):
        """Ajoute l'item à l'inventaire"""
        # if already in inventory, forbid
        adventurestate.inventory.add_item(self.inventory_clickable)
        adventurestate.remove_item_by_name(self.codename)
        return True  # action is over

    def use(self, adventurestate):
        print "Cannot use that item."
        return True

    def __str__(self):
        return self.fullname


class Container(Item):
    """
    Conteneur : item pouvant être ouvert / fermé, et révélant son contenu lorsqu'il est ouvert

    Il peut être préhensible ou non.

    Attributs hérités:
        codename            -- identifiant
        fullname            -- nom descriptif
        description         -- description
        area_image          -- image utilisée dans la zone
        inventory_image     -- image utilisée dans l'inventaire
        area_clickable      -- clickable utilisé dans la zone (utile pour référencer!)
        inventory_clickable -- clickable utilisé dans l'inventaire

    Attributs propres:
        open_state          -- booléen indiquant si le conteneur est ouvert (True) ou fermé (False)
        key_name            -- codename de la clé pouvant ouvrir le conteneur, ou None s'il n'y a pas besoin de clé
        content             -- contenu sous forme de liste
        open_area_image_path-- image path (ou peut-être image, à voir)

    """
    def __init__(self, codename, fullname, adventurestate, area_image_path, inventory_image_path, open_area_image_path, open_state=False, key_name=None, content=[]):
        Item.__init__(self, codename, fullname, adventurestate, area_image_path, inventory_image_path)
        self.open_area_image_path = open_area_image_path
        self.open_state = open_state
        self.key_name = key_name
        self.content = content

    def open(self, adventurestate):
        print 'trying to open container %s with bare hands' % self.fullname
        if self.open_state:
            print("%s est déjà ouvert." % self.fullname)
        else:
            if self.key_name is None:
                self.open_indeed(adventurestate)
            else:
                print("Une clé est nécessaire pour ouvrir %s." % self.fullname)
        return True

    def use(self, adventurestate):
        """
        Essaie d'ouvrir le conteneur à l'aide d'une clé. open est invoqué automatiquement.

        Plus tard, on utilisera peut-être l'attribut 'locked' et on différenciera les clés des autres objets.
        """
        # automatiser la détection de complément !
        if adventurestate.complement is None:
            print("Vous ne pouvez pas utiliser %s ainsi !" % self.fullname)
        else:
            tool_name = adventurestate.complement
            if tool_name == self.key_name:
                if self.open_state:
                    print("%s est déjà ouvert." % self.fullname)
                else:
                    self.open_indeed(adventurestate)
            else:
                print("L'objet %s ne peut être utilisé sur %s" % (tool_name, self.fullname))
        return True

    def open_indeed(self, adventurestate):
        """Ouvre le coffre à coup sûr, ne doit être appelé directement !"""
        self.open_state = True
        # should be modify view from here?
        self.area_clickable.change_image(self.open_area_image_path)
        adventurestate.view.load_content(self)
        print("%s has been opened." % self.fullname)


class AreaClickableItem(Clickable):  # ??
    """
    Attributs :
        item       -- référence à l'item (modèle)
    """
    def __init__(self, item, position, visible=1):
        Clickable.__init__(self, item.codename, item.fullname, item.area_image_path, position, visible)
        self.item = item

    # common for any clickable ? only real elements ?
    def on_click(self, adventurestate):
        # en mode MI 1&2 : action latente
        if hasattr(self.item, adventurestate.verb):
            # si l'action est connue de la part de l'item
            print "item name: " + self.item.codename
            if getattr(self.item, adventurestate.verb)(adventurestate):
                # if True is returned, the action has been completed
                del adventurestate.verb
                del adventurestate.complement
        else:
            # si l'action est inconnue, c'est le message 'rien à faire' par défaut
            print "Hum, je ne peux pas " + adventurestate.verb + " l'objet " + self.item.fullname + ". (action inconnue)"
            del adventurestate.verb


class InventoryClickableItem(Clickable):  # ??
    """
    Attributs :
        item       -- référence à l'item (modèle)
    """
    def __init__(self, item, visible=1):
        Clickable.__init__(self, item.codename, item.fullname, item.area_image_path, (0, 0), visible)
        self.item = item

    # common for any clickable ? only real elements ?
    def on_click(self, adventurestate):
        # en mode MI 1&2 : action latente
        if hasattr(self.item, adventurestate.verb):
            # si l'action est connue de la part de l'item
            print "item name: " + self.item.codename
            if getattr(self.item, adventurestate.verb)(adventurestate):
                del adventurestate.verb
        else:
            # si l'action est inconnue, c'est le message 'rien à faire' par défaut
            print "Hum, je ne peux pas " + adventurestate.verb + " l'objet " + self.item.fullname + ". (action inconnue)"
            del adventurestate.verb

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
        visible    -- visibilité
    """
    def __init__(self, area, codename, fullname, image_path, position, visible=1):
        """Initialise la porte avec l'area passée en argument"""
        Clickable.__init__(self, codename, fullname, image_path, position, visible)
        self.area = area

    def on_click(self, adventurestate):
        adventurestate.enter_area(self.area.codename)
        del adventurestate.verb

    def __str__(self):
        return "Gate to " + str(self.area)


# ce n'est pas un groupe de sprites ! enfin si, mais ce sont les sprites "inventaire"
# qui sont utilisés (image et position différentes)
class Inventory(object):
    """Inventaire du joueur
    Attributs :
        item_list : liste des items
        bg_image : background de l'inventaire

    """
    def __init__(self, path=None):
        
        self.item_list = []
        if path is not None:
            self.bg_image = load_image(path)
        else:
            self.bg_image = None #Ou trouver une image par défaut
        


    def add_item(self, item):
        self.item_list.append(item)
        print("Le joueur prend " + item.fullname)

    def remove(self, item):
        if item in self.item_list:
            self.item_list.remove(item)
            print(item.fullname + " a été retiré de l'inventaire")
        else:
            print(item.fullname + " n'est pas dans l'inventaire")

    def clear(self):
        del self.item_list[:]
        print("L'inventaire a été vidé")

    def __str__(self):
        inv_str = "Dans l'inventaire, il y a :"
        inv_str += inv_str.join([("-" + element + "\n") for element in self.pygame.sprite.Group])
        return inv_str

#Souris gérée par Pygame
# class Cursor(pygame.sprite.DirtySprite):
#     """curseur de la souris"""
#     def __init__(self, position, state, image_path):
#         pygame.sprite.DirtySprite.__init__(self)
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


def _on_click_for_interactive_button(self, adventurestate):
    #Que se passe-t-il? Action à définir en fonction du bouton défini
    print("On me clique dessus, que dois-je faire?")
    adventurestate.verb = self.codename
    del adventurestate.complement

def _on_click_for_query_interactive_button(self, adventurestate):
    adventurestate.verb = self.codename  # opt. ici mais pratique en mouse-over pour voir ce qu'on fait
    # direct link to item with a method 'get_by_name'? but this ensures the item is in the current area...
    # the item could also be linked to the parent menu, but one link is necessary in both cases
    item = adventurestate.area.get_item_by_name(adventurestate.complement)
    # that's some decoration
    if hasattr(item, adventurestate.verb):
        print "now calling query action %s for item %s" % (adventurestate.verb, item.fullname)
        if getattr(item, adventurestate.verb)(adventurestate):
            # if True is returned, the action has been completed
            # hide the dynamic menu again (includes action to default)
            print "hiding menu again"
            adventurestate.hide_menu()
    else:
        # si l'action est inconnue, c'est le message 'rien à faire' par défaut
        print "Hum, je ne peux pas " + adventurestate.verb + " l'objet " + item.fullname + ". (action inconnue)"
        del adventurestate.verb

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
