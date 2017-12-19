"""
Defunct Interpreter
by Elijah John Shadbolt (Cresspresso)
Copyright (c) 2017    MIT Licence

Version 1.2
2017-12-19 13:56:40 +1300

Check out the 'helptext' folder for more information about this project.
"""
#region Imports

from debugwrapper import *
from extensions import *
from structs import *
from globalvars import *
from reduction import *
import primitiveActions
import primitiveExpressions

#endregion
#region Command-Line Arguments

"""str - the file to interpret"""
clarg_filepath = None

def programCanStart(): return clarg_filepath != None #

#region Help

help_folder = "helptext"
help_type_default = ("version.txt", "clargs.txt")
help_types = {
	'about': ("about.txt",),
	'clargs': ("clargs.txt",),
	'licence': ("licence.txt",),
	'quick_start': ("quick_start.txt",),
	'version': ("version.txt",),
}

def PrintHelp():
	"""Handles the '-help' command-line argument and prints help text to the console."""
	def pr(*filenames):
		for filename in filenames:
			PrintFile(help_folder + '/' + filename)
	#

	if clargname_help in sys.argv:
		helptype = None
		try:
			helptype = sys.argv[sys.argv.index(clargname_help) + 1]
		except:
			pass

		if helptype in help_types:
			pr(*help_types[helptype])
		else:
			pr(*help_type_default)
	#
	else:
		pr(*help_type_default)
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
	if name in Keywords and not name in primitiveActions.names:
		raise DefunctError_InputError("Expected identifier, got keyword '{0}'".format(name), location)
	return name
#
def DoFuncArgname():
	name = DoName()
	if name in primitiveActions.names:
		raise DefunctError_InputError("Function Argument cannot have primitive name '{0}'".format(name), location)
	return name
#
def DoDefName():
	name = DoIdentifier()
	if name in Keywords:
		raise DefunctError_InputError("Expected identifier, got keyword '{0}'".format(name), location)
	elif name in primitiveActions.names:
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
		return primitiveExpressions.identity()

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
	"""Does a series of definitions and executions."""
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
			dprint ('EXECUTE    ' + SubToString(sub, sub), flush=True)
			sub = Simplify(sub, execute=True)
			dprint ('Finally    ' + SubToString(sub, sub), flush=True)
		#
	#
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

	HandleCLArguments()

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
			if cl_printdebug:
				raise e
		#
		except DefunctError as e:
			print("\n{0}: {1}\n{2}".format(
				'Error',
				e,
				type(e).__name__
			))
			print (cl_printdebug)
			if cl_printdebug:
				raise e
		#
	#
#

"""Call the program while wrapped in debug helpers"""
doMain(main)

#endregion


