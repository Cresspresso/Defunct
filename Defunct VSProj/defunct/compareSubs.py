#region imports

from enum import Enum, Flag

from structs import *
from globalvars import *

#endregion
#region Comparing Expressions

def Identical(subA, subB):
	"""Compares two expressions to see if they are identical in value.
	Arguments:
		subA: Sub
		subB: Sub
	Returns:
		bool - true if subA is identical in value to subB
	"""
	#region private

	"""set of frozenset(Func, Func) - unique pairs of Funcs"""
	identicalFuncs = set()

	def Identical1(subA, subB):
		"""
		Arguments:
			subA: Sub
			subB: Sub
		Returns:
			bool - true if types are identical and content is identical
		Changes:
			identicalFuncs
		"""
		T = type(subA)

		if T != type(subB):
			return False
		#

		if T == Func:
			identicalFuncs.add( (subA, subB) )
			return Identical1(subA.body, subB.body)
		#
		elif T == ArgRef:
			# if Func pair exists, they are identical
			for pair in identicalFuncs:
				if (pair == (subA.func, subB.func)) or (pair == (subB.func, subA.func)):
					return True
			#
			return False
		#
		elif T == Bracket:
			return (Identical1(subA.left, subB.left)
			  and Identical1(subA.right, subB.right))
		#

		elif subA == None and subB == None:
			return True
		#
		else:
			raise Exception('should not get here')
	#

	#endregion
	#region body Identical
	identicalFuncs.clear()
	retval = Identical1(subA, subB)
	identicalFuncs.clear()
	return retval
	#endregion
#

#region global Definitions

def FindIdenticalDefs(sub):
	"""Finds definitions whose bodies are identical in value to this expression.
	Arguments:
		sub: Sub - the expression to compare with
	Returns:
		list(Def) - all definitions which are identical to this expression
	"""
	defs = []
	for dfn in definitions.values():
		if Identical(sub, dfn.body):
			defs.append(dfn)
	#
	return defs
#

#endregion

#endregion
#region CopySub

def CopySub(originalSub):
	"""Creates a deep copy of a Sub (used during substitution of references).
	Arguments:
		originalSub : Sub ref
	Returns:
		Sub - a deep copy of originalSub
	"""
	#region private

	"""dictionary of
	key		: Func ref - the original Func
	value	: Func ref - the new/copied Func
	"""
	newFuncs = {}

	def CopySub1(originalSub):
		"""
		Arguments:
			originalSub : Sub ref
		Returns:
			Sub - a deep copy of originalSub
		"""
		nonlocal newFuncs

		if type(originalSub) == Func:
			new = Func(
				argname=originalSub.argname,
				recursive=originalSub.recursive
				)
			newFuncs[originalSub] = new
			new.body = CopySub1(originalSub.body)
			del newFuncs[originalSub]
			return new
		#
		elif type(originalSub) == Bracket:
			return Bracket(
				left=CopySub1(originalSub.left),
				right=CopySub1(originalSub.right)
			)
		#
		elif type(originalSub) == ArgRef:
			if originalSub.func in newFuncs:
				return ArgRef(argname=originalSub.argname, func=newFuncs[originalSub.func])
			else:
				return ArgRef(argname=originalSub.argname, func=originalSub.func)
		#
		else:
			return originalSub
	#

	#endregion
	#region body CopySub
	newFuncs.clear()
	sub = CopySub1(originalSub)
	newFuncs.clear()
	return sub
	#endregion
#

#endregion
#region SubToString

class ArgnameDisplayMode(Flag):
	"""Represents how argument names should be formatted for printing.
	(Internal)
	"""

	"""Do not show any argument names"""
	Off = 0
	"""Show function locality (with 0 being most global)"""
	FuncLoc = 1
	"""Show argument name string"""
	ArgName = 2
	"""Show '$' in front to indicate recursiveness"""
	Recursiveness = 4

	All = FuncLoc | ArgName | Recursiveness
#
argnameDisplayMode = ArgnameDisplayMode.ArgName | ArgnameDisplayMode.Recursiveness


def SubToString(sub, top=None):
	"""Return a formatted string representation of an expression.
	Arguments:
		sub: Sub  - the expression to format
		top: Sub  - the most global expression to be considered FuncLoc 0
		     None - defaults to 'sub' parameter
	Returns:
		str
	"""
	if top == None:
		top = sub

	#region private

	"""dictionary of
	key: Func
	value: string - the locality of the function
					(e.g. 0 for most global, 1 for immediate nested child, 2 for child of child...)
	"""
	funcLocs = {}
	

	def InitFuncLocs(sub, order=0):
		"""Initializes function locality strings before expression formatting
		Arguments:
			sub:   Sub - the 'top'/most global expression node
			order: int - the locality of the current expression node
		Changes:
			funcLocs
		"""
		if not sub:
			return

		if type(sub) == Func:
			funcLocs[sub] = str(order)
			InitFuncLocs(sub.body, order + 1)

		elif type(sub) == Bracket:
			InitFuncLocs(sub.left, order)
			InitFuncLocs(sub.right, order)
	#

	def GetFuncLoc(func):
		"""Returns a string representing the locality of a function.
		Arguments:
			func: Func - the function to get the locality of
				  None - just return '?'
		Returns:
			str - the locality string of this function (e.g. '0', '1', '2'...)
			'?' - Func is None
			''  - flag ArgnameDisplayMode.FuncLoc is not set in argnameDisplayMode
		"""
		if func == None:
			return '?'
		if ArgnameDisplayMode.FuncLoc not in argnameDisplayMode:
			return ''
		try:
			return funcLocs[func]
		except:
			return '?'
	#

	def ArgnameToString(func, argname):
		"""Formats an argname based on function locality and argument name.
		Arguments:
			func: Func - the function with the referenced argument
			argname: str - the argument name (input from user code)
		Returns:
			str
		"""
		return "{0}{1}{2}".format(
				'$'  if (func != None and func.recursive) and (ArgnameDisplayMode.Recursiveness in argnameDisplayMode)  else '',
				GetFuncLoc(func),
				argname  if (ArgnameDisplayMode.ArgName in argnameDisplayMode)  else ''
			)
	#

	def FuncArgToString(func):
		return ArgnameToString(func, func.argname)
	#

	def FuncSeriesToString(func):
		"""Formats a series of functions into one function block string.
		Arguments:
			func: Func - the top function
		Returns:
			str
		"""
		argseries = FuncArgToString(func)
		func = func.body
		while type(func) == Func:
			argseries += ' ' + FuncArgToString(func)
			func = func.body
		#
		return "[{0}. {1}]".format(
			argseries,
			SubToString1(func)
		)
	#

	def SeriesToString(sub):
		"""Formats a series of Brackets into one string block. Removes parentheses as long as sub.left is a Bracket.
		Arguments:
			sub: Sub
		Returns:
			str
		e.g.
			((x y)z) -> 'x y z'
			(x(y z)) -> 'x(y z)'
		"""
		def LeftToString(sub):
			if type(sub) == Bracket:
				return SeriesToString(sub)
			else:
				return SubToString1(sub)
		#
		def RightToString(sub):
			if type(sub) == Bracket:
				return "({0})".format(SubToString1(sub))
			else:
				return " {0}".format(SubToString1(sub))
		#
		return LeftToString(sub.left) + RightToString(sub.right)
	#

	def SubToString1(sub):
		if not sub:
			return '<None>'
	
		if type(sub) == ArgRef:
			return ArgnameToString(sub.func, sub.argname)
		#
		elif type(sub) == Bracket:
			return SeriesToString(sub)

		elif type(sub) == Func:
			return FuncSeriesToString(sub)

		else:
			return '<Non-Sub>'
	#

	#endregion
	#region body SubToString
	funcLocs.clear()

	if ArgnameDisplayMode.FuncLoc in argnameDisplayMode:
		InitFuncLocs(top)
		retval = SubToString1(sub)
		funcLocs.clear()
		return retval
	#
	else:
		return SubToString1(sub)
	#endregion
#

#endregion


