# -*- coding: utf-8 -*-
import unittest
from source.adventure.models import *

class TestArea(unittest.TestCase):

	def setUp(self):
		self.room = Area("blue screen of death", "background.png")
    	self.teapot = Element("teapot", "teapot.png", (15,30), (60,40)) # later an item

	def test_add(self):
		self.room.add(semf.teapot)
    	print room
    	# room.get_element('a teapot').take()
    	
    # def test_remove(self):

    # 	room.remove(teapot)
    # 	inventory = Inventory()
    # 	inventory.add(teapot)
    # 	print inventory
    # 	inventory.remove(teapot)

if __name__ == '__main__':
	unittest.main()