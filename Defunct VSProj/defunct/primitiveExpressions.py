#region imports

from structs import *

#endregion
#region Basics

""" identity = [x.x] """
def identity():
	f = Func('x', ArgRef('x'))
	f.body.func = f
	return f
#

""" false = [y x. x] """
def false():
	f = Func('y', Func('x', ArgRef('x')))
	f.body.body.func = f.body.body
	return f
#

""" true = [y x. y] """
def true():
	f = Func('y', Func('x', ArgRef('y')))
	f.body.body.func = f.body
	return f
#

#endregion
#region cn Operators

""" S = [w y x. y(w y x)] """
def successor():
	f = Func('w', Func('y', Func('x', Bracket(ArgRef('y'), Bracket(Bracket(ArgRef('w'), ArgRef('y')), ArgRef('x'))))))
	# TODO
	return f
#

#endregion
#region Church Numerals (cn)

""" 0 = [y x. x] """
def cn0():
	return false()
#

#region cn1
""" 1 = [y x. y x] """
def cn1():
	f = Func('y', Func('x', Bracket(ArgRef('y'), ArgRef('x'))))
	f.body.body.left.func = f
	f.body.body.right.func = f.body
	return f
#
_cn1 = cn1()
def cn1():
	return CopySub(_cn1)
#
#endregion

#region cn2
""" 2 = [y x. y(y x)] """
def cn2():
	f = Func('y', Func('x', Bracket(ArgRef('y'), ArgRef('x'))))
	f.body.body.left.func = f
	f.body.body.right.func = f.body
	return f
#
_cn2 = cn2()
def cn2():
	return CopySub(_cn2)
#
#endregon

#endregion


