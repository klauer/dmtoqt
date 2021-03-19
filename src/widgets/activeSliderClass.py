###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class activeSliderClass(BaseWidget):
	''' Produces a QEAnalogSlider widget (no implementation for caQtDM) '''

	count = 0
	@staticmethod
	def incrcount():
		activeSliderClass.count += 1
		return activeSliderClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(activeSliderClass, self).__init__(widget)
		self.count = activeSliderClass.incrcount()

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''
		self.property(elem, 'variable', 'controlPv', 'string')
		self.property(elem, 'readbackVariable', 'indicatorPv', 'string')
		#self.property(elem, 'savedValuePv', 'savedValuePv', 'unknowntype')
		if 'savedValuePv' in self.widget.props:
			self.logger.warn('savedValuePv property set to "%s"; ignoring as there\'s no equivalent on Qt Sliders' % self.widget.props['savedValuePv'])

		''' Autoscale unless limitsFromDb is turned off '''
		#self.property(elem, 'limitsFromDb', 'limitsFromDb', 'unknowntype')
		if not 'limitsFromDb' in self.widget.props:
			self.booleanProperty(elem, 'autoScale', False)
			self.property(elem, 'minimum', 'scaleMin', 'float')
			self.property(elem, 'maximum', 'scaleMax', 'float')
			''' Set major, minor intervals because QEAnalogSlider doesn't do a good job -
				but don't try to hard '''
			min = 0
			max = 10
			if 'scaleMin' in self.widget.props:
				min = float(self.widget.props['scaleMin'])
			if 'scaleMax' in self.widget.props:
				max = float(self.widget.props['scaleMax'])
			if min > max:
				tmp = min
				min = max
				max = tmp
			self.doubleProperty(elem, 'majorInterval', (max - min)/10.0)
			self.doubleProperty(elem, 'minorInterval', (max - min)/50.0)

		#self.property(elem, 'increment', 'increment', 'unknowntype')
		#self.property(elem, 'incMultiplier', 'incMultiplier', 'unknowntype')

		#self.property(elem, 'controlAlarm', 'controlAlarm', 'unknowntype')
		#self.property(elem, 'indicatorAlarm', 'indicatorAlarm', 'unknowntype')
		#self.property(elem, 'bgAlarm', 'bgAlarm', 'unknowntype')
		if 'controlAlarm' in self.widget.props or \
			'indicatorAlarm' in self.widget.props or \
			'bgAlarm' in self.widget.props:
			self.booleanProperty(elem, 'axisAlarmColours', True)

		#self.property(elem, 'bgColor', 'bgColor', 'color')
		#self.property(elem, 'displayFormat', 'displayFormat', 'unknowntype')
		self.property(elem, 'font', 'font', 'font')
		#self.property(elem, 'readLabel', 'readLabel', 'unknowntype')
		#self.property(elem, 'indicatorColor', 'indicatorColor', 'unknowntype')
		self.property(elem, 'precision', 'precision', 'int')
		#self.property(elem, '2ndBgColor', '2ndBgColor', 'unknowntype')
		#self.property(elem, 'controlLabel', 'controlLabel', 'unknowntype')
		#self.property(elem, 'controlColor', 'controlColor', 'unknowntype')
		#self.property(elem, 'fgColor', 'fgColor', 'color')

		''' Set continuousWrite to mimic the EDM behavior; users may want to override '''
		self.booleanProperty(elem, 'continuousWrite', True)
		''' Set border to more closely match the EDM appearance '''
		self.enumProperty(elem, 'frameShape', 'QFrame::StyledPanel')

		return elem

	def isBuiltInWidget(self):
		return False

	def isContainer(self):
		return False

	def widgetType(self):
		return 'QEAnalogSlider'

	def widgetName(self):
		return 'slider_%d' % activeSliderClass.count

	def widgetBaseClass(self):
		return 'QAnalogSlider'

	def widgetHeader(self):
		return self.widgetType()+'.h'
