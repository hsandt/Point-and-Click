#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
# for the release, remove the next line and change 'source' into 'pace',
# removing the 'as pace'
sys.path.append('/Users/hs/Projets/Python/Point-and-click/repo/engine')
sys.path.append('/Users/macbook/Documents/projet log/Github/Point-and-Click fork/engine')
# import pace
import source as pace # debug version
from source.adventure import models
from helper.files import get_resource_path
# TODO : avoid using resource path at any load by defining a path at the beginning, that the engine will take into account
from source.helper.setter import set_behaviour


def main():
    """Exemple de jeu avec manu dynamique style Monkey Island 3"""
    # on initialise le jeu point and click
    pac_game = pace.state.game.PaCGame((640, 400), title="DEMO game for pace")

    # on construit l'adventure state avec des salles et des objets
    adv = pac_game.context.states['adventure']
    adv.set_descriptions_from_file(get_resource_path("descriptions.txt"))

    bsod = models.Area('bsod', "blue screen of death", get_resource_path("background.png"))
    adv.add_area(bsod)
    drowning = models.Area('drowning', "the drowning 'room'", get_resource_path("drowning.png"))
    adv.add_area(drowning)

    # on ajoute des éléments dans la mock area
    teapot = models.Item("teapot", None, adv, get_resource_path("teapot.png"), get_resource_path("teapot.png"))
    bsod.add_item(teapot, position=(15, 30))
    # locker = models.Item("locker", None, adv, get_resource_path("closed_locker.png"), None)
    # locker.open = False
    # locker = models.Container("locker", None, adv, get_resource_path("closed_locker.png"), None, get_resource_path("open_locker.png"), key_name='key')
    locker = models.Container("locker", None, adv, get_resource_path("closed_locker.png"), None, get_resource_path("open_locker.png"), key_name='key')
    bsod.add_item(locker, position=(80, 60))
    key = models.Item("key", None, adv, get_resource_path("key.png"), get_resource_path("key.png"))
    bsod.add_item(key, position=(180, 60))

    # on change le comportement par défaut du locker
    def cannot_take(item, state):
        print "I cannot take " + str(item) + "!"
        return True
    set_behaviour(locker, "take", cannot_take)

    # use key behaviour
    # note that, Q5-like, we can directly use the key in the room with the locker without taking it
    # then the key will remain in the room...!
    def use_key(key, state):
        state.complement = "key"
        return False
    set_behaviour(key, "use", use_key)

    # porte "à la main"
    # door = models.Clickable("door", "porte", get_resource_path("door.png"), (200,20))
    door = models.Gate(drowning, "door", "porte", get_resource_path("door.png"), (200, 20))
    # bsod.add_acitem(door, door.rect.topleft)
    bsod.add_gate(door)
    # set_behaviour(door, "on_click", lambda self, state: state.enter_area("drowning"))

    # on construit des boutons
    button1 = models.InteractiveButton("take", "Prendre", get_resource_path("take.png"), (0, 0))
    button2 = models.InteractiveButton("use", "Utiliser", get_resource_path("use.png"), (100, 0))
    # button3 = models.InteractiveButton("open", "Ouvrir", get_resource_path("open.png"), (200, 0))
    button3 = models.InteractiveButton("open", "Ouvrir", get_resource_path("open.png"), (200, 0))

    # on les attache à un menu créé à ce moment (ou bien l'avance puis on append/add les boutons, évite les keyword avant args)
    dynamic_menu = models.InteractiveMenu(get_resource_path("menu.png"), (40, 340, 160, 60), 0, True, button1, button2, button3)
    adv.set_menu(dynamic_menu)

    adv.set_query_mode()

    # # change behaviour of button open: keeps complement
    # def query_button_on_click(self, adventurestate):
    #     adventurestate.display_menu_for(self)
    # set_behaviour(locker, "query", query_button_on_click)

    # # change behaviour of open button: used after complement has been chosen
    # def open_after_complement(self, adventurestate):
    #     adventurestate.verb = 'open'  # opt. ici mais pratique en mouse-over pour voir ce qu'on fait
    #     # direct link to item with a method 'get_by_name'? but this ensures the item is in the current area...
    #     if getattr(adventurestate.area.get_item_by_name(adventurestate.complement), adventurestate.verb)(adventurestate):
    #         # if True is returned, the action has been completed
    #         del adventurestate.verb
    #         del adventurestate.complement
    # set_behaviour(button3, "on_click", open_after_complement)

    # on peut entrer dans l'area qui est ready
    adv.enter_area('bsod')

    # on peut entrer dans le state qui est ready
    pac_game.context.enter_state("adventure")

    assert pac_game.context.states['adventure'].area.codename == 'bsod'

    # on peut lancer le jeu
    pac_game.run()

if __name__ == '__main__':
    main()