# -*- coding: utf-8 -*-

class InputException(Exception)
	"""docs.python.org/2/tutorial/errors.html
	Exception raised for errors in the input.

	Attributes:
		expr	-- input expression in which the error occured
		msg		-- explanation of the error

	"""

	def __init__(self, expr, msg):
		self.expr = expr
		self.msg = msg

# class TransitionError()