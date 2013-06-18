# -*- coding: utf-8 -*-

from nose import with_setup
from nose.tools import raises

from ..exception.exception import InputError, GetError
from ..state.game import GameApp
from ..model import models
from ..helper.files import get_resource_path


def setup_module(module):
    module.game = GameApp((800, 600))
    adv = module.game.manager.states['adventure']
    adv.set_descriptions_from_file(get_resource_path("descriptions.txt"))
    module.mock_area = models.Area('bsod', "blue screen of death", adv, get_resource_path("background.png"))
    module.mock_item = models.Item("teapot", "some teapot", adv, None, get_resource_path("teapot.png"), (15, 30), get_resource_path("teapot.png"))

def setup_state():
    # repeat game build here...
    game.manager.enter_state('adventure')

def teardown_state():
    game.manager.state = None

def setup_area():
    game.manager.states['adventure'].add_area(mock_area)

def teardown_area():
    game.manager.states['adventure'].remove_area('bsod')

def setup_item():
    game.manager.states['adventure'].areas['bsod'].acquire_element(mock_item)

def teardown_item():
    game.manager.states['adventure'].areas['bsod'].remove_element(mock_item)

def setup_enter_area():
    game.manager.states['adventure'].enter_area('bsod')

def teardown_enter_area():
    game.manager.states['adventure'].leave_area()

def test_screen():
    assert game.screen.get_size() == (800, 600)

def test_FPS():
    assert game.FPS == 30

@with_setup(setup_state, teardown_state)
@with_setup(setup_area, teardown_area)
@with_setup(setup_item, teardown_item)
def test_add_item():
    try:
        game.manager.states['adventure'].areas['bsod'].get_element_by_name("teapot")
    except GetError:
        self.fail()

@with_setup(setup_state, teardown_state)
@with_setup(setup_area, teardown_area)
@with_setup(setup_enter_area, teardown_enter_area)
def test_enter_area():
    adventure = game.manager.states['adventure']
    assert adventure.area.codename == 'bsod'

# fixtures per test
def setup_enter_state():
    game.manager.enter_state('menu')

def teardown_enter_state():
    game.manager.enter_state('adventure')

def setup_enter_incoming_state():
    game.manager.set_incoming_state('menu')
    game.manager.enter_incoming_state()

# effective tests
@with_setup(setup_state)
def test_first_state():
    gc = game.manager
    assert gc.state == gc.states['adventure']

@with_setup(setup_state)
@with_setup(setup_enter_state, teardown_enter_state)
def test_enter_state():
    gc = game.manager
    assert gc.state == gc.states['menu']

@with_setup(setup_state)
@raises(InputError)
def test_enter_wrong_state():
    game.manager.enter_state('wrong_state')

@with_setup(setup_state)
@with_setup(setup_enter_incoming_state, teardown_enter_state)
def test_enter_incoming_state():
    game.manager.set_incoming_state('menu')
    game.manager.enter_incoming_state()
    gc = game.manager
    assert gc.state == gc.states['menu']
