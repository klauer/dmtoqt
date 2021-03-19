'''
.. module:: StackedEDMWidget
	:synopsis: A specialization of EDMWidget for combining two or more EDMWidgets
'''
###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.EDMWidget import EDMWidget

class StackedEDMWidget(EDMWidget):
	''' Holds 2 or more EDMWidget instances that are stacked on top of one another. '''

	def __init__(self):
		''' Constructor '''
		super(StackedEDMWidget, self).__init__('StackWidget')
		self.stack = []
		self._stackType = None

	def add(self, edmWidget):
		''' Add a widget to the stack.

			As a side effect, sets edmWidget.props['inStack'] = True.

		Args:
			edmWidget (src.EDMWidget.EDMWidget): the widget to add

		Returns:
			boolean: True
		'''
		self.stack.append(edmWidget)
		if len(self.stack) == 1:
			self.geometry = edmWidget.geometry
			self.version = edmWidget.version
			self.firstWidget = edmWidget
		edmWidget.props['inStack'] = True
		return True

	def stackType(self):
		''' Determine my stack type ("labels" or "shapes").

			Uses self.firstWidget; if it is an activeXTextClass then this
			is a set of labels, presumably only one will be visible at a time.

			If it is anything else, assume this is a set of rectangles, circles,
			or whatever; the bottom one may always be visible while the others
			only appear when pv value(s) change.

		Returns:
			string: Either "labels" or "shapes"
		'''
		if self._stackType is not None:
			return self._stackType

		''' Re-assign self.firstWidget if there's one that has no Pv '''
		for w in self.stack:
			if 'visPv' not in w.props and 'alarmPv' not in w.props:
				self.firstWidget = w
				break

		if self.firstWidget.type == 'activeXTextClass':
			self._stackType = 'labels'
		else:
			self._stackType = 'shapes'
		return self._stackType

