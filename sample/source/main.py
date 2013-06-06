import sys
# for the release, remove the next line and change 'source' into 'pace',
# removing the 'as pace'
#/Users/macbook/Documents/projet log/Github/Point-and-Click fork/engine

sys.path.append('/Users/macbook/Documents/projet log/Github/Point-and-Click fork/')

# import pace
import source as pace # debug version
from source.adventure import models

def main():
    pac = pace.state.game.PaCGame((800, 600))
    pac.context.enter_state("adventure")

    bsod = models.Area("blue screen of death", "background.png")
    room = models.Area("blue screen of death", "../test_resource/background.png")
    teapot = models.Element("teapot", "../test_resource/teapot.png", (15,30), (60,40))
    room.add(teapot, "a teapot")
    print room
    room.get_element('a teapot').take()

if __name__ == '__main__':
    main()