'''
.. module:: DMReader
   :synopsis: Defines the DMReader class for reading EDM files

'''
###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################

import logging
import sys
import os
import re
from collections import OrderedDict
from EDMWidget import EDMWidget
from StackedEDMWidget import StackedEDMWidget

class DMReader:
	''' Reads an EDM file and creates a series of
		EDMWidget instances
	'''

	# regular expression: version string
	__re_version = re.compile(r'(\d) (\d) (\d)')

	# regular expression: comment
	_re_comment = re.compile(r'^# \((.*)\)')

	# regular expression: object declaration
	_re_objdecl = re.compile(r'^object ([^:]+)(:.+)?')

	# regular expression: name-value pair
	_re_namevalue = re.compile(r'^([^" ]+) "?([^"]+)"?')

	# regular expression: name-empty value pair
	_re_emptyvalue = re.compile(r'^([^" ]+) ""$')

	# regular expression: boolean value (name only)
	_re_boolvalue = re.compile(r'^([^" ]+)$')

	# regular expression: generic string
	_re_string = re.compile(r'^"([^"]+)"$')

	# regular expression: quoted string
	_re_quotestring = re.compile(r'^"\\"([^"]+)\\""$')

	def __init__(self, infilename):
		''' Constructor

	Args:
		infilename (string): the input EDM file name
	'''
		self.logger = logging.getLogger('DMReader')
		self.infilename = infilename
		self.lineno = 0
		self.version = { 'major': 0, 'minor': 0, 'release': 0 }

	def read(self, infile):
		''' Parse the EDM file

	Args:
		infile (file object): The input file stream object

	Returns:
		boolean: True on success, False otherwise
	'''
		self.widgets = []

		if not self.readHeading(infile):
			self.logger.critical('Cannot read heading from %s' % self.infilename)
			return False

		self.mainWidget = self.readWidget('activeWindowClass', infile)
		self.parentWidget = None
		for line in infile:
			self.lineno += 1
			line = line.strip()
			#self.logger.debug('[%d] Reading line: "%s"' % (self.lineno, line))
			if line == '': continue
			m = DMReader._re_comment.match(line)
			if m is not None:
				continue
			m = DMReader._re_objdecl.match(line)
			if m is not None:
				widget = self.readWidget(m.group(1), infile, extra=m.group(2))
				if widget is None:
					self.logger.critical('Failed to read widget')
					return False
				self.widgets.append(widget)
			else:
				self.logger.critical('Unrecognized string on line %d: "%s"' % (self.lineno, line))
				return False
		self.logger.info('Found %d widget(s) in %d lines' % (len(self.widgets), self.lineno))

		if not self.findRedundantWidgets():
			self.logger.warn('findRedundantWidgets failed')

		if not self.findStackedWidgets():
			self.logger.warn('findStackedWidgets failed')

		return True

	def readHeading(self, infile):
		''' Read the heading from the EDM file.

			The version should appear on the first line as 3 space-separated integers.
			Called from DMReader.read; not normally needed elsewhere.

		Args:
			infile (file object): The input file stream object

		Returns:
			boolean: True on success, False otherwise
		'''
		foundVersion = False
		for line in infile:
			self.lineno += 1
			line = line.strip()
			if not foundVersion:
				m = DMReader.__re_version.match(line)
				if m is None:
					self.logger.critical('Version not found; illegal edl file')
					return False
				self.version = { 'major': m.group(1), 'minor': m.group(2), 'release': m.group(3) }
				foundVersion = True
				return True
			if line == '': continue

		self.logger.critical('Version not found; illegal edl file')
		return False

	def readWidget(self, type, infile, extra=''):
		''' Read a widget definition from the EDM file.

			Called from DMReader.read.
			Interprets each line in the file as a property definition,
			until the end tag is reached.  Recursively calls itself
			when child widgets appear under this widget.

		Args:
			type (string): The EDM widget type
			infile (file object): The input file stream object
			extra (string): (optional) extra property to be set on the widget. Currently only used for activeXTextDspClass, which is used for text inputs with no extra and for text monitors with extra=":noedit"

		Returns:
			The created widget, or None if no widget is created.
		'''
		self.logger.debug('Reading widget, type="%s"' % type)
		widget = self.createWidgetType(type)
		widget.extra = extra
		self.groupCount = None
		for line in infile:
			self.lineno += 1
			line = line.strip()
			if line == '': continue
			if line == 'beginObjectProperties' or line == 'beginScreenProperties':
				inProps = True
				continue
			if line == 'endObjectProperties' or line == 'endScreenProperties':
				inProps = False
				return widget
			if line == 'beginGroup':
				if type != 'activeGroupClass':
					self.logger.critical('[line %d]: beginGroup in unexpected location; giving up' % self.lineno)
					return None
				widget.parent = self.parentWidget
				self.parentWidget = widget
				for line in infile:
					self.lineno += 1
					line = line.strip()
					if line == '': continue
					if line == 'endGroup':
						if self.parentWidget is not None:
							widget = self.parentWidget
							self.parentWidget = self.parentWidget.parent
							break # out of inner for loop
						self.logger.critical('[line %d]: endGroup in unexpected location; giving up' % self.lineno)
						return None
					m = DMReader._re_objdecl.match(line)
					if m is not None:
						''' Recursive call '''
						child = self.readWidget(m.group(1), infile, extra=m.group(2))
						if child is None:
							return None
						self.parentWidget.addChild(child)

			if not inProps:
				self.logger.critical('Invalid input file format, please check (at or near line %d)' % self.lineno)
			if line.endswith(' {'):
				widget.beginGroup(line[0:len(line)-2])
				self.groupCount = 0
				continue
			if line == '}':
				widget.endGroup()
				self.groupCount = None
				continue
			m = DMReader._re_namevalue.match(line)
			if m is not None:
				widget.setProperty(m.group(1), m.group(2))
				continue
			m = DMReader._re_emptyvalue.match(line)
			if m is not None:
				continue # ignore empty values
			m = DMReader._re_boolvalue.match(line)
			if m is not None:
				widget.setProperty(m.group(1), True)
				continue
			m = DMReader._re_string.match(line)
			if m is not None:
				if self.groupCount is not None:
					self.groupCount += 1
					widget.setProperty(str(self.groupCount), m.group(1))
				else:
					widget.setProperty('0', m.group(1))
				continue
			m = DMReader._re_quotestring.match(line)
			if m is not None:
				if self.groupCount is not None:
					self.groupCount += 1
					widget.setProperty(str(self.groupCount), '"%s"' % m.group(1))
				else:
					widget.setProperty('0', '"%s"' % m.group(1))
				continue
			self.logger.warn('Unknown string at line %d: %s' % (self.lineno, line))
		self.logger.debug('Created widget: %s' % widget)
		return widget

	def createWidgetType(self, type):
		''' Create a widget of the specified type.

			Currently a trivial function that returns a new EDMWidget,
			but could become more complicated in the future.

		Args:
			type (string): The type of widget to be created

		Returns:
			src.EDMWidget.EDMWidget: the created widget
		'''
		return EDMWidget(type)

	def findRedundantWidgets(self, parent=None):
		''' Find any text monitor widgets that are overlapping other widget types
			that monitor the same pv and can display the value as text, rendering
			the text monitor redundant.

			Also find button widgets overlaid by static text; users may have done this
			to, for example, put a carriage return in the displayed text.
			Will be called recursively when a widget containing children is found; in this
			case the parent parameter will be set to the containing widget.

		Args:
			parent (src.EDMWidget.EDMWidget): The parent widget

		Returns:
			boolean: True on success, False otherwise
		'''
		if parent is None:
			widgets = self.widgets
			self.nRemoved = 0
		else:
			widgets = parent.children
		for widget in widgets:
			if widget.type == 'activeGroupClass':
				''' Recursive call: check the group's children '''
				if not self.findRedundantWidgets(widget):
					self.logger.critical('findRedundantWidgets failed for an activeGroupClass')
					return False
				continue
			if widget.type in ['activeBarClass', 'activeMeterClass']:
				for widget2 in widgets:
					if widget2.type == 'activeXTextDspClass' and self.overlapping(widget, widget2):
						if 'controlPv' not in widget2.props:
							continue
						pv2 = widget2.props['controlPv']
						pv = ''
						if widget.type == 'activeBarClass' and 'indicatorPv' in widget.props:
							pv = widget.props['indicatorPv']
						elif widget.type == 'activeMeterClass' and 'readPv' in widget.props:
							pv = widget.props['readPv']
						if pv != pv2:
							continue
						self.logger.info('Found a text monitor overlapping a graphical widget that can replace the text; removing the text monitor (pv = %s)' % pv)
						widgets.remove(widget2)
						self.nRemoved += 1
						widget.props['showText'] = True
			elif widget.type in ['relatedDisplayClass', 'shellCmdClass']:
				for widget2 in widgets:
					if widget2.type == 'activeXTextClass' and self.overlapping(widget, widget2):
						widget.props['buttonLabel'] = "\n".join(list(widget2.props['value'].values()))
						if 'font' in widget2.props:
							widget.props['font'] = widget2.props['font']
						widgets.remove(widget2)
						self.nRemoved += 1
						self.logger.info('Found a static text overlapping a button; removing the static text "%s" and setting the button text' % widget.props['buttonLabel'])
						break
		if parent is None and self.nRemoved > 0:
			self.logger.info('Removed %d text monitor widgets as they were redundant' % nRemoved)
		return True

	def findStackedWidgets(self, parent=None):
		''' Find any widgets that are on top of each other whose visibility depends on
			the values of one or more pvs, and combine them into
			a StackedEDMWidget widget type.

			Will be called recursively when a widget containing children is found; in this
			case the parent parameter will be set to the containing widget.

		Args:
			parent (src.EDMWidget.EDMWidget): The parent widget

		Returns:
			boolean: True on success, False otherwise
		'''
		if parent is None:
			widgets = self.widgets
			self.nStacks = 0
			self.nWidgets = 0
		else:
			widgets = parent.children
		stacks = []
		for widget in widgets:
			if 'inStack' in widget.props:
				continue
			if widget.type == 'activeGroupClass':
				''' Recursive call: check the group for stacks '''
				if not self.findStackedWidgets(widget):
					self.logger.critical('findStackedWidgets failed for an activeGroupClass')
					return False
				continue
			if widget.type in ['activeXTextClass', 'activeCircleClass', 'activeRectangleClass'] and \
				('visPv' in widget.props or 'alarmPv' in widget.props):
				stackWidget = None
				for widget2 in widgets:
					if 'inStack' in widget2.props:
						continue
					if widget2.type == widget.type:
						if id(widget2) == id(widget):
							continue # same widget instance
						if not self.overlapping(widget, widget2):
							continue
						if stackWidget is None:
							stackWidget = StackedEDMWidget()
							stackWidget.add(widget)
							stacks.append(stackWidget)
						stackWidget.add(widget2)
		for stackWidget in stacks:
			if not self.addStackWidget(stackWidget, parent):
				self.logger.critical('addStackWidget failed')
				return False
			self.nStacks += 1
			self.nWidgets += len(stackWidget.stack)
		if parent is None and self.nStacks > 0:
			self.logger.info('Combined %d widgets into %d stacks' % (self.nWidgets, self.nStacks))
		return True

	def overlapping(self, widget, widget2):
		''' Determine whether two widgets overlap.  They also must have a similar
			position & size, to avoid false positives when, e.g., a rectangle is
			drawn around a group of widgets.

		Args:
			widget (src.EDMWidget.EDMWidget): One of the widgets
			widget2 (src.EDMWidget.EDMWidget): The other widget

		Returns:
			boolean: True if the widgets overlap; False otherwise
		'''
		g1 = widget.geometry
		g2 = widget2.geometry
		hmin1 = int(g1['x'])
		hmin2 = int(g2['x'])
		hmax1 = hmin1 + int(g1['w'])
		hmax2 = hmin2 + int(g2['w'])
		if (hmin1 > hmax2) or (hmax1 < hmin2):
			return False
		vmin1 = int(g1['y'])
		vmin2 = int(g2['y'])
		vmax1 = vmin1 + int(g1['h'])
		vmax2 = vmin2 + int(g2['h'])
		if (vmin1 > vmax2) or (vmax1 < vmin2):
			return False
		''' Position and height must be similar.  Width may vary if this is a stack of labels '''
		if abs(hmin1-hmin2) > 10 or abs(vmin1-vmin2) > 10 or abs(vmax1-vmax2) > 10:
			return False

		return True

	def addStackWidget(self, stackedEDMWidget, parent):
		''' Adds widget to the collection, removing any sub-widgets

		Args:
			stackedEDMWidget (src.StackedEDMWidget.StackedEDMWidget): The StackedEDMWidget instance
			parent (src.EDMWidget.EDMWidget): The parent widget or None to use DMReader

		Returns:
			boolean: True on success; False if an error occurs
		'''
		if parent is None:
			widgets = self.widgets
		else:
			widgets = parent.children
		idx = -1
		for s in stackedEDMWidget.stack:
			for w in widgets:
				if id(w) == id(s):
					if idx == -1:
						idx = widgets.index(w)
					widgets.remove(w)
		if idx != -1:
			if idx > len(widgets):
				idx = len(widgets)
			widgets.insert(idx, stackedEDMWidget)
			return True
		self.logger.critical('Cannot add a stacked EDM widget set')
		return False
