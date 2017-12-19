#region imports

from debugwrapper import dprint
from globalvars import currentHierarchy

#endregion
#region Exceptions

class DefunctError(Exception):
	"""An error was encountered during interpretation."""
	def __init__(this, message):
		"""
		Arguments:
			message : str
		"""
		super().__init__(message)
#

class DefunctError_InputError(DefunctError):
	"""An error was encountered while reading the input file."""
	def __init__(this, message, location):
		"""
		Arguments:
			message	 : str
			location : (int, int) - where the error was found in the file (line number and column number)
		"""
		super().__init__(message)
		this.location = location
#

#endregion
#region Defunct Expressions

"""NOTE:
Sub is a nonexistent base class of Bracket, Func, and ArgRef.
It represents what I call an expression node of Lambda Calculus.
"""

class Bracket:
	"""Represents an expression node where a Lambda Calculus Function (left) is being applied to another Sub (right).
	(Sub)
	"""
	def __init__(this, left=None, right=None):
		"""
		Arguments:
			left  : Sub ref - the Sub to apply to 'right'
			right : Sub ref - the Sub to pass in as a parameter to 'left'
		"""
		this.left = left
		this.right = right
	#
		
	@property
	def recursive(this):
		"""Whether this Bracket can be considered recursive.
		Returns:
			bool
		"""
		return this.left == None or this.right == None or (this.left.recursive and this.right.recursive)
	#

	@property
	def containsRecursive(this):
		"""Whether this Bracket contains a recursive Sub.
		Returns:
			bool
		"""
		return this.left.containsRecursive or this.right.containsRecursive
	#
#
class Func:
	"""Represents a Lambda Calculus Function which can be applied to another Sub.
	(Sub)
	"""
	def __init__(this, argname='', body=None, recursive=False):
		"""Arguments:
			argname		: str - this function's argument name
			body		: Sub ref - the top expression node contained within this function
			recursive	: bool - whether this function can be considered recursive.
		"""
		this.argname = argname
		this.body = body
		this.recursive = recursive
	#
	
	@property
	def containsRecursive(this):
		"""Whether this Func contains a recursive Sub.
		Returns:
			bool
		"""
		return this.recursive or this.body.containsRecursive
	#
#
class ArgRef:
	"""Represents a reference to either a function argument or a definition.
	(Sub)
	"""
	def __init__(this, argname='', func=None):
		"""
		Arguments:
			argname : str - the referenced Func argument name or Definition name.
			func	: Func ref - the referenced Func ('None' if not yet linked or referencing a Definition)
		"""
		this.argname = argname
		this.func = func
	#
	
	@property
	def recursive(this):
		"""Whether this ArgRef can be considered recursive.
		Returns:
			bool
		"""
		return this.func != None and this.func.recursive
	#
	
	@property
	def containsRecursive(this):
		"""Whether this ArgRef contains a recursive Sub.
		Returns:
			bool
		"""
		return this.recursive or this.func in currentHierarchy
	#
#


class Def:
	"""Represents a Definition, binding an expression to a name which can be referenced."""
	def __init__(this, name='', body=None):
		"""
		Arguments:
			name : str - the name which represents this expression
			body : Sub ref - the top expression node contained within this definition
		"""
		this.name = name
		this.body = body
	#

	def __contains__(this, item):
		if typeof(item) == Def and item == this:
			return True
		return this.body.__contains__(item)
	#
#

#endregion


