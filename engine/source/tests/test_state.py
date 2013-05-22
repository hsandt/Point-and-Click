# -*- coding: utf-8 -*-

from nose import with_setup

from state.game import PaCGame

def setup_module(module):
	module.game = PaCGame((800,600))
	game.context.enter_state('adventure')
	# game.context.states['adventure'].addArea()

def setup_enter_state():
	game.context.enter_state('menu')

def teardown_enter_state():
	game.context.enter_state('adventure')

def test_screen():
	assert game.screen.get_size() == (800, 600)

def test_FPS():
	assert game.FPS == 60

def test_init_state():
	gc = game.context
	assert gc.state == gc.states['adventure']

@with_setup(setup_enter_state, teardown_enter_state)
def test_enter_state():
	gc = game.context
	assert gc.state == gc.states['menu']

# def test_game_context_init():
# 	gc = game.context
# 	assert gc.state == gc.states['adventure']
