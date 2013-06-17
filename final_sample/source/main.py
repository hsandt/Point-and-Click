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
from source.model import models


# def main():
#     pac = pace.state.game.PaCGame((800, 600))
#     pac.manager.enter_state("adventure")

#     room1 = models.Area("blue screen of death", "background.png")
#     room = models.Area("blue screen of death", "../test_resource/background.png")
#     teapot = models.Element("teapot", "../test_resource/teapot.png", (15,30), (60,40))
#     room.add(teapot, "a teapot")
#     print room
#     room.get_element('a teapot').take()nputError,

from helper.files import get_resource_path
# TODO : avoid using resource path at any lod by defining a path at the beginning, that the engine will take into account
from source.helper.setter import set_behaviour

def main():

    # on initialise le jeu point and click
    pac_game = pace.state.game.GameApp((640, 400), title="DEMO game for GETA")

    # on construit l'adventure state avec des salles et des objets
    adv = pac_game.manager.states['adventure']
    adv.set_descriptions_from_file(get_resource_path("descriptions.txt"))

    # room 1
    room1 = models.Area('room1', "first room", adv, get_resource_path("thegoonies_room.png"))
    adv.add_area(room1)
    door1 = models.Gate("door1", "some door", adv, room1, "room2", get_resource_path("door.png"), (352, 142))
    teapot = models.Item("teapot", None, adv, room1, get_resource_path("teapot.png"), (400, 180), get_resource_path("teapot.png"))
    key = models.Item("key", None, adv, room1, get_resource_path("key.png"), (380, 220), get_resource_path("key.png"))

    # room 2
    room2 = models.Area('room2', "another room", adv, get_resource_path("thegoonies_room.png"))
    adv.add_area(room2)
    door2 = models.Gate("door2", "another porte", adv, room2, "drowning", get_resource_path("door.png"), (382, 142))
    locker = models.Container("locker", None, adv, room2, get_resource_path("closed_locker.png"), (325, 150), None, get_resource_path("open_locker.png"), key_name='key')
    
    def use_locker(self, state):
        if state.complement is None:
            state.display_description("I cannot use this item alone.")
            return True
        else:
            self.use_tool_with(state.complement, state)
    set_behaviour(locker, "use", use_locker)

    # drowning room
    drowning = models.Area('drowning', "the drowning 'room'", adv,  get_resource_path("drowning.png"))
    adv.add_area(drowning)

    # on construit des boutons
    button0 = models.VerbButton("look_at", "look at", adv, get_resource_path("small_hit.png"), (38, 38))
    button1 = models.VerbButton("hit", "hit", adv, get_resource_path("small_hit.png"), (38, 70))
    button2 = models.VerbButton("take", "take", adv, get_resource_path("small_take.png"), (38, 102))
    button3 = models.VerbButton("use", "use", adv, get_resource_path("small_use.png"), (38, 134))

    # on les attache à un menu créé à ce moment (ou bien l'avance puis on append/add les boutons, évite les keyword avant args)
    menu = models.AdventureMenu("menu", "Menu statique des verbes d'action", adv, get_resource_path("thegoonies_menu.png"), (102, 20), True, button1, button2, button3)
    adv.set_menu(menu)

    # déplacer l'inventaire là où l'on veut
    adv.set_inventory_view(position=(246, 292), image_path=get_resource_path("thegoonies_inventory.png"))

    # déplacer les actions et descriptions là on l'on veut
    adv.move_action_label_to((10, 230))
    adv.move_description_label_to((270, 350))

    # on peut entrer dans l'area qui est ready
    adv.enter_area('room1')

    # on peut entrer dans le state qui est readyinventory.background = pygame.sprite.DirtySprite()
    pac_game.manager.enter_state("adventure")

    assert pac_game.manager.states['adventure'].area.codename == 'room1'

    # on peut lancer le jeu
    pac_game.run()


if __name__ == '__main__':
    main()