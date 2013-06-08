# -*- coding: utf-8 -*-

# source: docs.python.org/2/tutorial/errors.html

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InputError(Error):
	"""
	Exception raised for errors in the input.

	Attributes:
		expr	-- input expression in which the error occured
		msg		-- explanation of the error

	"""

	def __init__(self, expr, msg):
		self.expr = expr
		self.msg = msg

class LoadError(Error):
	"""
	Raised when an error occurs while trying to load a resource.

	Attributes:
		res_name 	-- name of the resource that should have been loaded
		msg			-- explanation of the error
	
	"""

	def __init__(self, res_name, msg):
		self.res_name = res_name
		self.msg = msg

class OverwriteError(Error):
	"""
	Raised when trying to add an element with a pre-existing key in a dictionary.

	Attributes:
		codename 	-- identifier that is repeated in the insert
		msg			-- explanation of the error
	
	"""

	def __init__(self, codename, msg):
		self.codename = codename
		self.msg = msg