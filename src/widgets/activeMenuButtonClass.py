###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class activeMenuButtonClass(BaseWidget):
	''' Produces a QEComboBox (no implementation for caQtDM) '''

	count = 0
	@staticmethod
	def incrcount():
		activeMenuButtonClass.count += 1
		return activeMenuButtonClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(activeMenuButtonClass, self).__init__(widget)
		self.count = activeMenuButtonClass.incrcount()

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''
		self.property(elem, 'font', 'font', 'font')
		self.property(elem, 'variable', 'controlPv', 'string')
		self.defaultStyle(elem, {'background-color':'bgColor', 'color':'fgColor'})
		#self.property(elem, 'indicatorPv', 'indicatorPv', 'unknowntype')
		#self.property(elem, 'bgColor', 'bgColor', 'color')
		#self.property(elem, 'colorPv', 'colorPv', 'unknowntype')
		if 'fgAlarm' not in self.widget.props and 'bgAlarm' not in self.widget.props:
			self.enumProperty(elem, 'displayAlarmStateOption', 'WhenInAlarm')
		#self.property(elem, 'bgAlarm', 'bgAlarm', 'unknowntype')
		#self.property(elem, 'fgAlarm', 'fgAlarm', 'unknowntype')
		#self.property(elem, 'topShadowColor', 'topShadowColor', 'color')
		#self.property(elem, 'botShadowColor', 'botShadowColor', 'color')
		#self.property(elem, 'fgColor', 'fgColor', 'color')
		#self.property(elem, 'inconsistentColor', 'inconsistentColor', 'unknowntype')
		#self.property(elem, 'visInvert', 'visInvert', 'boolean')
		#self.property(elem, 'visPv', 'visPv', 'string')
		#self.property(elem, 'visMax', 'visMax', 'string')
		#self.property(elem, 'visMin', 'visMin', 'string')


		self.endWidget(elem)
		return elem

	def isBuiltInWidget(self):
		return False

	def isContainer(self):
		return False

	def widgetType(self):
		return 'QEComboBox'

	def widgetName(self):
		return 'menubutton_%d' % activeMenuButtonClass.count

	def widgetBaseClass(self):
		return 'QComboBox'
