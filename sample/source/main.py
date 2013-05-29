import sys
sys.path.append('/Users/hs/Projets/Python/Point-and-click/repo/engine')
# import pace
import source as pace # debug version
from source.adventure import models

def main():
    pac_game = pace.state.game.PaCGame((800, 600))
    adv = pac_game.context.states['adventure']


    bsod = models.Area("blue screen of death", "background.png")
    room = models.Area("blue screen of death", "../test_resource/background.png")
    teapot = models.Element("teapot", "../test_resource/teapot.png", (15,30), (60,40))
    room.add(teapot, "a teapot")
    print room
    room.get_element('a teapot').take()

    pac.context.enter_state("adventure")

if __name__ == '__main__':
    main()