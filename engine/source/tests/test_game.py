# -*- coding: utf-8 -*-

from nose import with_setup
from nose.tools import raises

from ..exception.exception import InputError
from ..state.game import PaCGame
from ..adventure import models
from ..helper.files import get_resource_path


def setup_module(module):
    module.game = PaCGame((800, 600))
    module.mock_area = models.Area('bsod', get_resource_path("background.png"), fullname="blue screen of death")
    module.mock_item = models.Element("teapot", get_resource_path("teapot.png"), (15, 30), (60, 40), fullname="a teapot")

def setup_state():
    # repeat game build here...
    game.context.enter_state('adventure')

def teardown_state():
    game.context.state = None

def setup_area():
    game.context.states['adventure'].add_area(mock_area)

def teardown_area():
    game.context.states['adventure'].remove_area('bsod')

def setup_item():
    pass
    game.context.states['adventure'].areas['bsod'].add(mock_item)

def teardown_item():
    pass
    game.context.states['adventure'].areas['bsod'].remove(mock_item)

def setup_enter_area():
    game.context.states['adventure'].enter_area('bsod')

def teardown_enter_area():
    game.context.states['adventure'].leave_area()

def test_screen():
    assert game.screen.get_size() == (800, 600)

def test_FPS():
    assert game.FPS == 60

@with_setup(setup_state, teardown_state)
@with_setup(setup_area, teardown_area)
@with_setup(setup_item, teardown_item)
def test_add_item():
    pass
    try:
        game.context.states['adventure'].areas['bsod'].get_element("teapot")
    except GetError:
        self.fail()

@with_setup(setup_state, teardown_state)
@with_setup(setup_area, teardown_area)
@with_setup(setup_enter_area, teardown_enter_area)
def test_enter_area():
    adventure = game.context.states['adventure']
    assert adventure.area.codename == 'bsod'

@with_setup(setup_state, teardown_state)
@with_setup(setup_area, teardown_area)
@with_setup(setup_enter_area, teardown_enter_area)
def test_enter_area_for_background():
    adventure = game.context.states['adventure']
    sprites = adventure.view.sprites()
    assert len(sprites) >= 1
    assert hasattr(sprites[0], 'codename')
    assert sprites[0].codename == 'bsod'
    assert sprites[0].image is not None

# fixtures per test
def setup_enter_state():
    game.context.enter_state('menu')

def teardown_enter_state():
    game.context.enter_state('adventure')

def setup_enter_incoming_state():
    game.context.set_incoming_state('menu')
    game.context.enter_incoming_state()

# effective tests
@with_setup(setup_state)
def test_first_state():
    gc = game.context
    assert gc.state == gc.states['adventure']

@with_setup(setup_state)
@with_setup(setup_enter_state, teardown_enter_state)
def test_enter_state():
    gc = game.context
    assert gc.state == gc.states['menu']

@with_setup(setup_state)
@raises(InputError)
def test_enter_wrong_state():
    game.context.enter_state('wrong_state')

@with_setup(setup_state)
@with_setup(setup_enter_incoming_state, teardown_enter_state)
def test_enter_incoming_state():
    game.context.set_incoming_state('menu')
    game.context.enter_incoming_state()
    gc = game.context
    assert gc.state == gc.states['menu']

