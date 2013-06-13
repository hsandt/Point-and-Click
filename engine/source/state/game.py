# -*- coding: utf-8 -*-

import pygame
from menustate import MenuState
from adventurestate import AdventureState
from ..exception import InputError, AbstractMethodError, GetError


class PaCGame(object):
    """
    Classe gérant le lancement du jeu point and click
    
    A instancier pour démarrer le jeu
    Gère la boucle event-update-render centrée sur le Game Context

    Attributs:
        screen      --      pygame.Surface représentant l'écran de jeu
        title       --      titre du jeu (inusité)
        FPS         --      FPS utilisé pour le jeu

    """

    def __init__(self, window_size=(600, 400), title="Pace game", FPS=60):
        """Initialisation du jeu : moteur, fenêtre et game states"""
        self.window_size = window_size
        self.title = title
        self.FPS = FPS

        # création du game context (inclut la création des game states)
        self.context = GameContext()

    def run(self):
        """Lance le jeu"""
        # initialisation de pygame et de la fenêtre de jeu
        pygame.init()
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption(self.title)

        clock = pygame.time.Clock()

        try:
            while 1:  # or while(not end state)
                self.context.handle_input()
                self.context.update()
                self.context.render(self.screen)
                pygame.display.flip()

                if self.context.enter_incoming_state():
                    return  # signal de sortie détecté

                clock.tick(self.FPS)
        except AbstractMethodError as e:
            print("ERROR: tried to call an abstract method  %s from class %s", e.method_name, e.class_name)
        except GetError as e:
            print("ERROR: could not find any element with codename %s in %s", e.codename, e.container_name)
        except IOError as e:
            print("IOERROR: " + str(e))


class GameContext(object):
    """
    Contexte du state pattern appliqué aux gamestates
    Remarque : si d'autres states, ne pas hésiter utiliser des héritages ou des décorateurs

    Attributs:
    state                --      état actuel
    incoming_state_name  --      prochain state à venir, mis à jour par update() et affecté dès la fin de la boucle (None pour garder le même state)

    """

    def __init__(self):
        """Initialise les gamestates et lance le state initial"""

        # on stocke les states en mémoire en leur associant réciproquement le game context 'self'
        self.states = {
            'menu': MenuState(self),
            'adventure': AdventureState(self)
        }

        self.state = None
        self.incoming_state_name = None

    def enter_state(self, state_name):
        """Change le gamestate actuel en appliquant les pre/post-conditions si applicables"""

        # pre-condition (sortie du state précédent)
        if self.state is not None:
            self.state.on_exit()

        # vérification du state name proposé
        if state_name not in self.states:
            raise InputError(state_name, "Entrée vers un state name qui n'est pas dans la liste")

        # changement de state
        self.state = self.states[state_name]

        # post-condition (entrée dans le state suivant)
        self.state.on_enter()

    def enter_incoming_state(self):
        """
        helper permettant d'entrer dans le state suivant, prévu au cours d'un update

        Renvoie :
            True    -- si le jeu doit être quitté
            False   -- sinon (state maintenu ou modifié normalement)
        """

        # la plupart du temps, aucun nouveau state n'est attendu
        if self.incoming_state_name is None:
            return False  # pas de sortie

        # sinon, vérifier que state_name est bien dans la liste
        if self.incoming_state_name in self.states:
            # changement de state approprié
            self.enter_state(self.incoming_state_name)
            self.incoming_state_name = None  # on rechangera plus la prochaine fois
            return False  # pas de sortie

        # state_name particulier ne correspondant à aucun state : sortie du jeu
        if self.incoming_state_name == 'exit':
            return True  # signal de sortie

        # sinon, l'incoming_state_name n'était pas conforme
        raise InputError(self.incoming_state_name, "Entrée vers un incoming state name qui n'est ni 'exit' ni dans la liste")

    def handle_input(self):
        self.state.handle_input()

    def update(self):
        self.state.update()

    def render(self, screen):
        self.state.render(screen)

    def set_incoming_state(self, state_name):
        """
        Simple setter pour incoming_state_name

        Peut simplifier l'emploi du développeur en acceptant des paramètres de façon plus souple
        """
        self.incoming_state_name = state_name

    def __str__(self):
        context_str = "[Game Context]"
        context_str.join([state_name for state_name in self.states])
        return context_str
