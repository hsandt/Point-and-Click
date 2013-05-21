import sys
# sys.path.append('/Developer/Library/Python')
sys.path.append('/Users/hs/Projets/Python/Point-and-click/repo/engine')
# import pace
import source as pace

def main():
	pac = pace.state.PaCGame((800, 600))
	pac.enter_state("adventure")

	bsod = pace.adventure.models.Area("blue screen of death", "../test_resource/background.png")
	room = Area("blue screen of death", "../test_resource/background.png")
        >>> teapot = Element("teapot", "../test_resource/teapot.png", (15,30), (60,40))
        >>> room.add(teapot, "a teapot")
        >>> print room
        >>> room.get_element('a teapot').take()

if __name__ == "main":
	main()