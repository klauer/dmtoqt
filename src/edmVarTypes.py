'''
.. module:: edmVarTypes
	:synopsis: Simple types for use by findEDMProps

'''
###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################

class Variable:
	''' Simple container for a variable, its type, and a default value

		See: :mod:`findEDMProps`
	'''
	def __init__(self, varname, type=None, initvalue=None):
		self.name = varname.strip()
		self.type = type
		self.initvalue = initvalue

''' Collection of known variable types.  This aids findEDMProps.py
	in writing the proper types.  It could be fleshed out more,
	but in practice has not proven all that useful.

	See :class:`edmVarTypes.Variable`
'''
knownVariableTypes = { \
	'major': Variable('major', 'int', None),\
	'minor': Variable('minor', 'int', None),\
	'release': Variable('release', 'int', None),\
	'x': Variable('x', 'int', None),\
	'y': Variable('y', 'int', None),\
	'w': Variable('w', 'int', None),\
	'h': Variable('h', 'int', None),\
	'invisible': Variable('invisible', 'boolean', 0),\
	'visInvert': Variable('visInvert', 'boolean', 0),\
	'lineColor': Variable('lineColor', 'color', None),\
	'fillColor': Variable('fillColor', 'color', None),\
	'fgColor': Variable('fgColor', 'color', None),\
	'bgColor': Variable('bgColor', 'color', None),\
	'textColor': Variable('textColor', 'color', None),\
	'ctlFgColor1': Variable('ctlFgColor1', 'color', None),\
	'ctlFgColor2': Variable('ctlFgColor2', 'color', None),\
	'ctlBgColor1': Variable('ctlBgColor1', 'color', None),\
	'ctlBgColor2': Variable('ctlBgColor2', 'color', None),\
	'topShadowColor': Variable('topShadowColor', 'color', None),\
	'botShadowColor': Variable('botShadowColor', 'color', None),\
	'lineAlarm': Variable('lineAlarm', 'boolean', 0),\
	'fill': Variable('fill', 'boolean', 0),\
	'fillAlarm': Variable('fillAlarm', 'boolean', 0),\
	'lineWidth': Variable('lineWidth', 'int', 1),\
	'lineStyle': Variable('lineStyle', 'enum', 'solid'),\
	'alarmPv': Variable('alarmPv', 'string', ''),\
	'visPv': Variable('visPv', 'string', ''),\
	'visMin': Variable('visMin', 'string', ''),\
	'visMax': Variable('visMax', 'string', ''),\
	'font': Variable('font', 'font', ''),\
	'ctlFont': Variable('ctlFont', 'font', ''),\
	'btnFont': Variable('btnFont', 'font', ''),\
	'command': Variable('command', 'strings', ''),\
	'commandLabel': Variable('commandLabel', 'strings', ''),\
	'buttonLabel': Variable('buttonLabel', 'string', ''),\
	'closePolygon': Variable('closePolygon', 'boolean', False),\
	'numPoints': Variable('numPoints', 'int', 0),\
	'precision': Variable('precision', 'int', 0),\
	'limitsFromDb': Variable('limitsFromDb', 'boolean', False),\
	'showUnits': Variable('addUnits', 'boolean', False),\
	'editable': Variable('editable', 'boolean', True),\
}

