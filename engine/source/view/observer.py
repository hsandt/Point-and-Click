# -*- coding: utf-8 -*-

from ..exception import AbstractMethodError


class Observer(object):
    """
    Observateur dans l'observer pattern (classe abstraite)

    """

    def __init__(self):
        pass

    def update(self):
        raise AbstractMethodError("update", self.__class__.__name__)
