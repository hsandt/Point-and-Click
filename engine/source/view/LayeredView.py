# -*- coding: utf-8 -*-
import pygame

class LayeredView(pygame.sprite.LayeredUpdates):
	"""manage the different layers of the game, display or hide them when required"""
	def __init__(self):
		pygame.sprite.LayeredUpdates.__init__(self)
		pass

	def loadArea(self, area):
		pass
		
	def clearMenuLayer(self):
		pass

	def fillMenuLayer(self):
		pass

	def displayText(text):
		pass

	def clearText(self):
		pass

	def displayCursor(self):
		pass

	def hideCursor(self):
		pass


