###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class activeMotifSliderClass(BaseWidget):
	''' Depending on this widget's properties, produces either
		a QESlider, or a QEAnalogSlider (no implementation for caQtDM)
	'''

	count = 0
	@staticmethod
	def incrcount():
		activeMotifSliderClass.count += 1
		return activeMotifSliderClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(activeMotifSliderClass, self).__init__(widget)
		self.count = activeMotifSliderClass.incrcount()

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		self.geometry(elem)
		''' Add your widget-specific properties here '''
		#self.property(elem, 'showLimits', 'showLimits', 'unknowntype')
		#self.property(elem, 'limitsFromDb', 'limitsFromDb', 'unknowntype')
		#self.property(elem, 'bgColor', 'bgColor', 'color')
		#self.property(elem, 'increment', 'increment', 'unknowntype')
		self.property(elem, 'font', 'font', 'font')
		#self.property(elem, 'showValue', 'showValue', 'unknowntype')
		#self.property(elem, 'scaleMax', 'scaleMax', 'unknowntype')
		self.property(elem, 'variable', 'controlPv', 'string')
		#self.property(elem, 'showLabel', 'showLabel', 'unknowntype')
		#self.property(elem, 'precision', 'precision', 'unknowntype')
		#self.property(elem, 'showSavedValue', 'showSavedValue', 'unknowntype')
		#self.property(elem, 'topShadowColor', 'topShadowColor', 'color')
		#self.property(elem, 'savedValuePv', 'savedValuePv', 'unknowntype')
		#self.property(elem, 'scaleMin', 'scaleMin', 'unknowntype')
		#self.property(elem, 'bgAlarm', 'bgAlarm', 'unknowntype')
		#self.property(elem, '2ndBgColor', '2ndBgColor', 'unknowntype')
		#self.property(elem, 'controlLabel', 'controlLabel', 'unknowntype')
		#self.property(elem, 'botShadowColor', 'botShadowColor', 'color')
		#self.property(elem, 'fgColor', 'fgColor', 'color')

		if self.widgetType() == 'QESlider':
			if 'orientation' not in self.widget.props:
				self.enumProperty(elem, 'orientation', 'Qt::Horizontal', {'stdset':'0'})
			flags = ['showLabel', 'showLimits', 'showSavedValue', 'showValue']
			found = False
			for flag in flags:
				if flag in self.widget.props:
					found = True
					break
			if found: # Even if vertical, property gets written as TicksAbove/TicksBelow
				self.enumProperty(elem, 'tickPosition', 'QSlider::TicksAbove')
			ss = 'QESlider { '
			applyss = False
			if 'fgColor' in self.widget.props:
				applyss = True
				rgb = self.colors.getRGB(self.widget.props['fgColor'])
				ss += ' color: %s' % str(rgb)
			if 'bgColor' in self.widget.props and 'useDisplayBg' not in self.widget.props:
				if applyss: ss += ';'
				else: applyss = True
				rgb = self.colors.getRGB(self.widget.props['bgColor'])
				ss += ' background-color: %s' % str(rgb)
			if applyss:
				ss += ' }'
				self.stringProperty(elem, 'defaultStyle', ss, {'notr':'true'})
			self.property(elem, 'minimum', 'scaleMin', 'float')
			self.property(elem, 'maximum', 'scaleMax', 'float')
			self.property(elem, 'pageStep', 'increment', 'float')
			self.enumProperty(elem, 'displayAlarmStateOption', 'WhenInAlarm', {'stdset':'0'})
		else:
			self.property(elem, 'readbackVariable', 'indicatorPv', 'string')
			#self.property(elem, 'savedValuePv', 'savedValuePv', 'unknowntype')
			if 'savedValuePv' in self.widget.props:
				self.logger.warn('savedValuePv property set to "%s"; ignoring as there\'s no equivalent on Qt Analog Sliders' % self.widget.props['savedValuePv'])

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

			if 'bgAlarm' in self.widget.props:
				self.booleanProperty(elem, 'axisAlarmColours', True)

			self.property(elem, 'precision', 'precision', 'int')

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
		if 'orientation' in self.widget.props:
			return 'QESlider' # QEAnalogSlider cannot be vertical
		flags = ['showLabel', 'showLimits', 'showSavedValue', 'showValue']
		found = False
		for flag in flags:
			if flag in self.widget.props:
				found = True
				break
		if not found:
			return 'QESlider'
		return 'QEAnalogSlider'

	def widgetName(self):
		return 'motifslider_%d' % activeMotifSliderClass.count

	def widgetBaseClass(self):
		if self.widgetType() == 'QESlider':
			return 'QSlider'
		return 'QAnalogSlider'

	def widgetHeader(self):
		return self.widgetType()+'.h'
