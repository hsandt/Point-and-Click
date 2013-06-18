# -*-coding:Latin-1 -*

import pygame
from pygame import sprite
from .subject import Subject
from ..exception.exception import GetError, AbstractMethodError


class Element(object):
    """
    Elément : zone, objet, personnage ou porte

    Il possède une description et réagit au verbe 'look_at'
    Il correspond à un élément quelconque sous root dans l'arborescence XML (à venir).

    Attributs :
        codename            -- identifiant
        fullname            -- nom descriptif (codename par défaut)
        description         -- description
        tag                 -- type d'élément ('area', 'item', 'inventory'...)
        _parent             -- parent dans l'arborescence des élements
        children            -- liste des enfants

        """

    def __init__(self, codename, fullname, adventurestate, tag=None, parent=None):
        set_names(self, codename, fullname)
        # TODO: pass description instead of adventurestate and use a factory to build items from files
        if tag == 'inventory':
            self.description = "your inventory"
        elif tag == 'menu':
            self.description = "menu"
        elif tag == 'button':
            self.description = "button"
        elif tag == 'verb':
            self.description = "verb subject"
        else:
            self.description = adventurestate.description_hash[codename]  # use description + factory instead
        self.tag = tag
        self._parent = None  # needed to have setter work
        self.parent = parent
        self.children = []

    def look_at(self, adventurestate):
        adventurestate.display_description(self.description)

    def acquire_element(self, element):
        # acquit l'élément comme enfant (réciproquement), quitte à le soustraire à un autre parent
        element.parent = self
        print "%s added to %s" % (str(element), str(self))

    def acquire_element_list(self, element_list):
        for element in element_list:
            self.acquire_element(element)
        print("Element list %s has been added to %s." % (str([element.codename for element in element_list])), str(self))

    def get_element_by_name(self, codename):
        print "children for %s: %s" % (self.codename, self.children)
        for element in self.children:
            if element.codename == codename:
                return element
        raise GetError(codename, str(self))

    def remove_element(self, element):
        if element in self.children:
            del element.parent
            print 'element %s removed from area %s' % (str(element), str(self))
        else:
            raise GetError(str(element), str(self))

    def move_element_to(self, element, new_parent):
        if element in self.children:
            remove_element(element)
            new_parent.add_element(element)
        else:
            raise GetError(str(element), str(self))

    def remove_all(self):
        for child in children:
            self.remove_element(child)
        print("%s has been emptied." % str(self))

    @property
    def parent(self):
        """Parent de l'élément, dont la modification affecte les associations bidirectionnelles"""
        return self._parent

    @parent.setter
    def parent(self, new_parent):
        if self._parent is not None:
            # if there was already a parent, it is a move, so remove the existing link first
            # warning: don't use .parent = None!, use ._parent = None (init) or the deleter (if already a parent)
            print "try to remove %s from %s" % (self.codename, new_parent.codename)
            self._parent.children.remove(self)
        self._parent = new_parent
        if new_parent is not None:
            new_parent.children.append(self)
            print "%s got child %s" % (new_parent.codename, self.codename)

    @parent.deleter
    def parent(self):
        if self._parent is not None:
            self._parent.children.remove(self)
            self._parent = None

    def __str__(self):
        return "<Element '%s'(%d child(ren))>" % (self.codename, len(children))


class ObservableElement(Element, Subject):
    """
    Element pouvant disposer d'une vue = observateur (classe abstraite)

    Attributs hérités :
        codename            -- identifiant
        fullname            -- nom descriptif (codename par défaut)
        description         -- description
        tag                 -- type d'élément ('area', 'item', 'inventory'...)
        _parent             -- parent dans l'arborescence des élements
        children            -- liste des enfants

        observer_list       -- liste des vues

    Attributs propres:
        _visible            -- booléen indiquant si l'élement est visible actuellement
        _view_position      -- position used in relative (to the model's parent) positioning of the view
        Besides, any ObservableElement must have a view_position attribute, whether fictive or real. (but every derived class implements its own so as to avoid conflict between properties and attributes)
    """
    def __init__(self, codename, fullname, adventurestate, tag, parent):
        Element.__init__(self, codename, fullname, adventurestate, tag, parent)
        Subject.__init__(self)

        self._visible = True
        self._view_position = (0, 0)

    def notify(self):
        print "%s will now notify its observers: %s." % (self.codename, self.observer_list)
        Subject.notify(self)

    @property
    def visible(self):
        """
        Décrit la visibilité du modèle. Elle est reliée à celle de la vue si présente.

        Attention, elle prend des valeurs booléennes au lieu de 0 ou 1.

        """
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value
        self.notify()

    @property
    def view_position(self):
        """Normally an access to self._view_position, it may be overriden to get a customized position."""
        return self._view_position

    @view_position.setter
    def view_position(self, position):
        self._view_position = position

    def __str__(self):
        return "<ObservableElement '%s'>" % self.codename

class Area(ObservableElement):
    """
    Zone de jeu : une des scènes sur laquelle se déroule l'aventure

    Elle possède son propre décor et contient des élements.

    Attributs hérités :
        codename
        fullname
        description
        children         --  liste des enfants : objets et portes

    Attributs propres :
        image_path       --  adresse de l'image du décor

    """

    def __init__(self, codename, fullname, adventurestate, image_path):
        ObservableElement.__init__(self, codename, fullname, adventurestate, tag="area", parent=None)
        self.children = []

        self.image_path = image_path

    def __str__(self):
        return "<Area '%s', (%d children element(s)>" % (self.codename, len(self.children))


class Item(ObservableElement):
    """
    Objet : élément réagissant par défaut aux verbes 'take' et 'use'

    Attributs hérités :
        codename
        fullname
        description
        parent
        children
        observer_list       -- liste des observateurs (vues associées à l'objet)

    Attributs propres :
        _visible             -- booléen indiquant si l'objet peut-être vu, et donc pris (si possible) (synchronisé avec la vue si présente)
        area_image_path     -- image path utilisée dans la zone
        area_position       -- position dans la zone
        inventory_image_path-- image path utilisée dans l'inventaire
        takeable            -- booléen valant True si l'objet peut être pris

    """
    def __init__(self, codename, fullname, adventurestate, parent, area_image_path=None, area_position=None, inventory_image_path=None):
        """
        On initialise le nom et les données brutes utilisées plus tard dans les vues.

        Comme certains objets ne servent que dans la zone ou que dans l'inventaire, un des deux types de caractéristiques 'area' et 'inventory' est parfois suffisant.

        """
        ObservableElement.__init__(self, codename, fullname, adventurestate, "item", parent)

        self.area_image_path = area_image_path
        self.area_position = area_position
        self.inventory_image_path = inventory_image_path

        # l'objet peut être pris s'il a une image pour l'inventaire !
        self.takeable = inventory_image_path is not None
    
    # TODO: trouver un moyen de ne DEFINIR la méthode que si l'objet est préhensible
    def take(self, adventurestate):
            """Réponse au verbe 'take'"""
            if self.takeable:
                if self.parent.tag == 'inventory':
                    adventurestate.display_description("I already have this item in my inventory!")
                elif self.parent.tag in ['area', 'item']:
                    # on prend l'objet depuis une zone ou depuis un coffre
                    self.parent = adventurestate.inventory
                    # en parallèle, ajouter la vue (les observateurs ne suffisent pas quand une vue est créée)
                    adventurestate.add_item_view_to_inventory(self)
                    self.notify()
                    adventurestate.inventory.notify()
            else:
                adventurestate.display_description("I cannot take this object.")
            return True  # action terminée

    def use(self, adventurestate):
        """Réponse au verbe 'utiliser' (attend par défaut un 2e complément)"""
        if adventurestate.complement is None:
            # pas encore de complément, on retient donc l'objet courant comme le premier complément
            adventurestate.complement = self
            return False  # l'action n'est pas terminée
        else:
            self._use_tool_with(adventurestate, adventurestate.complement)
            print "used tool with!!"
            return True  # action terminée

    def _use_tool_with(self, adventurestate, tool):
        """
        Utilisation combinée de deux objets (par défaut, rien ne se passe)

        Le concepteur doit overrider cette méthode en posant des conditions sur l'outil utilisé.
        """
        adventurestate.display_description("I cannot use %s on %s" % (tool.fullname, self.fullname))

    @property
    def view_position(self):
        if self.parent.tag == 'inventory':
            return None  # pas de position statique dans l'inventaire
        else:
            return self.area_position

    @view_position.setter
    def view_position(self, position):
        if self.parent.tag == 'inventory':
            pass  # idem
        else:
            self.area_position = position

    def __str__(self):
        return "<Item '%s'>" % self.codename


class Container(Item):
    """
    Conteneur : item pouvant être ouvert / fermé, et révélant son contenu lorsqu'il est ouvert

    Il peut être préhensible ou non.

    Attributs hérités :
        codename
        fullname
        description
        observer_list
        parent
        children                   -- contenu

    Attributs propres:
        open_state                -- booléen indiquant si le conteneur est ouvert (True) ou fermé (False)
        key_name                  -- codename de la clé pouvant ouvrir le conteneur, ou None s'il n'y a pas besoin de clé
        area_open_image_path      -- image path (ou peut-être image, à voir)
        inventory_open_image_path -- image path (ou peut-être image, à voir)

    """
    def __init__(self, codename, fullname, adventurestate, parent, area_image_path=None, area_position=None, inventory_image_path=None, open_state=False, key_name=None, area_open_image_path=None, inventory_open_image_path=None):
        Item.__init__(self, codename, fullname, adventurestate, parent, area_image_path, area_position, inventory_image_path)
        self.open_state = open_state
        self.key_name = key_name
        self.area_open_image_path = area_open_image_path
        self.inventory_open_image_path = inventory_open_image_path

    def open(self, adventurestate):
        # print 'trying to open container %s with bare hands' % self.fullname
        if self.open_state:
            adventurestate.display_description("%s is already open." % self.fullname)
        else:
            # le conteneur doit être ouvert, on vérifie si une clé est nécessaire
            if self.key_name is None:
                # ouverture effective du conteneur
                self.open_state = True
                adventurestate.display_description("You open %s." % self.fullname)
            else:
                # si une clé est nécessaire, il faut passer par l'action 'use key with...'
                # remarque : la clé peut être un outil quelconque, comme un pied de biche...
                adventurestate.display_description("You need something to open %s." % self.fullname)
        return True

    def _use_tool_with(self, adventurestate, tool):
        """Applique l'outil qui devrait être une clé ou un autre outil capable d'ouvrir le conteneur"""
        if tool.codename == self.key_name:
            if self.open_state:
                print("%s est déjà ouvert." % self.fullname)
            else:
                self.open_indeed(adventurestate)
                adventurestate.display_description("You open %s with %s." % (self.fullname, tool.fullname))
                # remarque : ici, la clé ne disparaît pas !
        else:
            adventurestate.display_description("I cannot use %s on %s" % (tool.fullname, self.fullname))

    def close(self, adventurestate):
        """Réponse au verbe 'close'"""
        if self.open_state:
            self.close_indeed(adventurestate)
            adventurestate.display_description("You close %s." % self.fullname)

    def remove_element(self, element):
        self.content.remove(element)
        print 'element %s removed from container %s' % (element.codename, self.codename)

    # ne pas utiliser de propriété pour open_state car il faut accéder à des paramètres comme adventurestate en plus
    def open_indeed(self, adventurestate):
        """Ouverture effective"""
        self.open_state = True

        if self.parent.tag == 'inventory':
            # dans l'inventaire, ouvrir une boîte dépose le contenu dans l'inventaire
            print "CONTENT: %s" % self.children
            self.parent.add_item_list(self.content)
            self.remove_all()
            # ajouter également les observateurs dans la vue de l'inventaire !
            adventurestate.add_item_view_to_inventory(contained_item)
        else:  # area
            # à moins de charger tout de suite les objets contenus et de ne les rendre visibles que maintenant, il faut dire à la vue de charger les objets contenus maintenant
            for contained_item in self.children:
                adventurestate.add_item_view_to_area(contained_item)
            # remarque : les objets *restent* contenus, au cas où on refermerait le conteneur
        print("%s has been opened." % self.codename)
        self.notify()  # notifies container and contained!

    def close_indeed(self, adventurestate):
        """fermeture effective"""
        self.open_state = False

        if self.parent.codename == 'inventory':
            # dans l'inventaire, fermer une boîte ne cache pas les objets déjà libérés
            pass
        else:
            pass
            # dans une zone, fermer un conteneur cache les objets contenus (qui n'ont pas encore été pris)
            # ici, on va détruire les observateurs mais on pourrait seulement les masquer
            for contained_item in self.children:
                for item_view in contained_item.observer_list:
                    item_view.destroy()
                # adventurestate.destroy_item_view_from_area(contained_item)
        print("%s has been closed." % self.codename)
        self.notify()  # notifie la vue du conteneur mais aussi celles des objets contenus


class Character(ObservableElement):
    """
    PNJ avec lesquels on peut 'discuter' et plus si affinité (à la discrétion du développeur)

    En développement

    """
    def __init__(self, codename, fullname, adventurestate, parent=None):
        ObservableElement.__init__(self, codename, fullname, adventurestate, "item", parent)

    def talk(self):
        pass


class Gate(ObservableElement):
    """
    Porte : élément de zone faisant passer le joueur dans une autre zone

    Attributs hérités :
        codename            -- identifiant
        fullname            -- nom descriptif (codename par défaut)
        description         -- description
        observer_list       -- liste des observateurs (vues associées à l'objet)
        _visible

    Attributs propres :
        target_area_name     -- nom de la zone ciblée par la porte
        image_path     -- image path utilisée dans la zone
        view_position       -- position dans la zone

    """
    def __init__(self, codename, fullname, adventurestate, parent_room, target_area_name, image_path, view_position, visible=1):
        """Initialise la porte avec l'area passée en argument"""
        ObservableElement.__init__(self, codename, fullname, adventurestate, "gate", parent_room)

        self.target_area_name = target_area_name
        self.image_path = image_path
        self.view_position = view_position

    def __str__(self):
        return "<Gate to %s>" % self.target_area_name


class Inventory(ObservableElement):
    """
    Inventaire du joueur

    Attributs hérités :
        codename
        fullname
        description
        parent              -- parent (éventuellement utile par la suite pour désigner le personnage porteur de l'inventaire)
        children            -- liste des objets dans l'inventaire
        observer_list


    Attributs propres :
        image_path      -- background de l'inventaire
        size            -- dimension de l'inventaire (si pas d'image de fond)

    """
    def __init__(self, adventurestate):
        """Initialisation à vide, les autres caractéristiques seront accédées par set"""
        ObservableElement.__init__(self, "inventory", "l'inventaire", adventurestate, tag="inventory", parent=None)

        self.view_position = None
        self.image_path = None


    def add_item_list(self, item_list):
        """Adds item list to children"""
        for item in item_list:
            self.add_element(item)
        print("Item list %s has been added to inventory." % [item.codename for item in item_list])

    def has_item_by_name(self, item_name):
        # return len([1 for item in self.item_list if item.codename == item_name])
        for item in self.item_list:
            if item.codename == item_name:
                return True
        return False

    def __str__(self):
        inv_str = "Dans l'inventaire, il y a :"


class MenuButton(ObservableElement):
    """Bouton de menu (classe abstraite)"""
    def __init__(self, codename, fullname, adventurestate, image_path, view_position, parent_menu):
        """"""
        ObservableElement.__init__(self, codename, fullname, adventurestate, tag="button", parent=parent_menu)
        self.image_path = image_path
        self.relative_rect = pygame.rect.Rect(view_position, (0, 0))

    def __str__(self):
        return "<MenuButton called %s>" % self.codename


class VerbButton(MenuButton):
    def __init__(self, codename, fullname, adventurestate, image_path, view_position, parent_menu=None):
        """"""
        MenuButton.__init__(self, codename, fullname, adventurestate, image_path, view_position, parent_menu=parent_menu)

    def __str__(self):
        return "<VerbButton for verb '%s'>" % self.codename


class AdventureMenu(ObservableElement):
    """
    Menu des verbes d'action

    Attributs hérités :
        codename
        fullname
        description
        parent
        children            -- liste des boutons
        observer_list       -- liste des observateurs (vues associées à l'objet)

    Attributs propres :
        visible        -- booléen indiquant si le menu est visible
        image_path      -- chemin de l'image utilisée pour le menu
        view_position   -- position à fournir à la vue

    """
    def __init__(self, codename, fullname, adventurestate, image_path, view_position, visible=True, *buttons):
        ObservableElement.__init__(self, codename, fullname, adventurestate, tag="menu", parent=None)
        buttons = list(buttons)
        self.image_path = image_path
        self.view_position = view_position

        # positionnement relatif
        for button in buttons:
            button.relative_rect.move_ip(*self.view_position)
        self.buttons = buttons

        self.all_visible = visible

class ActionSubject(ObservableElement):
    """Sujet représentant l'action courante

    Attributs hérités :
        codename
        fullname
        description
        parent
        children
        observer_list

    Attributs propres :
        _verb            -- le verbe en cours
        _complement      -- le complément en cours
        visible         -- booléen indiquant si le verbe est visible
        image_path      -- chemin de l'image utilisée pour le menu
        view_position   -- position à fournir à la vue

    """
    def __init__(self, adventurestate, starting_verb):
        ObservableElement.__init__(self, 'verb_label', None, adventurestate, tag="verb", parent=None)
        self._verb = starting_verb
        self._complement = None
        # le reste doit être initialisé avant de lancer le jeu
        self.image_path = None
        self.view_position = (0, 0)
        self.textcolor = (255, 255, 255)
        self.bgcolor = (0, 0, 0)

    @property
    def verb(self):
        """Verbe de l'action en cours"""
        return self._verb

    @verb.setter
    def verb(self, value):
        self._verb = value
        self.notify()

    @property
    def complement(self):
        """Verbe de l'action en cours"""
        return self._complement

    @complement.setter
    def complement(self, value):
        self._complement = value
        self.notify()

def set_names(self, codename, fullname):
    """
    helper pour fournir un nom complet si besoin
    1° argument nommé 'self' pour faciliter la lecture

    """
    self.codename = codename
    if fullname is None:
        self.fullname = codename
    else:
        self.fullname = fullname
