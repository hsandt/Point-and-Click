# -*- coding: utf-8 -*-

import os

# on remonte de deux dossiers pour atteindre le dossier projet
MAIN_DIRECTORY = os.path.join(os.path.dirname(__file__), "..", "..")

def get_full_path(*path):
    return os.path.join(MAIN_DIRECTORY, *path)
