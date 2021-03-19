'''
.. module:: EDMWidget
	:synopsis: Simple class to hold the properties of an EDM widget

'''
###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from collections import OrderedDict

class EDMWidget(object):
	''' Class to hold EDM properties '''

	def __init__(self, type):
		''' Constructor

		Args:
			type (string): The type name, e.g. activeXTextClass
		'''
		self.type = type
		self.version = {'major': 0, 'minor': 0, 'release': 0}
		self.geometry = {'x': 0, 'y': 0, 'w': 0, 'h': 0}
		self.props = {}
		self.currentGroup = None
		self.children = []
		# extra: any additional parameters added to the class declaration; e.g. 'activeXTextDspClass:noedit'
		self.extra = ''

	def setProperty(self, name, value):
		''' Set a property name-value pair.

			Performs some minimal processing to fill self.version or
			self.geometry, as appropriate; otherwise, the property
			is inserted into self.props.

		Args:
			name (string): The property name
			value (any): The property value
		'''
		if name in list(self.version.keys()):
			self.version[name] = value
			return
		elif name in list(self.geometry.keys()):
			self.geometry[name] = value
			return
		if self.currentGroup is not None:
			self.props[self.currentGroup][name] = value
			return
		self.props[name] = value

	def beginGroup(self, groupname):
		''' Start a group property; that is, a property whose value is an array

		Args:
			groupname (string): The name of the property
		'''
		self.setProperty(groupname, OrderedDict())
		self.currentGroup = groupname

	def endGroup(self):
		''' Finish a group property. '''
		self.currentGroup = None

	def addChild(self, widget):
		''' Add a child widget to self.children.

		Args:
			widget (src.EDMWidget.EDMWidget): the child widget
		'''
		self.children.append(widget)

	def hasChildren(self):
		''' Does this widget have one or more children?

		Returns:
			boolean: True if this widget has children
		'''
		return len(self.children) > 0

	def adjustChildGeometries(self):
		''' Ensure parent is big enough to hold all children.

			EDM does not hide children in this case; Qt does
		'''

		''' Subtract my x, y positions from the child's geometry '''
		left = int(self.geometry['x'])
		top = int(self.geometry['y'])
		right = left + int(self.geometry['w'])
		bottom = top + int(self.geometry['h'])

		# First pass: find outer limits
		for c in self.children:
			# Must first adjust grandchildren, great-grandchildren, ...
			c.adjustChildGeometries()

			cleft = int(c.geometry['x'])
			ctop = int(c.geometry['y'])
			cright = cleft + int(c.geometry['w'])
			cbottom = ctop + int(c.geometry['h'])
			if cleft < left:
				left = cleft
			if ctop < top:
				top = ctop
			if cright > right:
				right = cright
			if cbottom > bottom:
				bottom = cbottom

		# Second pass: subtract top, left from child coords
		for c in self.children:
			cleft = int(c.geometry['x'])
			ctop = int(c.geometry['y'])
			c.geometry['x'] = str(cleft - left)
			c.geometry['y'] = str(ctop - top)

		# Expand my size to fit all children
		self.geometry['x'] = str(left)
		self.geometry['y'] = str(top)
		self.geometry['w'] = str(right - left)
		self.geometry['h'] = str(bottom - top)
