# -*- coding: utf-8 -*-

from models import Element

class Prompter:
    def __init__(self):
        pass

    def prompt(self):
        action_string = raw_input("What do you want to do?\n")
        action_list = "take it".split()
        teapot = Element("teapot", "../test_resource/teapot.png", (15,30), (60,40)) # debug
        getattr(Element, "take")(teapot)

# test unitaire
if __name__ == '__main__':

    # prompt for action
    prompter = Prompter()
    prompter.prompt()