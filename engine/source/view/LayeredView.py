# -*- coding: utf-8 -*-
import pygame

class LayeredView(pygame.sprite.LayeredUpdate):
	"""manage the different layers of the game, display or hide them when required"""
	def __init__(self):
		pygame.sprite.LayeredUpdate.__init__(self)
		pass

	def loadArea(self, int area):
		pass
		
	def clearMenuLayer(self):
		pass

	def fillMenuLayer(self):
		pass

	def displayText(pygame.Surface text):
		pass

	def clearText(self):
		pass

	def displayCursor(self):
		pass

	def hideCursor(self):
		pass


