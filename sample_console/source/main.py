# -*- coding: utf-8 -*-
import sys
# for the release, remove the next line and change 'source' into 'pace',
# removing the 'as pace
#/Users/macbook/Documents/projet log/Github/Point-and-Click fork/engine

#sys.path.append('/Users/macbook/Documents/projet log/Github/Point-and-Click fork/')

#/Users/hs/Projets/Python/Point-and-click/repo/engine


# sys.path.append('/Users/hs/Projets/Python/Point-and-click/repo/engine')
# sys.path.append('/Users/macbook/Documents/projet log/Github/Point-and-Click fork/engine')

# import pace
from engine import source as geta

# def main():
#     pac = pace.state.game.PaCGame((800, 600))
#     pac.context.enter_state("adventure")

#     bsod = models.Area("blue screen of death", "background.png")
#     room = models.Area("blue screen of death", "../test_resource/background.png")
#     teapot = models.Element("teapot", "../test_resource/teapot.png", (15,30), (60,40))
#     room.add(teapot, "a teapot")
#     print room
#     room.get_element('a teapot').take()

from helper.files import get_resource_path
# TODO : avoid using resource path at any lod by defining a path at the beginning, that the engine will take into account

def main():

    # on initialise le jeu point and click
    pac_game = geta.state.game.GameApp((640, 400), title="DEMO game for pace")

    # on construit l'adventure state avec des salles et des objets
    adv = pac_game.manager.states['adventure']
    adv.set_descriptions_from_file(get_resource_path("descriptions.txt"))

    bsod = geta.model.models.Area('bsod', "blue screen of death", get_resource_path("background.png"))
    adv.add_area(bsod)
    drowning = geta.model.models.Area('drowning', "the drowning 'room'", get_resource_path("drowning.png"))
    adv.add_area(drowning)

    # # room 1
    # room1 = models.Area('room1', "first room", adv, get_resource_path("thegoonies_room.png"))
    # adv.add_area(room1)
    # door1 = models.Gate("door1", "some door", adv, room1, "room2", get_resource_path("door.png"), (352, 142))
    # teapot = models.Item("teapot", None, adv, None, get_resource_path("teapot.png"), (8, 8), get_resource_path("teapot.png"))
    # key = models.Item("key", None, adv, room1, get_resource_path("key.png"), (380, 220), get_resource_path("key.png"))
    #
    # # room 2
    # room2 = models.Area('room2', "another room", adv, get_resource_path("thegoonies_room.png"))
    # adv.add_area(room2)
    # door2 = models.Gate("door2", "another porte", adv, room2, "drowning", get_resource_path("door.png"), (382, 142))
    # locker = models.Container("locker", None, adv, room2, get_resource_path("closed_locker.png"), (325, 150), None, open_state=False, key_name='key', area_open_image_path=get_resource_path("open_locker.png"))
    # locker.acquire_element(teapot)
    #
    #
    # on ajoute des éléments dans la mock area
    teapot = geta.model.models.Item("teapot", None, adv, get_resource_path("teapot.png"), get_resource_path("teapot.png"))
    bsod.acquire_element(teapot, position=(15, 30))
    # locker = models.Item("locker", None, adv, get_resource_path("closed_locker.png"), None)
    # locker.open = False
    locker = geta.model.models.Container("locker", None, adv, get_resource_path("closed_locker.png"), None, get_resource_path("open_locker.png"), key_name='key')
    bsod.add_item(locker, position=(80, 60))
    key = geta.model.models.Item("key", None, adv, get_resource_path("key.png"), get_resource_path("key.png"))
    bsod.add_item(key, position=(180, 60))

    # on change le comportement par défaut du locker

    def cannot_take(item, state):
        print "I cannot take " + str(item) + "!"
        return True

    geta.helper.setter.set_behaviour(locker, "take", cannot_take)

    # use key behaviour
    # note that, Q5-like, we can directly use the key in the room with the locker without taking it
    # then the key will remain in the room...!

    def use_key(key, state):
        state.complement = "key"
        return False
    geta.helper.setter.set_behaviour(key, "use", use_key)

    # porte "à la main"
    # door = models.Clickable("door", "porte", get_resource_path("door.png"), (200,20))
    door = geta.model.models.Gate(drowning, "door", "porte", get_resource_path("door.png"), (200, 20))
    # bsod.add_acitem(door, door.rect.topleft)
    bsod.add_gate(door)
    # set_behaviour(door, "on_click", lambda self, state: state.enter_area("drowning"))

    # on construit des boutons
    button1 = geta.model.models.InteractiveButton("take", "Prendre", get_resource_path("take.png"), (0, 0))
    button2 = geta.model.models.InteractiveButton("use", "Utiliser", get_resource_path("use.png"), (100, 0))
    button3 = geta.model.models.InteractiveButton("open", "Ouvrir", get_resource_path("open.png"), (200, 0))

    # on les attache à un menu créé à ce moment (ou bien l'avance puis on append/add les boutons, évite les keyword avant args)
    menu = geta.model.models.InteractiveMenu(get_resource_path("menu.png"), (40, 340, 160, 60), 1, True, button1, button2, button3)
    adv.set_menu(menu)

    

    # on peut entrer dans l'area qui est ready
    adv.enter_area('bsod')

    # on peut entrer dans le state qui est ready
    pac_game.context.enter_state("adventure")

    assert pac_game.context.states['adventure'].area.codename == 'bsod'

    # on peut lancer le jeu
    pac_game.run()


if __name__ == '__main__':
    main()
