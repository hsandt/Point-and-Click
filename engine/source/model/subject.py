# -*- coding: utf-8 -*-

class Subject(object):
    """
    Sujet dans l'observer pattern (classe abstraite)

    On fonctionne sur une association subject [1]--[0..*] observer
    Nous n'utilisons pas de mapping ni de médiateur.
    Nous ne précisons pas le sujet modifié dans la requête d'update car il est unique par observateur.
    Les notifications se font aux niveaux les plus bas (setter), à moins que plusieurs modificiations simultanées aient lieu

    Attributs :
        observer_list   -- liste des observateurs

    """
    def __init__(self):
        self.observer_list = []

    def attach(self, observer):
        self.observer_list.append(observer)

    def detach(self, observer):
        self.observer_list.remove(observer)

    def notify(self):
        for observer in self.observer_list:
            observer.update()
