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
# TODO : avoid using resource path at any lod by defining a path at the beginning, that the engine will take into account
from source.helper.setter import set_behaviour

def main():

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
    bsod.add_acitem(teapot.area_clickable, position=(15, 30))
    locker = models.Item("locker", None, adv, get_resource_path("closed_locker.png"), None)
    locker.open = False
    bsod.add_acitem(locker.area_clickable, position=(80, 60))
    key = models.Item("key", None, adv, get_resource_path("key.png"), get_resource_path("key.png"))
    bsod.add_acitem(key.area_clickable, position=(180, 60))

    # on change le comportement par défaut du locker
    def cannot_take(item, state):
        print "I cannot take " + str(item) + "!"
    set_behaviour(locker, "take", cannot_take)

    # use key behaviour
    # note that, Q5-like, we can directly use the key in the room with the locker without taking it
    # then the key will remain in the room...!
    def use_key(key, state):
        state.set_complement("key")
    set_behaviour(key, "use", use_key)

    # use key on locker behaviour (actually use locker when complement is set at 'key')
    # we could also change the verb to 'use2' or 'use_object_on'

    # rather, we should have only one use method and use_X_on_Y should be used as a 'case' of use
    def use_key_on_locker(locker, state):
        if state.complement == 'key':
            locker.open = True
            locker.area_clickable.change_image(get_resource_path("open_locker.png"))
        else:
            print "you cannot use the locker this way"
    set_behaviour(locker, "use", use_key_on_locker)

    # porte "à la main"
    # door = models.Clickable("door", "porte", get_resource_path("door.png"), (200,20))
    door = models.Gate(drowning, "door", "porte", get_resource_path("door.png"), (200, 20))
    # bsod.add_acitem(door, door.rect.topleft)
    bsod.add_gate(door)
    # set_behaviour(door, "on_click", lambda self, state: state.enter_area("drowning"))

    # on construit des boutons
    button1 = models.InteractiveButton("take", "Prendre", get_resource_path("take.png"), (40, 340))
    button2 = models.InteractiveButton("use", "Utiliser", get_resource_path("use.png"), (210, 306))

    # on les attache à un menu créé à ce moment (ou bien l'avance puis on append/add les boutons, évite les keyword avant args)
    menu = models.InteractiveMenu(get_resource_path("menu.png"), (40, 340, 160, 60), True, button1, button2)
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