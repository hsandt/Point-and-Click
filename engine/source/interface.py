# -*- coding: utf-8 -*-

from model import models
from helper.files import get_resource_path

class Prompter:
    """Interactive prompter (used before GUI appears)"""
    def __init__(self):
        pass

    def prompt(self):
        action_string = raw_input("What do you want to do?\n")
        action_list = "take it".split()
        teapot = models.Item("teapot", "some teapot", adv, None, get_resource_path("teapot.png"), (15, 30), get_resource_path("teapot.png"))
        getattr(Element, "take")(teapot)

# test unitaire
if __name__ == '__main__':
    """does not work with relative imports"""
    # prompt for action
    prompter = Prompter()
    prompter.prompt()