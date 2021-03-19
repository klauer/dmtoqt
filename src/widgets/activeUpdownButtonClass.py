###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class activeUpdownButtonClass(BaseWidget):
	''' Produces a QESpinBox widget (no implementation for caQtDM) '''
	count = 0
	@staticmethod
	def incrcount():
		activeUpdownButtonClass.count += 1
		return activeUpdownButtonClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(activeUpdownButtonClass, self).__init__(widget)
		self.count = activeUpdownButtonClass.incrcount()

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''
		#self.property(elem, 'visInvert', 'visInvert', 'boolean')
		#self.property(elem, 'limitsFromDb', 'limitsFromDb', 'boolean')
		#self.property(elem, 'visMax', 'visMax', 'string')
		#self.property(elem, 'bgColor', 'bgColor', 'color')
		#self.property(elem, 'rate', 'rate', 'unknowntype')
		#self.property(elem, 'colorPv', 'colorPv', 'unknowntype')
		self.property(elem, 'font', 'font', 'font')
		self.property(elem, 'minimum', 'scaleMin', 'float')
		self.property(elem, 'maximum', 'scaleMax', 'float')
		#self.property(elem, 'coarseValue', 'coarseValue', 'unknowntype')
		#self.property(elem, 'label', 'label', 'unknowntype')
		#self.property(elem, 'controlPv', 'controlPv', 'unknowntype')
		#self.property(elem, '3d', '3d', 'unknowntype')
		#self.property(elem, 'visPv', 'visPv', 'string')
		self.property(elem, 'singleStep', 'fineValue', 'float')
		if 'coarseValue' in self.widget.props and 'rate' in self.widget.props:
			self.booleanProperty(elem, 'accelerated', True)
		#self.property(elem, 'topShadowColor', 'topShadowColor', 'color')
		#self.property(elem, 'savedValuePv', 'savedValuePv', 'unknowntype')
		#self.property(elem, 'invisible', 'invisible', 'boolean')
		#self.property(elem, 'visMin', 'visMin', 'string')
		#self.property(elem, 'botShadowColor', 'botShadowColor', 'color')
		#self.property(elem, 'fgColor', 'fgColor', 'color')


		self.endWidget(elem)
		return elem

	def isBuiltInWidget(self):
		return False

	def isContainer(self):
		return False

	def widgetType(self):
		return 'QESpinBox'

	def widgetName(self):
		return 'updown_%d' % activeUpdownButtonClass.count

	def widgetBaseClass(self):
		return 'QDoubleSpinBox'
