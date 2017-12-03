"""
Defunct Interpreter
by Elijah John Shadbolt (Cresspresso)
Copyright (c) 2017    MIT Licence

Version 1.04
2017-11-24 19:26:22 +1300


___Quick-Start___

In the console, cd to the directory containing Defunct.exe and run this command:

Defunct "examples\example01.txt"


___Descrption___

This is an interpeter (written in Python) for Defunct code.

Defunct is a simplistic programming language based on pure Lambda Calculus.
It is terribly inefficient and slow, but it relies solely on the principles
of raw Lambda Calculus. Expressions of functions can be defined, referenced,
simplified, substituted, and executed.

This interpreter works by creating Function, Bracket, and Reference objects
in no particular place in memory, all referencing each other to create a
syntax tree, which is then evaluated at runtime. References are linked and
substituted during simplification of an expression.

Defunct is a non-typed language. There are some functions that are not pure
Lambda Calculus which are called commands, but they always return Lambda
Calculus functions (usually the identity function). An example is the command
'print', which prints an expression to the console.

It is very inefficient because all code data is made up of many python
objects, and there are no optimised primitive types such as Integer or Float.


___Examples___

Some examples of working code can be found in the 'examples' folder included
with this package.


___Command-Line Arguments___

Usage:
    <filepath> [options]


    <filepath>: string
        Specifies the .txt file to interpret.

    -printinfo
        Display log text in the console, such as which file is being read.

    -pauseOnExit
        Shows the prompt "Press any key to continue . . . " when the program is
        exited.

    -debugInternal
        (Internal, not for public use)
        Displays debugging text (useful when developing the internal code).

Usage:
    -help
    -help about
    -help licence


___Licence___

MIT License

Copyright (c) 2017 Elijah John Shadbolt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE


"""
#region Help Text

__help_clargs = """Defunct Interpreter
by Elijah John Shadbolt (Cresspresso)
Copyright (c) 2017    MIT Licence

Version 1.04
2017-11-24 19:26:22 +1300

Usage:
    <filepath> [options]


    <filepath>: string
        Specifies the .txt file to interpret.

    -printinfo
        Display log text in the console, such as which file is being read.

    -pauseOnExit
        Shows the prompt "Press any key to continue . . . " when the program is
        exited.

    -debugInternal
        (Internal, not for public use)
        Displays debugging text (useful when developing the internal code).

Usage:
    -help
    -help about
    -help licence
"""

__help_about = """Defunct Interpreter

This is an interpeter (written in Python) for Defunct code.

Defunct is a simplistic programming language based on pure Lambda Calculus.
It is terribly inefficient and slow, but it relies solely on the principles
of raw Lambda Calculus. Expressions of functions can be defined, referenced,
simplified, substituted, and executed.

This interpreter works by creating Function, Bracket, and Reference objects
in no particular place in memory, all referencing each other to create a
syntax tree, which is then evaluated at runtime. References are linked and
substituted during simplification of an expression.

Defunct is a non-typed language. There are some functions that are not pure
Lambda Calculus which are called commands, but they always return Lambda
Calculus functions (usually the identity function). An example is the command
'print', which prints an expression to the console.

It is very inefficient because all code data is made up of many python
objects, and there are no optimised primitive types such as Integer or Float.
"""

__help_licence = """Product/Service: Defunct Interpreter

MIT License

Copyright (c) 2017 Elijah John Shadbolt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE
"""

#endregion
#region Imports

import traceback
import os
from msvcrt import getch
import sys


from enum import Flag, Enum

#endregion
#region Internal

"""The working directory of the program.
(Constant)
"""
__directory__ = os.path.dirname(os.path.realpath(__file__))

#region Command-Line Arguments

#region Variables

"""Whether to display the "Press any key to continue . . . " prompt on program exit.
(Command Line Argument)
"""
__pauseOnExit__ = False

"""Whether to display 'dprint' calls to the console.
(Command Line Argument)
(Internal)
"""
__printdebug__ = False

"""Whether to display 'printinfo' calls to the console.
(Command Line Argument)
"""
__printinfo__ = False

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
	global __pauseOnExit__
	global __printdebug__
	global __printinfo__

	# __pauseOnExit__
	try:
		__pauseOnExit__ = clargname_pauseOnExit in sys.argv
	#
	except:
		pass

	# __printdebug__
	try:
		__printdebug__ = clargname_debugprint in sys.argv
		dprint ('Internal Debugging enabled.')
	#
	except:
		pass

	# __printinfo__
	try:
		__printinfo__ = clargname_printinfo in sys.argv
	#
	except:
		pass
#

#endregion

def dprint (value, *args, sep=' ', end='\n', file=sys.stdout, flush=False):
	"""Calls print() only if __printdebug__ is true.
	(Internal)
	"""
	if __printdebug__:
		print(value, *args, sep=sep, end=end, file=file, flush=flush)
#

def printinfo (value, *args, sep=' ', end='\n', file=sys.stdout, flush=False):
	"""Calls print() only if __printinfo__ is true."""
	if __printinfo__:
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
		filename = filepath.replace(__directory__, '..')
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
		HandleCLArguments()
		retval = func()
	except Exception as e:
		printException(e)
	print()

	if __pauseOnExit__:
		print('Press any key to continue . . . ', end='', flush=True)
		getch()
		print()
	#

	return retval
#

#endregion
#region General Python Extensions

def joinitems(separator, selector, items):
	"""Joins a string of items by calling the selector with each item and putting the separator in between each item.
	Arguments:
		separator : str - string to put between each item
		selector : callable(item) - function with one parameter
		items : list - the items to join
	Returns:
		str
	Examples:
		>>> joinitems(', ', lambda x: x + 1, [0, 5, 2])
		'1, 6, 3'
	"""
	if type(separator) != str:
		raise TypeError('type(separator) should be str.')
	if type(items) != list:
		raise TypeError('type(items) should be list.')

	retval = ''
	if len(items) > 0:
		last = items.pop()
		for item in items:
			retval += str(selector(item)) + separator
		#
		retval += str(selector(last))
	return retval
#

def appendIfTruthy(lst, item):
	"""Appends an item to a list only if that item exists or is considered truthy (not None, not '', etc)."""
	if item:
		lst.append(item)
#

#endregion
#region Command-Line Arguments

#"""Sets clarg_filepath to <filepath>
#	-f <filepath>
#"""
#clargname_filepath = '-f'

"""str - the file to interpret"""
clarg_filepath = None


def programCanStart(): return clarg_filepath != None #


#region Help

help_types = {
	'about': __help_about,
	'licence': __help_licence,
}

def PrintHelp():
	"""Handles the '-help' command-line argument and prints help text to the console."""
	if clargname_help in sys.argv:
		helptype = None
		try:
			helptype = sys.argv[sys.argv.index(clargname_help) + 1]
		except:
			pass

		if helptype in help_types:
			print(help_types[helptype])
		else:
			print(__help_clargs)
	#
	else:
		print(__help_clargs)
#

#endregion

def HandleCLArguments():
	"""Reads and handles the command-line arguments."""
	global clarg_filepath

	# filepath
	try:
		firstarg = sys.argv[1]
		if firstarg not in valid_clargnames:
			clarg_filepath = firstarg
		#clarg_filepath = sys.argv[sys.argv.index(clargname_filepath) + 1]
	except:
		pass

	# handle core command-line arguments, or print help text
	if programCanStart():
		HandleCoreCLArguments()
	else:
		PrintHelp()
#

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
#region Structs

"""
Note: 'Sub' is a nonexistent base class of Bracket, Func, and ArgRef.
Sub represents what I call an expression node of Lambda Calculus.
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

	@property
	def recursive(this):
		"""Whether this Bracket can be considered recursive.
		Returns:
			bool
		"""
		return this.left == None or this.right == None or (this.left.recursive and this.right.recursive)
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

	@property
	def recursive(this):
		"""Whether this ArgRef can be considered recursive.
		Returns:
			bool
		"""
		return this.func != None and this.func.recursive
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

#endregion
#region Simplifying and Substituting

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

#region Simplify

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

				if sub.left.argname == primitiveName_Print:
					return Execute_Print(sub.right)
				elif sub.left.argname == primitiveName_PrintFlush:
					return Execute_Print(sub.right, flush=True)

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

#endregion
#region Printing

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

#endregion
#region Keywords

"""Create a Definition.
	def <name> <body>
"""
keyword_Define = 'def'

"""Create an unsimplified Definition.
	def_u <name> <body>
"""
keyword_DefineUnsimplified = 'def_u'

"""Simplify an expression and execute all primitive functions
	do <expression>
"""
keyword_Execute = 'do'


"""List of all valid Entry-level keywords"""
Keywords = [keyword_Define, keyword_DefineUnsimplified, keyword_Execute]

#endregion
#region Primitive Names

"""Print an expression to the console.
	print <expression>    -> identity
"""
primitiveName_Print = 'print'

"""Print an expression to the console. Flush buffer and display immediately.
	print_flush <expression>    -> identity
"""
primitiveName_PrintFlush = 'print_flush'


"""List of all valid primitive names"""
PrimitiveNames = [primitiveName_Print, primitiveName_PrintFlush]

#endregion
#region Primitives

def Primitive_Identity():
	"""(Primitive Function) Takes 1 argument. Returns that argument."""
	sub = Func('x', ArgRef('x'))
	sub.body.func = sub
	return sub
#

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
		msg += joinitems(', ', lambda d: d.name, defs) + ' :  '
	msg += SubToString(sub)
	print (msg, flush=flush)
	return Primitive_Identity()
#

#endregion
#region Interpreter
"""Note: Most functions within this #region use the variable 'char'. Some use 'file' and 'location'."""

"""The file to read input from"""
file = None

"""The current character being read from the file"""
char = ''

"""The location of the current character in the file.
Tuple of (int, int): (line number, column number)
"""
location = (1,1)


def getchar():
	"""Gets the next character from the input file and stores it in 'char'."""
	global char
	global location

	char = file.read(1)

	if char == '\n':
		location = (location[0] + 1, 1)
	else:
		location = (location[0], location[1] + 1)
#

#region Character Recognition
"""Functions and variables for recognising what kind of character/token is being read at the moment."""

chars_whitespace = ' \t\r\n'

char_CommentStart = '/'
char_CommentSingle = '/'
char_CommentMultiline = '*'

char_BracketStart = '('
char_BracketEnd = ')'

char_FuncStart = '['
char_FuncEnd = ']'
char_FuncArgumentEnd = '.'

char_Recursive = '$'

chars_NotIdentifier = (
	chars_whitespace
	+ char_BracketStart + char_BracketEnd
	+ char_FuncStart + char_FuncEnd + char_FuncArgumentEnd
	)

"""Functions that return bool - whether current character is a certain type of character"""
def ischar_whitespace(char):		return char  and  char in chars_whitespace #
def ischar_CommentStart(char):		return char == char_CommentStart #
def ischar_BracketStart(char):		return char == char_BracketStart #
def ischar_BracketEnd(char):		return not char  or  char == char_BracketEnd  or  char == char_FuncEnd #
def ischar_FuncStart(char):			return char == char_FuncStart #
def ischar_FuncEnd(char):			return not char  or  char == char_FuncEnd #
def ischar_FuncArgumentEnd(char):	return char == char_FuncArgumentEnd #
def ischar_Identifier(char):		return char  and  char not in chars_NotIdentifier #

#endregion
#region Do... Functions

#region DoComments

def DoCommentSingle():
	"""Single-line comment. Reads all characters until endline '\n' is found.
	Returns:
		str - the comment's content
	Input Example:
		//comment
	"""
	retval = ''
	while char and char != '\n':
		retval += char
		getchar()
	return retval
#

def DoCommentMultiline():
	"""Multiline comment. Reads all characters until character sequence '*/' is found.
	Returns:
		str - the comment's content
	Input Example:
		/*comment*/
	"""
	retval = ''
	while char:
		if char == char_CommentMultiline:
			getchar()
			if char == char_CommentStart:
				getchar()
				return retval
			else:
				retval += char
				getchar()
		#
		else:
			retval += char
			getchar()
	#
	return retval
#

def DoComment():
	"""Checks if a comment is starting, and retrieves the comment. If no comment is starting, restore current location in file.
	Assumes:
		char == char_CommentStart
	Returns:
		str  - the comment
		None - no comment was starting
	Input Examples:
		//comment
		/*comment*/
	"""
	global location

	# store location
	oldposition = file.tell()
	oldlocation = location

	getchar()
	if char == char_CommentSingle:
		getchar()
		return DoCommentSingle()
	#
	elif char == char_CommentMultiline:
		getchar()
		return DoCommentMultiline()
	#
	else:
		#restore location
		file.seek(oldposition)
		location = oldlocation
		#return None
#

#endregion
#region Cradle

def skipwhite():
	"""Skips characters until a non-whitespace character is found. Retrieves any comments along the way.
	Returns:
		list(str) - list of comments
	"""
	comments = []
	if ischar_CommentStart(char):
		appendIfTruthy(comments, DoComment())
	#
	while ischar_whitespace(char):
		getchar()
		if ischar_CommentStart(char):
			appendIfTruthy(comments, DoComment())
		#
	#
	return comments
#

def match(s):
	"""Matches the next string of characters (throws an error if string was not correct), then skips whitespace.
	Arguments:
		s: str - the expected string of characters
	Returns:
		list(str) - list of comments
	Exceptions:
		DefunctInputError - the sequence of characters was not expected.
	"""
	for c in s:
		if char != c:
			raise DefunctError_InputError("Expected '{0}', got '{1}'.".format(s, char), location)
		getchar()
	#
	return skipwhite()
#

#endregion
#region DoIdentifiers

def DoIdentifier():
	"""Does an identifier name (e.g. argument name, definition name, reference name)
	Returns:
		str - the identifier/name
	"""
	if not ischar_Identifier(char):
		raise DefunctError_InputError("Expected identifier, got '{0}'.".format(char), location)

	retval = char
	getchar()
	while ischar_Identifier(char):
		if ischar_CommentStart(char):
			DoComment()
			break
		#else
		retval += char
		getchar()
	#
	skipwhite()
	return retval
#

def DoKeyword():
	name = DoIdentifier()
	if name not in Keywords:
		raise DefunctError_InputError("Expected keyword, got '{0}'".format(name), location)
	return name
#
def DoName():
	name = DoIdentifier()
	if name in Keywords and not name in PrimitiveNames:
		raise DefunctError_InputError("Expected identifier, got keyword '{0}'".format(name), location)
	return name
#
def DoFuncArgname():
	name = DoName()
	if name in PrimitiveNames:
		raise DefunctError_InputError("Function Argument cannot have primitive name '{0}'".format(name), location)
	return name
#
def DoDefName():
	name = DoIdentifier()
	if name in Keywords:
		raise DefunctError_InputError("Expected identifier, got keyword '{0}'".format(name), location)
	elif name in PrimitiveNames:
		raise DefunctError_InputError("Expected identifier, got primitive '{0}'".format(name), location)
	return name
#

#endregion

def DoRef():
	"""Does an argument/definition reference by name.
	Returns:
		ArgRef
	"""
	return ArgRef(argname=DoName())
#

#region DoFunc

def LinkArgRefs(sub, func):
	"""Makes sure local ArgRefs with same name as func.argname are linked to that Func.
	Arguments:
		sub: Sub - the current expression node
		func: Func - the function to link references to
	"""
	if sub == None or func == None:
		return

	if type(sub) == ArgRef:
		if sub.func == None and sub.argname == func.argname:
			sub.func = func

	elif type(sub) == Func:
		LinkArgRefs(sub.body, func)

	elif type(sub) == Bracket:
		LinkArgRefs(sub.left, func)
		LinkArgRefs(sub.right, func)
#

def DoFuncArg():
	"""Creates a new function with its argname and recursiveness, but not its body.
	Returns:
		Func - the newly created function
	"""
	func = Func()

	if char == char_Recursive:
		match(char_Recursive)
		func.recursive = True
	#

	func.argname = DoFuncArgname()

	return func
#

def DoFuncSeries():
	"""Does a series of functions inside a function definition bracket set (like a function with multiple arguments).
	Returns:
		Func - the top Func, possibly the start of many Funcs
	Input Examples:
		[x. (...) ]
		[x y z. (...) ]
	"""
	match(char_FuncStart)

	# creating Funcs
	topfunc = DoFuncArg()
	funcs = [ topfunc ]
	endfunc = topfunc

	while not ischar_FuncArgumentEnd(char):
		func = DoFuncArg()
		endfunc.body = func

		funcs.append(func)
		endfunc = func
	#
	if char:
		match(char_FuncArgumentEnd)

	# getting body
	endfunc.body = DoSeries()
	
	# linking ArgRefs
	for func in reversed(funcs):
		LinkArgRefs(func.body, func)
	#

	if char:
		match(char_FuncEnd)

	return topfunc
#

#endregion
#region DoSeries

def DoSeries():
	"""Does a series of expressions
	Returns:
		Sub - a single expression (there were no further expressions)
		Bracket - top of series of expressions
	Input Examples:
		x				-> x
		x y z			-> ((x y)z)
		x(y z)			-> (x(y z))
		()				-> [x.x]
	"""
	if ischar_BracketEnd(char):
		return Primitive_Identity()

	retval = DoSub()
	while not ischar_BracketEnd(char):
		retval = Bracket(
			left=retval,
			right=DoSub()
			)
	#
	return retval
#

def DoBracketedSeries():
	"""Does a series of expressions contained within parentheses.
	Returns:
		Sub - a single expression
		Brackte - top of series of expressions
	Input Examples:
		x				-> x
		x y z			-> ((x y)z)
		x(y z)			-> (x(y z))
		()				-> [x.x]
	"""
	match(char_BracketStart)
	retval = DoSeries()
	if char:
		match(char_BracketEnd)
	return retval
#

#endregion

def DoSub():
	"""Does an expression and any sub-expressions.
	Returns:
		Sub - an expression node
	"""

	if ischar_BracketStart(char):
		return DoBracketedSeries()

	elif ischar_FuncStart(char):
		return DoFuncSeries()

	elif ischar_Identifier(char):
		return DoRef()
#

#region DoDef

def DoDef(simplify = True):
	"""Does a definition with an expression bound to a name which can later be referenced.
	Arguments:
		simplify: bool - should the retrieved input expression be simplified before storing?
	Changes:
		definitions
	Returns:
		None
	Input Examples:
		def   myFunc ([a.a][x y.y x])			// [x y. y x] is bound to myFunc
		def_u myExpr ([a.a][a b.b a])			// ([a.a][a b.b a]) is bound to myExpr
		def   myRef myFunc						// [x y. y x]
		def_u myRefu myFunc						// ?myFunc
		def   myUnknown unknown					// ?unknown
		def myExpr [a.a[x.x]]					// myExpr is now [a.a[x.x]], no longer ([a.a][a b.b a])
	"""
	global definitions
	
	name = DoDefName()

	#if name in definitions:
	#	raise DefunctError("Def with name '{0}' already exists.".format(name))

	dfn = Def(
		name=name,
		body=DoSub()
		)

	definitions[name] = dfn
	
	#dprint ("{0}   initially  {1}".format(name, SubToString(dfn.body, dfn.body)))

	if simplify:
		dfn.body = Simplify(dfn.body, execute=False)
		#dprint ("{0}   finally    {1}".format(dfn.name, SubToString(dfn.body, dfn.body)))

		#for d in FindIdenticalDefs(dfn.body):
		#	if d.name != dfn.name:
		#		dprint("\tIdentical to '{0}'".format(d.name))
		#
	#
#

#endregion

def DoEntry():
	"""Does a series of definitions and executions.
	Returns:
		None
	"""
	while char:
		key = DoKeyword()

		if key == keyword_Define:
			DoDef()
		#
		elif key == keyword_DefineUnsimplified:
			DoDef(simplify=False)
		#
		elif key == keyword_Execute:
			sub = DoSub()
			#dprint ('EXECUTE    ' + SubToString(sub, sub))
			sub = Simplify(sub, execute=True)
			#dprint ('Finally    ' + SubToString(sub, sub))
		#
	#
#

#endregion
#region global Definitions

"""dictionary of
	key: str - name of the definition
	value: Def - the definition
"""
definitions = {}

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
#region Entry

def InterpretFile(filepath):
	"""Opens a file and begins interpretation.
	Arguments:
		filepath: str - the file to open
	Exceptions:
		DefunctError:FileNotFoundError - no file was found at <filepath>
	"""
	global file

	try:
		printinfo ('Interpreting file at "{0}"...'.format(filepath))
		with open(filepath, 'r') as file:
			getchar()
			skipwhite()
			DoEntry()
		#
		printinfo ('Finished interpreting file at "{0}".'.format(filepath))
	except FileNotFoundError as e:
		raise DefunctError('File not found at "{0}"'.format(filepath)) from e
	#
#

#endregion

#endregion
#region MAIN

def main():
	"""The main entry point for the Defunct Interpreter."""
	if programCanStart():
		try:
			InterpretFile(clarg_filepath)
			printinfo('No errors encountered.')
		#
		except DefunctError_InputError as e:
			print("\n{0} (line {2}): {1}\n(line {2}, column {3})".format(
				'InputError',
				e,
				e.location[0],
				e.location[1]
			))
			if __printdebug__:
				raise e
		#
		except DefunctError as e:
			print("\n{0}: {1}\n{2}".format(
				'Error',
				e,
				type(e).__name__
			))
			if __printdebug__:
				raise e
		#
	#
#

"""Call the program while wrapped in debug helpers"""
doMain(main)

#endregion


