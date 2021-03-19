###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree
import math

class activeMeterClass(BaseWidget):
	''' Produces a QEAnalogProgressBar (no implementation for caQtDM) '''

	count = 0
	@staticmethod
	def incrcount():
		activeMeterClass.count += 1
		return activeMeterClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(activeMeterClass, self).__init__(widget)
		self.count = activeMeterClass.incrcount()

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''
		self.enumProperty(elem, 'mode', 'Meter')

		self.property(elem, 'useDbDisplayLimits', 'scaleLimitsFromDb', 'boolean')
		if 'scaleLimitsFromDb' not in self.widget.props:
			''' Don't set these if using db limits, because we can't determine the
				intervals without polling the pv '''
			minelem = self.property(elem, 'maximum', 'scaleMax', 'float')
			maxelem = self.property(elem, 'minimum', 'scaleMin', 'float')
			if len(set(self.widget.props) & set(['labelIntervals', 'majorIntervals', 'minorIntervals'])) > 0:
				min = 0.0
				max = 0.0
				if minelem is not None:
					min = float(self.widget.props['scaleMin'])
				if maxelem is not None:
					max = float(self.widget.props['scaleMax'])
				if max < min: tmp = max; max = min; min = tmp
				bigintvl = (max - min)/5
				smallintvl = 0
				if 'labelIntervals' in self.widget.props:
					n = int(self.widget.props['labelIntervals'])
					bigintvl = (max - min)/n
				if 'majorIntervals' in self.widget.props:
					n = int(self.widget.props['majorIntervals'])
					if 'labelIntervals' in self.widget.props:
						smallintvl = bigintvl/n
					else:
						bigintvl = (max - min)/n
				if 'minorIntervals' in self.widget.props and smallintvl == 0:
					n = int(self.widget.props['minorIntervals'])
					smallintvl = bigintvl/n
				if smallintvl == 0:
					''' Force small interval to an even divisor of big interval;
						otherwise QEAnalogProgressBar will override it '''
					smallintl = 10 ** int(math.log10(bigintvl))
					if smallintvl == 0: smallintvl = 1
				''' minorInterval must be set first; otherwise majorInterval may not take effect '''
				self.doubleProperty(elem, 'minorInterval', smallintvl)
				self.doubleProperty(elem, 'majorInterval', bigintvl)
				self.logger.info('%s %s: minorInterval=%g; majorInterval=%g' % (self.widgetType(), self.widgetName(), smallintvl, bigintvl))
		else:
			self.logger.warn('%s %s: scaleLimitsFromDb is set in .edl file.  This does not always work correctly; please check minorInterval and majorInterval' % (self.widgetType(), self.widgetName()))

		self.property(elem, 'fontColour', 'scaleColor', 'color')
		if 'useDisplayBg' in self.widget.props:
			self.colorProperty(elem, 'backgroundColour', 'transparent')
		else:
			self.property(elem, 'backgroundColour', 'bgColor', 'color')
		#self.property(elem, 'useDisplayBg', 'useDisplayBg', 'unknowntype')
		#self.property(elem, 'caseAlarm', 'caseAlarm', 'unknowntype')
		#self.property(elem, 'complexNeedle', 'complexNeedle', 'unknowntype')
		self.property(elem, 'borderColour', 'caseColor', 'color')
		if 'labelType' in self.widget.props:
			''' Same behavior for labelType == "literal" or "pvLabel" '''
			label = ''
			if 'label' in self.widget.props:
				label = self.widget.props['label']
			self.stringProperty(elem, 'localEnumeration', '<=0:"%s",>0:"%s"' % (label, label))
			self.enumProperty(elem, 'format', 'LocalEnumeration')
			self.booleanProperty(elem, 'addUnits', False)
		else:
			# The showText property is set in DMReader.findRedundantWidgets; if not present
			# it defaults to True
			showText = False
			if 'showText' in self.widget.props:
				showText = self.widget.props['showText']
			self.booleanProperty(elem, 'showText', showText)
		#self.property(elem, 'label', 'label', 'unknowntype')
		#self.property(elem, 'labelColor', 'labelColor', 'unknowntype')
		self.property(elem, 'showScale', 'showScale', 'boolean')
		self.enumProperty(elem, 'displayAlarmStateOption', 'WhenInAlarm')
		#self.property(elem, 'fgAlarm', 'fgAlarm', 'unknowntype')
		#self.property(elem, 'scaleAlarm', 'scaleAlarm', 'unknowntype')
		self.property(elem, 'spanAngle', 'meterAngle', 'int')
		#self.property(elem, 'topShadowColor', 'topShadowColor', 'color')
		#self.property(elem, 'scaleFontTag', 'scaleFontTag', 'unknowntype')
		if 'precision' in self.widget.props:
			self.booleanProperty(elem, 'useDbPrecision', False)
		self.property(elem, 'precision', 'scalePrecision', 'int')
		#self.property(elem, 'scaleFormat', 'scaleFormat', 'unknowntype')
		self.property(elem, 'font', 'labelFontTag', 'font')
		self.property(elem, 'variable', 'readPv', 'string')
		#self.property(elem, 'trackDelta', 'trackDelta', 'unknowntype')
		#self.property(elem, 'botShadowColor', 'botShadowColor', 'color')
		#self.property(elem, '3d', '3d', 'unknowntype')
		self.property(elem, 'foregroundColour', 'fgColor', 'color')


		self.endWidget(elem)
		return elem

	def isBuiltInWidget(self):
		return False

	def isContainer(self):
		return False

	def widgetType(self):
		return 'QEAnalogProgressBar'

	def widgetName(self):
		return 'meter_%d' % activeMeterClass.count

	def widgetBaseClass(self):
		return 'QEAnalogIndicator'
