# -*- coding: utf-8 -*-

# source: docs.python.org/2/tutorial/errors.html


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(Error):
    """
    Exception raised for an incorrect input, independently from the current state of the game.

    Attributes:
        expr    -- input expression in which the error occured
        msg     -- explanation of the error

    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg


class GetError(Error):
    """
    Exception raised for an incorrect codename in a get call.

    Attributes:
        codename    -- incorrect codename
        msg         -- explanation of the error

    """

    def __init__(self, codename, msg):
        self.codename = codename
        self.msg = msg


class LoadError(Error):
    """
    Raised when an error occurs while trying to load a resource.

    Attributes:
        res_path    -- path of the resource that should have been loaded
        msg         -- explanation of the error

    """

    def __init__(self, res_path, msg):
        self.res_path = res_path
        self.msg = msg


class OverwriteError(Error):
    """
    Raised when trying to add an element with a pre-existing key in a dictionary.

    Attributes:
        codename    -- identifier that is repeated in the insert
        msg         -- explanation of the error

    """


class AbstractMethodError(Error):
    """
    Raised when trying to call an abstract method (that should have been overridden).

    Attributes:
        object_name     --  name of the object on which the method was called
        method_name     --  abstract method that was called

    """

    def __init__(self, object_name, method_name):
        self.object_name = object_name
        self.method_name = method_name
