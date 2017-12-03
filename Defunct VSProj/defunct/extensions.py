"""General Extensions to Python"""

def joinObjects(separator, selector, items):
	"""Joins a string of objects by calling the selector with each item and putting the separator in between each item.
	Arguments:
		separator : str - string to put between each item
		selector : callable(item) - function with one parameter
		items : list - the objects to join
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

def PrintFile(filepath):
	"""Prints all the lines in a file, flushing every 20 lines."""
	with open(filepath) as file:
		i = 0
		for line in file:
			if i >= 20:
				print(line, end='', flush=True)
				i = 1
			else:
				print(line, end='')
				i += 1
		#
	#
#


