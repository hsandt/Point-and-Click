# -*- coding: utf-8 -*-

import sys
# for the release, remove the next line and change 'source' into 'pace',
# removing the 'as pace'
#/Users/macbook/Documents/projet log/Github/Point-and-Click fork/engine

sys.path.append('/Users/macbook/Documents/projet log/Github/Point-and-Click fork/')
# import pace
import source as pace # debug version
from source.adventure import models
from helper.files import get_resource_path

def main():

    # on initialise le jeu point and click
    pac_game = pace.state.game.PaCGame((800, 600), title="DEMO game for pace")

    # on construit l'adventure state avec des salles et des objets
    adv = pac_game.context.states['adventure']
    bsod = models.Area('bsod', "blue screen of death", get_resource_path("background.png"))
    adv.add_area(bsod)

    # on ajoute des éléments dans la mock area
    teapot = models.Item("teapot", None, get_resource_path("teapot.png"), get_resource_path("teapot.png"))
    bsod.add_acitem(teapot.area_clickable, position=(15, 30))
    locker = models.Item("locker", None, get_resource_path("open_locker.png"), get_resource_path("open_locker.png"))
    bsod.add_acitem(locker.area_clickable, position=(80, 60))

    # on construit des boutons
    button1 = models.InteractiveButton("take", "Prendre", get_resource_path("take.png"), (40, 550))    

    # on les attache à un menu créé à ce moment (ou bien l'avance puis on append/add les boutons, évite les keyword avant args)
    menu = models.InteractiveMenu(get_resource_path("menu.png"), (40, 550, 160, 60), True, button1)
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