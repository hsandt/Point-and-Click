#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from engine import source as geta

from engine.source.state.game import GameApp
from engine.source.model import models

from helper.files import get_resource_path
from engine.source.helper import setter

def main():

    # on initialise le jeu point and click
    game_app = GameApp((640, 400), title="DEMO game for GETA")

    # on construit l'adventure state avec des salles et des objets
    adv = game_app.manager.states['adventure']
    adv.set_descriptions_from_file(get_resource_path("descriptions.txt"))

    # room 1
    room1 = models.Area('room1', "first room", adv, get_resource_path("thegoonies_room.png"))
    adv.add_area(room1)
    door1 = models.Gate("door1", "some door", adv, room1, "room2", get_resource_path("door.png"), (352, 142))
    teapot = models.Item("teapot", None, adv, None, get_resource_path("teapot.png"), (8, 8), get_resource_path("teapot.png"))
    key = models.Item("key", None, adv, room1, get_resource_path("key.png"), (380, 220), get_resource_path("key.png"))

    # room 2
    room2 = models.Area('room2', "another room", adv, get_resource_path("thegoonies_room.png"))
    adv.add_area(room2)
    door2 = models.Gate("door2", "another porte", adv, room2, "drowning", get_resource_path("door.png"), (382, 142))
    locker = models.Container("locker", None, adv, room2, get_resource_path("closed_locker.png"), (325, 150), None, open_state=False, key_name='key', area_open_image_path=get_resource_path("open_locker.png"))
    locker.acquire_element(teapot)
    print "!!! " + teapot.parent.codename

    def use_locker(self, state):
        if state.complement is None:
            state.display_description("I cannot use this item alone.")
        else:
            self._use_tool_with(state, state.complement)
        return True  # action terminée
    setter.set_behaviour(locker, "use", use_locker)

    # drowning room
    drowning = models.Area('drowning', "the drowning 'room'", adv,  get_resource_path("drowning.png"))
    adv.add_area(drowning)

    # on construit des boutons
    button0 = models.VerbButton("look_at", "look at", adv, get_resource_path("small_hit.png"), (38, 38))
    button1 = models.VerbButton("hit", "hit", adv, get_resource_path("small_hit.png"), (38, 70))
    button2 = models.VerbButton("take", "take", adv, get_resource_path("small_take.png"), (38, 102))
    button3 = models.VerbButton("use", "use", adv, get_resource_path("small_use.png"), (38, 134))
    button4 = models.VerbButton("close", "close", adv, get_resource_path("small_close.png"), (38, 166))

    # on les attache à un menu créé à ce moment
    menu = models.AdventureMenu("menu", "Menu statique des verbes d'action", adv, get_resource_path("thegoonies_menu.png"), (102, 20), True, button1, button2, button3, button4)
    adv.set_menu(menu)

    # déplacer l'inventaire là où l'on veut
    adv.set_inventory_view(position=(246, 292), image_path=get_resource_path("thegoonies_inventory.png"))

    # déplacer les actions et descriptions là on l'on veut
    adv.set_action_label((10, 230), get_resource_path("blank.png"))
    adv.move_description_label_to((270, 350))

    # on peut entrer dans l'area qui est prête
    adv.enter_area('room1')

    # on peut entrer dans le state qui est prêt
    game_app.manager.enter_state("adventure")

    # on peut lancer le jeu
    game_app.run()


if __name__ == '__main__':
    main()
