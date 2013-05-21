# -*- coding: utf-8 -*-

from state.gamecontext import GameContext

def setup_module(module):
	module.gc = GameContext()

def test_game_context_init():
	assert gc.state == gc.states['menu']