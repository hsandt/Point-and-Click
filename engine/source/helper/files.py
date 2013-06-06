# -*- coding: utf-8 -*-

import os

# on remonte de deux dossiers pour atteindre le dossier projet
MAIN_DIRECTORY = os.path.join(os.path.dirname(__file__), "..", "..", "test_resource")

def get_resource_path(*path):
    return os.path.join(MAIN_DIRECTORY, *path)

## only used in tests