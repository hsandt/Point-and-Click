# -*- coding: utf-8 -*-

import sys
# for the release, remove the next line and change 'source' into 'pace',
# removing the 'as pace'
sys.path.append('/Users/hs/Projets/Python/Point-and-click/repo/engine')
# import pace
import source as pace # debug version
from source.adventure import models
from helper.files import get_resource_path

def main():

    # on initialise le jeu point and click
    pac_game = pace.state.game.PaCGame((800, 600), title="DEMO game for pace")

    # on construit l'adventure state avec des salles et des objets
    adv = pac_game.context.states['adventure']
    bsod = models.Area('bsod', "blue screen of death", get_resource_path("background.png"), )
    adv.add_area(bsod)

    # on ajoute des éléments dans la mock area
    teapot = models.Clickable("teapot", None, get_resource_path("teapot.png"), (15, 30))
    bsod.add(teapot)
    locker = models.Clickable("locker", None, get_resource_path("open_locker.png"), (80, 60))
    bsod.add(locker)

    # on construit des boutons
    button1 = models.InteractiveButton("take", get_resource_path("take.png"), (40, 550), fullname="Prendre")    

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