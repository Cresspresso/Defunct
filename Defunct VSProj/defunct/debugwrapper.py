#region imports

import traceback
import os
from msvcrt import getch
import sys

#endregion
#region Internal

"""The working directory of the program.
(Constant)
"""
cl_directory = os.path.dirname(os.path.realpath(__file__))

#region Command-Line Arguments

#region Variables

"""Whether to display the "Press any key to continue . . . " prompt on program exit.
(Command Line Argument)
"""
cl_pauseOnExit = False

"""Whether to display 'dprint' calls to the console.
(Command Line Argument)
(Internal)
"""
cl_printdebug = False

"""Whether to display 'printinfo' calls to the console.
(Command Line Argument)
"""
cl_printinfo = False

#endregion
#region Argument Names

"""Sets __pauseOnExit__ to True"""
clargname_pauseOnExit = '-pauseOnExit'

"""Sets __printdebug__ to True"""
clargname_debugprint = '-debugInternal'

"""Sets __printinfo__ to True"""
clargname_printinfo = '-printinfo'


clargname_help = '-help'


valid_clargnames = [
	clargname_pauseOnExit,
	clargname_printinfo,
	clargname_debugprint,
	clargname_help,
]

#endregion

def HandleCoreCLArguments():
	"""Reads and handles the command-line arguments for core/internal parts of the program."""
	global cl_pauseOnExit
	global cl_printdebug
	global cl_printinfo

	# __pauseOnExit__
	try:
		cl_pauseOnExit = clargname_pauseOnExit in sys.argv
	#
	except:
		pass

	# __printdebug__
	try:
		cl_printdebug = clargname_debugprint in sys.argv
		dprint ('Internal Debugging enabled.')
	#
	except:
		pass

	# __printinfo__
	try:
		cl_printinfo = clargname_printinfo in sys.argv
	#
	except:
		pass
#

#endregion

def dprint (value, *args, sep=' ', end='\n', file=sys.stdout, flush=False):
	"""Calls print() only if __printdebug__ is true.
	(Internal)
	"""
	if cl_printdebug:
		print(value, *args, sep=sep, end=end, file=file, flush=flush)
#

def printinfo (value, *args, sep=' ', end='\n', file=sys.stdout, flush=False):
	"""Calls print() only if __printinfo__ is true."""
	if cl_printinfo:
		print(value, *args, sep=sep, end=end, file=file, flush=flush)
#


def formatExceptionStackTrace(e):
	"""Formats an exception message, making it easier to read than Python's default formatting.
	Arguments:
		e: Exception
	Returns:
		str
	(Internal)
	"""

	stack = traceback.extract_tb(e.__traceback__)
	formatted = []
	for filepath, lineno, module, line in stack:
		filename = filepath.replace(cl_directory, '..')
		formatted.append('  File "{0}", in {2},\n\t\t\t\t\t\tline {1},    {3}'.format(filename, lineno, module, line))
	#
	return '\n'.join(formatted)
#

def printException(e):
	"""Displays an exception message with optional stack trace.
	Arguments:
		e: Exception
	(Internal)

	First displays the error message and the final line where it occurred.
	Then waits for user to press a key:
		Spacebar      - displays stack trace with custom formatting.
		Escape        - displays stack trace with default formatting (by raising the exception).
		any other key - exits the program without showing a stack trace.
	"""

	print('\n\n InternalException (line {2}):\n {0}: {1}\n'.format(type(e).__name__, e, traceback.extract_tb(e.__traceback__)[-1][1]))

	print('Press SPACE for stack trace, or ESC for unformatted traceback ')
	keypress = ord(getch())
	if keypress == 32: # Space
		print(formatExceptionStackTrace(e))
		print('\n {0}: {1}\n'.format(type(e).__name__, e))
	#
	elif keypress == 27: # ESC
		raise e
	#
#

def doMain(func):
	"""Starts a program by its main/entry function.
		If any exceptions are raised, displays the exception message with optional stack trace.
	Arguments:
		func: callable() - the main/entry function to call
	Returns:
		value returned by the function
	(Internal)
	"""
	retval = None
	try:
		retval = func()
	except Exception as e:
		printException(e)
	print()

	if cl_pauseOnExit:
		print('Press any key to continue . . . ', end='', flush=True)
		getch()
		print()
	#

	return retval
#

#endregion


