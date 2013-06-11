from ..state import game
from .. import adventure

def main():
    pac = game.PaCGame((800, 600))
    pac.context.enter_state("adventure")
    bsod = adventure.models.Area("blue screen of death", "background.png")
    # room = Area("blue screen of death", "../test_resource/background.png")
 #        >>> teapot = Element("teapot", "../test_resource/teapot.png", (15,30), (60,40))
 #        >>> room.add(teapot, "a teapot")
 #        >>> print room
 #        >>> room.get_element('a teapot').take()

if __name__ == '__main__':
    main()