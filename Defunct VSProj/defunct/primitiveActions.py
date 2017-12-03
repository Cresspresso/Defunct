#region imports

from extensions import joinObjects
from compareSubs import *
import primitiveExpressions

#endregion
#region Constants

"""List of all valid primitive names and their associated functions"""
names = {
	# Print an expression to the console.
	#   print <expression>    -> identity
	#
	'print': lambda x: Execute_Print(x),

	# Print an expression to the console. Flush buffer and display immediately.
	#   print_flush <expression>    -> identity
	#
	'print_flush': lambda x: Execute_Print(x, True),
}

#endregion
#region Actions

def Execute_Print(sub, flush=False):
	"""Prints an expression to the console, along with any aliases (names of definitions with identical body).
	Arguments:
		sub: Sub - the expression to print
		flush: bool - passed in to python 'print' function
	Returns:
		Func - Identity primitive
	"""
	defs = FindIdenticalDefs(sub)
	msg = ''
	if len(defs) > 0:
		msg += joinObjects(', ', lambda d: d.name, defs) + ' :  '
	msg += SubToString(sub)
	print (msg, flush=flush)
	return primitiveExpressions.identity()
#

#endregion


