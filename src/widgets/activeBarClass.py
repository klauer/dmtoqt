###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class activeBarClass(BaseWidget):
	''' Maps the EDM activeBarClass to EpicsQt QEAnalogProgressBar,
		or caQtDM caLinearGauge.
	'''

	count = 0
	@staticmethod
	def incrcount():
		activeBarClass.count += 1
		return activeBarClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(activeBarClass, self).__init__(widget)
		self.count = activeBarClass.incrcount()

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''
		if self.framework() == 'EpicsQt':
			self.property(elem, 'variable', 'indicatorPv', 'string')
			self.property(elem, 'showScale', 'showScale', 'boolean')
			# The showText property is set in DMReader.findRedundantWidgets; if not present
			# it defaults to True
			showText = False
			if 'showText' in self.widget.props:
				showText = self.widget.props['showText']
			self.booleanProperty(elem, 'showText', showText)
			if 'orientation' in self.widget.props:
				self.enumProperty(elem, 'orientation', 'QEAnalogIndicator::Bottom_To_Top')
			# EDM displays 3 tick levels (label, major, minor); QE widgets only 2
			# EDM also sets #ticks while QE sets intervals
			if 'limitsFromDb' in self.widget.props:
				self.booleanProperty(elem, 'useDbDisplayLimits', True)
			else:
				self.property(elem, 'minimum', 'min', 'float')
				self.property(elem, 'maximum', 'max', 'float')
				min = 0
				max = 100
				lticks = 10
				mticks = 5
				if 'min' in self.widget.props:
					min = float(self.widget.props['min'])
				if 'max' in self.widget.props:
					max = float(self.widget.props['max'])
				if 'labelTicks' in self.widget.props:
					lticks = int(self.widget.props['labelTicks'])
				if 'minorTicks' in self.widget.props:
					mticks = int(self.widget.props['minorTicks'])
				lintvl = max - min
				if lticks != 1:
					lintvl /= (lticks - 1)
				mintvl = lintvl/mticks
				self.doubleProperty(elem, 'minorInterval', mintvl)
				self.doubleProperty(elem, 'majorInterval', lintvl)
			if 'border' in self.widget.props:
				self.property(elem, 'borderColour', 'fgColor', 'color')
			else:
				self.colorProperty(elem, 'borderColour', {'r':0, 'g':0, 'b':0, 'a':0})
			self.property(elem, 'backgroundColour', 'bgColor', 'color')
			self.property(elem, 'foregroundColour', 'indicatorColor', 'color')
			self.property(elem, 'fontColour', 'fgColor', 'color')
			# default scaleFormat is FFloat, which matches the QE default Fixed notation
			if 'scaleFormat' in self.widget.props:
				fmt = 'QEAnalogProgressBar::'
				if self.widget.props['scaleFormat'] == 'Exponential':
					fmt += 'Scientific'
				else: # 'GFloat'
					fmt += 'Automatic'
				self.enumProperty(elem, 'notation', fmt)
			if 'precision' in self.widget.props:
				self.intProperty(elem, 'precision', self.widget.props['precision'])
				self.booleanProperty(elem, 'useDbPrecision', False)
			if 'fgAlarm' in self.widget.props:
				self.enumProperty(elem, 'alarmSeverityDisplayMode', 'QEAnalogProgressBar::foreground')
			if 'indicatorAlarm' in self.widget.props:
				self.enumProperty(elem, 'displayAlarmStateOption', 'QEAnalogProgressBar::WhenInAlarm')
		else: # caQtDM
			self.property(elem, 'channel', 'indicatorPv', 'string')
			self.property(elem, 'scaleEnabled', 'showScale', 'boolean')
			if 'orientation' not in self.widget.props:
				self.stringProperty(elem, 'orientation', 'caLinearGauge::Horizontal')
			if 'limitsFromDb' not in self.widget.props:
				self.stringProperty(elem, 'displayLimits', 'EAbstractGauge::User_Limits')
				self.property(elem, 'minValue', 'min', 'float')
				self.property(elem, 'maxValue', 'max', 'float')
				self.property(elem, 'reference', 'origin', 'float')
				self.stringProperty(elem, 'fillMode', 'caLinearGauge::FROM_REF')
			else:
				self.stringProperty(elem, 'fillMode', 'caLinearGauge::FROM_ZERO')
			# EDM displays 3 tick levels (label, major, minor); caQtDM widgets only 2
			self.property(elem, 'numMajorTicks', 'labelTicks', 'int')
			self.property(elem, 'numMinorTicks', 'minorTicks', 'int')
			fmt = '%'
			precision = 1
			if 'precision' in self.widget.props:
				precision = int(self.widget.props['precision'])
			fmt += '.%d' % precision
			if 'scaleFormat' in self.widget.props:
				if self.widget.props['scaleFormat'] == 'Exponential':
					fmt += 'e'
				else: # 'GFloat'
					fmt += 'g'
			else:
				fmt += 'f'
			self.stringProperty(elem, 'valueFormat', fmt)

		#self.property(elem, 'origin', 'origin', 'unknowntype')
		#self.property(elem, 'majorTicks', 'majorTicks', 'unknowntype')
		#self.property(elem, 'indicatorPv', 'indicatorPv', 'unknowntype')
		#self.property(elem, 'backgroundColor', 'bgColor', 'color')
		self.property(elem, 'font', 'font', 'font')
		#self.property(elem, 'border', 'border', 'unknowntype')
		#self.property(elem, 'min', 'min', 'unknowntype')
		#self.property(elem, 'label', 'label', 'unknowntype')
		#self.property(elem, 'labelTicks', 'labelTicks', 'unknowntype')
		#self.property(elem, 'indicatorAlarm', 'indicatorAlarm', 'unknowntype')
		#self.property(elem, 'showScale', 'showScale', 'unknowntype')
		#self.property(elem, 'fgAlarm', 'fgAlarm', 'unknowntype')
		#self.property(elem, 'indicatorColor', 'indicatorColor', 'unknowntype')
		#self.property(elem, 'max', 'max', 'unknowntype')
		#self.property(elem, 'precision', 'precision', 'unknowntype')
		#self.property(elem, 'scaleFormat', 'scaleFormat', 'unknowntype')
		#self.property(elem, 'limitsFromDb', 'limitsFromDb', 'unknowntype')
		#self.property(elem, 'nullPv', 'nullPv', 'unknowntype')
		#self.property(elem, 'minorTicks', 'minorTicks', 'unknowntype')
		#self.property(elem, 'fgColor', 'fgColor', 'color')

		return elem

	def isBuiltInWidget(self):
		return False

	def isContainer(self):
		return False

	def widgetType(self):
		if self.framework() == 'EpicsQt':
			return 'QEAnalogProgressBar'
		return 'caLinearGauge'

	def widgetName(self):
		return 'bar_%d' % activeBarClass.count

	def widgetBaseClass(self):
		if self.framework() == 'EpicsQt':
			return 'QEAnalogIndicator'
		return 'QWidget'
