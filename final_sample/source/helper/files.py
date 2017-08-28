# -*- coding: utf-8 -*-

from os.path import dirname, join

__author__ = 'huulong'

# this module is located in final_sample/source/helper so the main directory is final_sample/
MAIN_DIRECTORY = dirname(dirname(dirname(__file__)))


def get_full_path(*path):
    return join(MAIN_DIRECTORY, *path)


# the resource folder is final_sample/sample_resource/
def get_resource_path(*path):
    return join(MAIN_DIRECTORY, "sample_resource", *path)
