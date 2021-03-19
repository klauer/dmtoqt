###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class activeGroupClass(BaseWidget):
	''' The activeGroupClass provides a grouping of widgets.  In Qt, this is best mapped
		to an invisible QWidget.  The child widgets under this will retain that
		hierarchy in the output .ui file.
	'''

	count = 0
	@staticmethod
	def incrcount():
		activeGroupClass.count += 1
		return activeGroupClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(activeGroupClass, self).__init__(widget)
		self.count = activeGroupClass.incrcount()

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''
		#self.property(elem, 'visMin', 'visMin', 'string')
		#self.property(elem, 'visPv', 'visPv', 'string')
		#self.property(elem, 'visInvert', 'visInvert', 'boolean')
		#self.property(elem, 'object', 'object', 'unknowntype')
		#self.property(elem, 'endGroup', 'endGroup', 'unknowntype')
		#self.property(elem, 'beginGroup', 'beginGroup', 'unknowntype')
		#self.property(elem, 'visMax', 'visMax', 'string')


		self.endWidget(elem)
		return elem

	def isBuiltInWidget(self):
		return True

	def isContainer(self):
		return True

	def widgetType(self):
		return 'QWidget'

	def widgetName(self):
		return 'group_%d' % activeGroupClass.count

	def widgetBaseClass(self):
		return 'QObject'
