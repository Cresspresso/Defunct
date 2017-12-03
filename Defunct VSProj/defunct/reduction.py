#region imports

from enum import Enum, Flag

from debugwrapper import dprint
from structs import *
from globalvars import *
import primitiveActions
from compareSubs import *

#endregion
#region Simplifying and Substituting

class SimplifyMode(Enum):
	"""Represents how an expression is being simplified."""

	"""Simplify this expression and any sub-expressions. If a recursive expression is encountered, change to SimplifyMode.ApplyRecursive."""
	Normal = 0
	
	"""Apply a recursive function, then simplify using SimplifyMode.DoneRecursive."""
	ApplyRecursive = 1
	
	"""Simplify this expression and any sub-expressions, but do not simplify recursive expressions."""
	DoneRecursive = 2
#

def Simplify(sub, execute=False, simplifyMode=SimplifyMode.Normal):
	"""Simplifies an expression node and any sub-expressions.
	Arguments:
		sub: Sub - the expression to simplify
		exectue: bool - if true, will execute primitive functions like 'print'
		simplifyMode: SimplifyMode
			.Normal - simplify this expression and any sub-expressions
			.DoneRecursive - simplify this expression and any sub-expressions, but not recursive expressions
	Returns:
		Sub - the expression which is as simplified as possible
	"""
	#region private SimplifyBracket

	def SimplifyBracket(sub, execute=False, simplifyMode=SimplifyMode.Normal):
		"""Simplifies both sides of the expression, then attempts to apply the function 'left' to the expression 'right'.
		Arguments:
			sub: Bracket - the expression to simplify
			exectue: bool - if true, will execute primitive functions like 'print'
			simplifyMode: SimplifyMode
				.Normal - simplify this expression and any sub-expressions
				.DoneRecursive - simplify this expression and any sub-expressions, but not recursive expressions
		Returns:
			Sub - the simplified expression
		"""
		#region private Apply

		def SimplifyBracket_Apply(sub, execute=False, simplifyMode=SimplifyMode.Normal):
			"""Applies 'left' Func to 'right' expression. Substitutes all references to the function's argument with 'right'.
			Arguments:
				sub: Bracket - the expression to simplify
					sub.left: Func - the function to apply
					sub.right: Sub - the expression to substitute in
				exectue: bool - if true, will execute primitive functions like 'print'
				simplifyMode: SimplifyMode
					.Normal, .DoneRecursive - simplify this expression and any sub-expressions
					.ApplyRecursive - simplify this recursive expression but not any further recursions
			Returns:
				Sub - the simplified expression
			"""
			#region private  Substitution of Arguments and Primitive References

			def SubstituteArg(sub, referredSub, func):
				"""Replaces all references to a specific function's argument within a Sub with deep copies of the referred Sub.
				Arguments:
					sub			: Sub  - the current Sub being checked
					referredSub : Sub  - the Sub to deep copy and replace the references
					func		: Func - the function with the argument being checked
				Returns:
					Sub - the 'sub' parameter with all references replaced
				"""
				if not sub:
					return sub
				if not func:
					raise ValueError('func null')
				if type(func) != Func:
					raise TypeError('func not a Func')


				if type(sub) == ArgRef:
					if sub.func == func:
						return CopySub(referredSub)
					else:
						return sub
				#
				elif type(sub) == Func:
					sub.body = SubstituteArg(sub.body, referredSub, func)
					return sub
				#
				elif type(sub) == Bracket:
					sub.left = SubstituteArg(sub.left, referredSub, func)
					sub.right = SubstituteArg(sub.right, referredSub, func)
					return sub
				#
				else:
					return sub
			#

			def ExecuteRef(sub):
				"""Executes a primitive built-in function.
				Arguments:
					sub: Bracket - the Bracket with a possible primitive function being applied
						sub.left: ArgRef - the reference to a possibly primitive function
				Returns:
					Func - Identity function   | sub.left was a primitive function
					Sub  - the 'sub' parameter | sub.left was not a primitive function
				"""
				if type(sub) != Bracket:
					raise TypeError('sub not a Bracket')
				if type(sub.left) != ArgRef:
					raise TypeError('sub.left not an ArgRef')

				if sub.left.argname in primitiveActions.names:
					return primitiveActions.names[sub.left.argname](sub.right)
				else:
					return sub
			#

			#endregion
			#region body SimplifyBracket_Apply
			if not sub:
				raise ValueError('sub null')
			if type(sub) != Bracket:
				raise TypeError('sub not a Bracket')
			if not sub.left:
				return sub
	
			if type(sub.left) == Func:
				new = SubstituteArg(sub.left.body, sub.right, sub.left)

				if simplifyMode == SimplifyMode.ApplyRecursive:
					new = Simplify(new, execute, SimplifyMode.DoneRecursive)
				else:
					new = Simplify(new, execute, simplifyMode)

				return new
			#
			elif type(sub.left) == ArgRef:
				if execute:
					return ExecuteRef(sub)
			#

			return sub
			#endregion
		#

		#endregion
		#region body SimplifyBracket
		if not sub:
			raise ValueError('sub null')
		if type(sub) != Bracket:
			raise TypeError('sub not a Bracket')
		if not sub.left:
			return sub

		# Simplify both sub-expressions
		sub.left  = Simplify(sub.left,  execute, simplifyMode)
		sub.right = Simplify(sub.right, execute, simplifyMode)
	
		# Apply left func to right expression
		if simplifyMode == SimplifyMode.Normal:
			if sub.left.recursive:

				def check():
					return (type(sub) == Bracket and sub.left.recursive
					and ((type(sub.left) == Bracket and type(sub.left.left) != ArgRef) or (type(sub.left) == Func)))
				#
				if not sub.right.recursive and check():
					while check():
						if type(sub.left) == Bracket:
							sub.left = SimplifyBracket_Apply(sub.left, execute, SimplifyMode.ApplyRecursive)
						elif type(sub.left) == Func:
							sub = SimplifyBracket_Apply(sub, execute, SimplifyMode.ApplyRecursive)
					#
					sub = SimplifyBracket_Apply(sub, execute, SimplifyMode.DoneRecursive)
					sub = Simplify(sub, execute, SimplifyMode.Normal)
				#
			#
			elif not sub.left.recursive:
				sub = SimplifyBracket_Apply(sub, execute, simplifyMode)
		#
		elif simplifyMode == SimplifyMode.DoneRecursive:
			if not sub.left.recursive:
				sub = SimplifyBracket_Apply(sub, execute, simplifyMode)
		#

		return sub
		#endregion
	#

	#endregion
	#region body Simplify
	if type(sub) == Bracket:
		sub = SimplifyBracket(sub, execute, simplifyMode)
	#
	elif type(sub) == Func:
		sub.body = Simplify(sub.body, execute, simplifyMode)
	#
	elif type(sub) == ArgRef:
		if sub.func == None and sub.argname in definitions:
			sub = CopySub(definitions[sub.argname].body)
			sub = Simplify(sub, execute, simplifyMode)
		#
	#
	return sub
	#endregion
#

#endregion


