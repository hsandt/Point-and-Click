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
    bsod = models.Area('bsod', get_resource_path("background.png"), fullname="blue screen of death")
    adv.add_area(bsod)

    # on ajoute des éléments dans la mock area
    teapot = models.Element("teapot", get_resource_path("teapot.png"), (15, 30), (60, 40), fullname="a teapot")
    bsod.add(teapot)
    locker = models.Element("locker", get_resource_path("open_locker.png"), (80, 60), (30, 20), fullname="an opened locker")
    bsod.add(locker)

    # on peut entrer dans l'area qui est ready
    adv.enter_area('bsod')

    # on peut entrer dans le state qui est ready
    pac_game.context.enter_state("adventure")

    assert pac_game.context.states['adventure'].area.codename == 'bsod'

    # on peut lancer le jeu
    pac_game.run()

if __name__ == '__main__':
    main()