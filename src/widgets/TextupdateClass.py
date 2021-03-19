###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class TextupdateClass(BaseWidget):
	''' Produces a QELabel widget (no implementation for caQtDM) '''

	count = 0
	@staticmethod
	def incrcount():
		TextupdateClass.count += 1
		return TextupdateClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(TextupdateClass, self).__init__(widget)
		self.count = TextupdateClass.incrcount()

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''
		self.property(elem, 'font', 'font', 'font')
		self.enumProperty(elem, 'displayAlarmStateOption', 'WhenInAlarm')
		#self.property(elem, 'lineAlarm', 'lineAlarm', 'boolean')
		#self.property(elem, 'bgColor', 'bgColor', 'color')
		#self.property(elem, 'fgAlarm', 'fgAlarm', 'unknowntype')
		#self.property(elem, 'fgColor', 'fgColor', 'color')
		#self.property(elem, 'fill', 'fill', 'boolean')
		ss = '%s { ' % self.widgetType()
		useSS = False
		if 'fill' in self.widget.props and 'bgColor' in self.widget.props:
			useSS = True
			ss += 'background-color: %s; ' % self.colors.getRGB(self.widget.props['bgColor'])
		if 'fgAlarm' not in self.widget.props and 'fgColor' in self.widget.props:
			useSS = True
			ss += 'color: %s; ' % self.colors.getRGB(self.widget.props['fgColor'])
		if useSS:
			ss += '}'
			self.stringProperty(elem, 'defaultStyle', ss)
		#self.property(elem, 'fontAlign', 'fontAlign', 'unknowntype')
		self.property(elem, 'precision', 'precision', 'int')
		self.property(elem, 'lineWidth', 'lineWidth', 'int')
		if 'lineWidth' in self.widget.props:
			self.enumProperty(elem, 'frameShape', 'Box')
		self.property(elem, 'variable', 'controlPv', 'string')
		#self.property(elem, 'colorPv', 'colorPv', 'unknowntype')


		self.endWidget(elem)
		return elem

	def isBuiltInWidget(self):
		return False

	def isContainer(self):
		return False

	def widgetType(self):
		return 'QELabel'

	def widgetName(self):
		return 'textupdate_%d' % TextupdateClass.count

	def widgetBaseClass(self):
		return 'QLabel'
