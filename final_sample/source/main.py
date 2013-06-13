# -*- coding: utf-8 -*-
import sys
# for the release, remove the next line and change 'source' into 'pace',
# removing the 'as pace
#/Users/macbook/Documents/projet log/Github/Point-and-Click fork/engine

#sys.path.append('/Users/macbook/Documents/projet log/Github/Point-and-Click fork/')

#/Users/hs/Projets/Python/Point-and-click/repo/engine


sys.path.append('/Users/hs/Projets/Python/Point-and-click/repo/engine')

sys.path.append('/Users/macbook/Documents/projet log/Github/Point-and-Click fork/engine')
# import pace
import source as pace # debug version
from source.adventure import models


# def main():
#     pac = pace.state.game.PaCGame((800, 600))
#     pac.manager.enter_state("adventure")

#     room1 = models.Area("blue screen of death", "background.png")
#     room = models.Area("blue screen of death", "../test_resource/background.png")
#     teapot = models.Element("teapot", "../test_resource/teapot.png", (15,30), (60,40))
#     room.add(teapot, "a teapot")
#     print room
#     room.get_element('a teapot').take()

from helper.files import get_resource_path
# TODO : avoid using resource path at any lod by defining a path at the beginning, that the engine will take into account
from source.helper.setter import set_behaviour

def main():

    # on initialise le jeu point and click
    pac_game = pace.state.game.GameApp((640, 400), title="DEMO game for GETA")

    # on construit l'adventure state avec des salles et des objets
    adv = pac_game.manager.states['adventure']
    adv.set_descriptions_from_file(get_resource_path("descriptions.txt"))

    room1 = models.Area('room1', "first room", get_resource_path("thegoonies_room.png"))
    adv.add_area(room1)
    drowning = models.Area('drowning', "the drowning 'room'", get_resource_path("drowning.png"))
    adv.add_area(drowning)
    print room1

    # on ajoute des éléments dans la mock area
    teapot = models.Item("teapot", None, adv, get_resource_path("teapot.png"), get_resource_path("teapot.png"))
    room1.add_item(teapot, position=(15, 30))
    # locker = models.Item("locker", None, adv, get_resource_path("closed_locker.png"), None)
    # locker.open = False
    locker = models.Container("locker", None, adv, get_resource_path("closed_locker.png"), None, get_resource_path("open_locker.png"), key_name='key')
    room1.add_item(locker, position=(80, 60))
    key = models.Item("key", None, adv, get_resource_path("key.png"), get_resource_path("key.png"))
    room1.add_item(key, position=(180, 60))

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
    door = models.Gate(drowning, "door", "porte", get_resource_path("door.png"), (352, 142))
    # room1.add_acitem(door, door.rect.topleft)
    room1.add_gate(door)
    # set_behaviour(door, "on_click", lambda self, state: state.enter_area("drowning"))

    # on construit des boutons
    button1 = models.InteractiveButton("hit", "frapper", get_resource_path("small_hit.png"), (38, 70))
    button2 = models.InteractiveButton("take", "prendre", get_resource_path("small_take.png"), (38, 102))
    button3 = models.InteractiveButton("use", "utiliser", get_resource_path("small_use.png"), (38, 134))

    # on les attache à un menu créé à ce moment (ou bien l'avance puis on append/add les boutons, évite les keyword avant args)
    menu = models.InteractiveMenu(get_resource_path("thegoonies_menu.png"), (102, 20, 0, 0), 1, True, button1, button2, button3)
    adv.set_menu(menu)

    

    # on peut entrer dans l'area qui est ready
    adv.enter_area('room1')

    # on peut entrer dans le state qui est ready
    pac_game.manager.enter_state("adventure")

    assert pac_game.manager.states['adventure'].area.codename == 'room1'

    # on peut lancer le jeu
    pac_game.run()


if __name__ == '__main__':
    main()