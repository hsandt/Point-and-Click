# -*- coding: utf-8 -*-

import pygame
from menustate import MenuState
from adventurestate import AdventureState
from ..exception import InputError, AbstractMethodError, GetError


class GameApp(object):
    """
    Classe gérant le lancement du jeu point and click

    Doit être instanciée pour pouvoir construire le monde,
    puis doit être lancée avec la méthode run.

    Attributs :
        screen      --      pygame.Surface représentant l'écran
        window_size --      dimensions utlisées pour l'écran
        title       --      titre du jeu
        FPS         --      FPS du jeu

    """

    def __init__(self, window_size=(640, 480), title="GETA game", FPS=30):
        """Initialisation du jeu : moteur, fenêtre et game states"""
        self.window_size = window_size
        self.title = title
        self.FPS = FPS

        # initialisatio des modules nécessaires à la construction du jeu
        pygame.font.init()
        pygame.display.init() # temp
        self.screen = pygame.display.set_mode(self.window_size)

        # création du game state manager (inclut la création des game states)
        self.manager = GameStateManager()

    def run(self):
        """Lance le jeu
        Gère la boucle event-update-render centrée sur le Game Context"""

        # initialisation des modules restants de pygame et de la fenêtre de jeu
        
        pygame.mixer.init()
        # pygame.display.init()
        # self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption(self.title)

        clock = pygame.time.Clock()

        try:

            while 1:
                self.manager.handle_input()
                self.manager.update()
                self.manager.render(self.screen)
                pygame.display.flip()

                if self.manager.enter_incoming_state():
                    # signal de sortie détecté
                    return

                clock.tick(self.FPS)

        except AbstractMethodError as e:
            print("ERROR: tried to call abstract method  %s from class %s" % (e.method_name, e.class_name))

        except GetError as e:
            print("ERROR: could not find any element with codename %s in %s" % (e.codename, e.container_name))

        except InputError as e:
            print("ERROR: wrong input: %s, expecting one of the following: %s" % (e.expr, e.expected))

        except IOError as e:
            print("IOERROR: " + str(e))


class GameStateManager(object):
    """
    Egalement nommé 'Context' dans le state pattern, il gère les gamestates.

    Attributs :
        states               --      dictionnaire des gamestates
        state                --      gamestate actuel
        _incoming_state_name  --      nom du prochain gamestate à venir, mis à jour dans la méthode update et affecté dès la fin de la boucle de GameApp (la valeur None permet de ne pas changer de gamestate)

    """

    def __init__(self):
        """Crée les gamestates et les associe au manager"""

        # afin d'agréger les gamestates au manager, on fait passer ce dernier en argument du constructeur
        self.states = {
            'menu': MenuState(self),
            'adventure': AdventureState(self)
        }

        self.state = None
        self._incoming_state_name = None

    def handle_input(self):
        """Délègue la gestion des input au gamestate actuel"""
        self.state.handle_input()

    def update(self):
        """Délègue la mise à jour au gamestate actuel"""
        self.state.update()

    def render(self, screen):
        """Délègue le rendu au gamestate actuel"""
        self.state.render(screen)

    def enter_state(self, state_name):
        """Entre dans un nouveau gamestate en appliquant opérations de sortie et d'entrée si applicables"""

        # opération de sortie du state précédent, sauf si c'est le premier invoqué
        if self.state is not None:
            self.state.on_exit()

        # vérification du state name proposé
        if state_name not in self.states:
            raise InputError(state_name, self.states.keys())

        # changement de state
        self.state = self.states[state_name]

        # opération d'entrée du state suivant
        self.state.on_enter()

    def enter_incoming_state(self):
        """
        Helper permettant d'entrer dans le state suivant,
        qui a été déclaré au préalable au cours de l'update précédent

        Renvoie :
            True    -- si la sortie du jeu est invoquée
            False   -- sinon (le state est maintenu ou on passe à un state ordinaire)
        """

        # la plupart du temps, aucun nouveau state n'est attendu
        if self.incoming_state_name is None:
            return False  # pas de sortie

        # sinon, vérifier que state_name est bien une entrée du dictionnaire
        if self.incoming_state_name in self.states:
            self.enter_state(self.incoming_state_name)
            self.incoming_state_name = None  # on ne rechangera plus la prochaine fois a priori
            return False  # pas de sortie

        # state_name particulier ne correspondant à aucun state : sortie du jeu
        if self.incoming_state_name == 'exit':
            return True  # signal de sortie

        # si aucun cas ne convient, l'incoming_state_name n'était pas conforme
        raise InputError(self.incoming_state_name, self.states.keys())

    def set_incoming_state(self, state_name):
        """
        Simple setter pour incoming_state_name

        Peut simplifier l'emploi du développeur en acceptant des paramètres de façon plus souple
        """
        self.incoming_state_name = state_name

    @property
    def incoming_state_name(self):
        return self._incoming_state_name

    @incoming_state_name.setter
    def incoming_state_name(self, state_name):
        # vérification du state name proposé (exit possible)
        if state_name not in self.states.keys() + ['exit']:
            raise InputError(state_name, self.states.keys())
        # sinon, on met à jour _incoming_state_name
        self._incoming_state_name = state_name

    def __str__(self):
        manager_str = "[Game State Manager]\n"
        manager_str += "".join(("- %s\n" % state_name for state_name in self.states))
        return manager_str
