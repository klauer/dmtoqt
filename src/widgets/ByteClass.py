###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class ByteClass(BaseWidget):
	''' Produces a QEBitStatus widget (no implementation for caQtDM) '''

	count = 0

	@staticmethod
	def incrcount():
		ByteClass.count += 1
		return ByteClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(ByteClass, self).__init__(widget)
		self.count = ByteClass.incrcount()

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''
		self.property(elem, 'offColour', 'offColor', 'color')
		self.property(elem, 'onColour', 'onColor', 'color')
		self.property(elem, 'boarderColour', 'lineColor', 'color')
		self.property(elem, 'numberOfBits', 'numBits', 'int')
		self.property(elem, 'variable', 'controlPv', 'string')
		if 'endian' in self.widget.props and self.widget.props['endian'] == 'little':
			self.enumProperty(elem, 'Orientation', 'LSB_On_Left')
		#self.property(elem, 'endian', 'endian', 'unknowntype')
		self.property(elem, 'shift', 'shift', 'int')
		#self.property(elem, 'lineWidth', 'lineWidth', 'int')
		#self.property(elem, 'lineStyle', 'lineStyle', 'enum')


		self.endWidget(elem)
		return elem

	def isBuiltInWidget(self):
		return False

	def isContainer(self):
		return False

	def widgetType(self):
		return 'QEBitStatus'

	def widgetName(self):
		return 'byte_%d' % ByteClass.count

	def widgetBaseClass(self):
		return 'QBitStatus'
