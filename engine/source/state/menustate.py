# -*- coding: utf-8 -*-

import pygame

from gamestate import GameState

class MenuState(GameState):
    """Gamestate du menu de pause

    Attributs :
        gsm        game state manager supervisant ce game state
    
    """

    def __init__(self, gsm, view):
        GameState.__init__(self, gsm, view)
        # self.view.display_text("PAUSE", (300, 230), (0,255,0), (0,0,0), layer=self.view.pause_layer)
        self.view.hide_layer(self.view.pause_layer)

    def on_enter(self):
        self.view.display_text("PAUSE", (300, 230), (0,255,0), (0,0,0))

    def on_exit(self):
        # self.view.remove_sprites_of_layer(self.view.pause_layer)
        self.view.remove(self.view.get_sprites_from_layer(self.view.text_layer)[-1])

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.gsm.incoming_state_name = 'exit'

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.gsm.incoming_state_name = 'adventure'

    def update(self):
        pass

    def render(self, screen):
        self.view.draw(screen)

    def __str__(self):
        return "Menu State"
