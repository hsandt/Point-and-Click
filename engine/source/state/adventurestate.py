# -*- coding: utf-8 -*-

import pygame

from gamestate import GameState
from ..model import models
from ..view import views
from ..exception.exception import OverwriteError, GetError

from ..helper.load import load_descriptions


class AdventureState(GameState):
    """Gamestate du mode principal de jeu

    Attributs hérités :
        gsm         --  game state manager supervisant ce game state
        view        --  vue

    Attributs :
        areas        --  ensemble des zones en jeu
        area         --  zone en cours de visite
        inventory    --  inventaire de l'avatar
        menu         --  menu interactif
        default_verb --  verbe par défaut (appelé sur clic gauche sans rien)
        verb         --  verbe en cours de sélection
        complement   --  1° complément de l'action
        description_hash -- hash des descriptions (pour l'instant, n'est pas initialisé automatiquement)

        cursor       -- à venir

    """

    def __init__(self, gsm, view):
        """Initialisation des ressources et des modèles (une seule fois)"""
        GameState.__init__(self, gsm, view)
        self.areas = {}
        self.area = None
        self.description_hash = {}
        self.default_verb = 'look_at'
        self._action_subject = models.ActionSubject(self, self.default_verb)
        self._complement = None  # idem
        self.inventory = models.Inventory(self)

        # query mode encore en beta
        # self.set_query_mode(False)

    def on_enter(self):

        self.cursor = None  # TODO: autoriser les curseurs personnalisés
        # mouse_command décrit, pour chaque bouton de la souris, l'état d'appui
        # 0 : relâché, 1 : vient d'être pressé, 2 : en cours d'appui
        # et la position du clic (None ici)
        self.mouse_command = {'left': [0, None], 'right': [0, None]}

        # on réinitialise l'action
        del self.verb
        del self.complement
        
    def on_exit(self):
        pass

    def handle_input(self):
        """
        Gère les évènements séparéments de l'update

        Permet de considérer tous les évènements avant de commencer la mise à jour

        """
        for event in pygame.event.get():

            # détection escape (quitter le jeu)
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.gsm.incoming_state_name = 'exit'  # changement toléré 

            # détection space pour ouvrir le menu pause
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.gsm.incoming_state_name = 'menu'

            # détection clics souris : entrée -> assigner le sprite cliqué (situé le plus haut)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # we should add a safety to check that view is not void, especially when
                # only clickable are considered (otherwise bg has odds to be clicked on)
                if event.button == 1:
                    if self.mouse_command['left'][0] == 0:  #  if mouse button has just been set down
                        self.mouse_command['left'][:] = [1, event.pos]  # 1 for 'new click' (may be called several times due to looping)
                elif event.button == 2:
                    if self.mouse_command['right'][0] == 0:  #  if mouse button has just been set down
                        self.mouse_command['right'][:] = [1, event.pos]  # 1 for 'new click'

            # détection clics souris : sortie
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_command['left'][0] = 0  # means no clicks, you can keep old mouse position
                elif event.button == 2:
                    self.mouse_command['right'][0] = 0

    def update(self):

        # on regarde si on a cliqué (clic gauche) sur un élément du jeu
        if self.mouse_command['left'][0] == 1:  # only consider new clicks for action clicks
            print "click detected on " + str(self.mouse_command['left'][1])

            self.mouse_command['left'][0] = 2  # say it's now in 'hold mode'
            ## TODO : customize with mask collision

            # on teste les sprites sur lesquels on a pu vouloir cliquer en commençant
            # par celui dessiné le plus au-dessus
            reversed_sprites = self.view.get_sprites_at(self.mouse_command['left'][1])
            reversed_sprites.reverse()
            for sprite in reversed_sprites:
                # vérifier que le sprite est visible et cliquable, sinon on l'ignore
                if sprite.visible and hasattr(sprite, 'on_click'):
                    sprite.on_click(self, button=1)
                    return  # cela suffit, on a trouvé le sprite voulu
            # si on ne trouve rien de convenable c'est qu'on a cliqué dans le décor
            print("click detected on the background")
            del self.verb
            del self.complement

    def render(self, screen):
        self.view.draw(screen)

    # méthodes de construction du jeu

    def add_area(self, area):
        """
        Attache la zone area à l'AdventureState sous l'entrée codename dans le dictionnaire

        Le nom de code permet d'avoir des noms simplifiés et toujours distincts.
        Si le nom de code proposé a déjà été entré, la méthode lance une exception.
        Exemple : "Laboratoire" -> "labo", une autre salle nommée "Laboratoire" -> "labo2"

        """
        if area.codename in self.areas:
            raise OverwriteError(area.codename, "Could not overwrite preexisting area codename: " + area.codename)
        self.areas[area.codename] = area
        print "added area"

    def remove_area(self, codename):
        if codename not in self.areas:
            raise GetError(codename, "Could not remove area because of unexisting codename: " + codename)
        del self.areas[codename]  # mutates the dictionary
        print "removed area"

    def enter_area(self, area_codename):
        # area on_exit ?
        print "entering area..." + area_codename
        self.area = self.areas[area_codename]
        self.view.load_area(self.area)

    # un peu pour le debug, un peu pour "on_exit"
    def leave_area(self):
        self.area = None
        self.view.empty()

    def set_descriptions_from_file(self, file_path):
        self.description_hash = load_descriptions(file_path)

    # gère modèles et vues, évite les rafraîchissements inutiles
    # def remove_item_from_area(self, item, area):
    #     """Retire un item d'une zone donnée"""
    #     self.area.remove_item(item)
    #     self.view.remove_item(item)

    # def remove_item_by_name_from_area(self, item_name, area):
    #     """Retire un item d'une zone donnée"""
    #     self.area.remove_item_by_name(item_name)
    #     self.view.remove_item_by_name(item_name)

    # def remove_item(self, item):
    #     """Retire un item de la zone active"""
    #     self.remove_item_from_area(item, self.area)

    # def remove_item_by_name(self, item_name):
    #     """Retire un item de la zone active"""
    #     self.remove_item_by_name_from_area(item_name, self.area)

    def set_menu(self, menu):
        """setter de modèle avec construction automatique de la vue"""
        self.menu = menu
        self.view.load_menu(menu)

    def set_inventory_view(self, position, image_path):
        """setter de la vue seulement car l'inventaire modèle est automatiquement créé"""
        self.inventory.view_position = position
        self.inventory.image_path = image_path
        self.view.load_inventory(self.inventory)

    def set_action_label(self, position, image_path, visible=1, textcolor=(255, 255, 255), bgcolor=(0, 0, 0)):
        self._action_subject.view_position = position
        self._action_subject.image_path = image_path
        self.view.load_action_label(self._action_subject, image_path, position, visible, textcolor, bgcolor)

    def set_default_verb(self, verb):
        self.default_verb = verb

    @property
    def verb(self):
        """Verbe de l'action en cours"""
        return self._action_subject.verb

    @verb.setter
    def verb(self, value):
        self._action_subject.verb = value

    @verb.deleter
    def verb(self):
        self._action_subject.verb = self.default_verb
        # pour l'instant, on suppose que le complément reste
        # self.refresh_action_label()

    @property
    def complement(self):
        """Verbe de l'action en cours"""
        return self._action_subject._complement

    @complement.setter
    def complement(self, value):
        self._action_subject._complement = value
        # self.refresh_action_label()

    @complement.deleter
    def complement(self):
        self._action_subject._complement = None
        # on suppose que le verbe reste
        # self.refresh_action_label()

    def refresh_action_label(self):
        """
        Rafraîchit l'indication de l'action en cours

        Plutôt dans l'adventure state que la vue car supposé
        'haut niveau', dépend du jeu et peut être overridée (avec la bonne doc)

        """
        # pour l'instant, la préposition par défaut est 'avec'
        if self.complement is None:
            action_str = self.verb
        else:
            action_str = " %s %s avec ..." % (self.verb, self.complement)
        self.view.setActionText(action_str, None, (255, 255, 255), (0, 0, 0))


    def display_menu_for(self, complement_object):
        """BETA : affiche le menu dynamique en mode query"""
        self.verb = '???'  # action still undefined
        self.complement = complement_object.codename  # but complement is for a dynamic menu
        self.view.display_menu()

    def hide_menu(self):
        """BETA : Masque le menu dynamique ET rétablit l'action par défaut"""
        del self.verb
        del self.complement
        self.view.hide_menu()

    # def display_text(self, text, position, textcolor=(255, 255, 255), bgcolor=(0, 0, 0)):
    #     self.view.display_text(text, position, textcolor=(255, 255, 255), bgcolor=(0, 0, 0))

    

    def set_query_mode(self, query_mode=True):
        """BETA : Active le mode 'query' pour tous les modèles
        !! modification structurelle (classes) et non seulement pour les instances de state adventure
        """
        if query_mode:
            self.default_verb = 'query'
            models.Item.query = lambda self, adventurestate: adventurestate.display_menu_for(self)
            models.InteractiveButton.on_click = models._on_click_for_query_interactive_button
        else:
            self.default_verb = 'look_at'
            if hasattr(models.Item, 'query'):
                del models.Item.query
            # query mode still in beta
            # models.InteractiveButton.on_click = models._on_click_for_interactive_button

    # peut-être ajouter .name pour accéder au nom plus facilement (et faire des tests)
    def __str__(self):
        return "Adventure State"

    # pure view methods
    def move_action_label_to(self, position):
        self.view.move_text(position, index=0)  # index 0 pour les actions

    def move_description_label_to(self, position):
        self.view.move_text(position, index=1)  # index 1 pour les descriptions

    def display_description(self, text, position=None, textcolor=(255,255,255), bgcolor=(0,0,0)):
        self.view.set_text(text, position, 1, textcolor, bgcolor)
