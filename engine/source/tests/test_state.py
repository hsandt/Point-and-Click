# -*- coding: utf-8 -*-

from nose import with_setup

from state.game import PaCGame

def setup_module(module):
	module.game = PaCGame((800,600))

def setup_game_context():
	game.context.enter_state('adventure')

def test_screen():
	assert game.screen.get_size() == (800, 600)

def test_FPS():
	assert game.FPS == 60

def test_game_context_init():
	gc = game.context
	assert gc.state == None and gc.incoming_state_name == None

@with_setup(setup_game_context)
def test_game_context_enter_state():
	gc = game.context
	assert gc.state == gc.states['adventure']

# def test_game_context_init():
# 	assert gc.state == gc.states['menu']

# def test_game_context_init():
	# assert gc.state == gc.states['menu']