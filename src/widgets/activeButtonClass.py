###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class activeButtonClass(BaseWidget):
	''' Depending on the chosen framework
		and the properties of this widget, produces either
		a QEPushButton, a QECheckBox, a caMessageButton, or a caToggleButton
	'''

	count = 0
	@staticmethod
	def incrcount():
		activeButtonClass.count += 1
		return activeButtonClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(activeButtonClass, self).__init__(widget)
		self.count = activeButtonClass.incrcount()

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''
		if self.framework() == 'EpicsQt':
			self.property(elem, 'variable', 'controlPv', 'string')
			self.property(elem, 'altReadbackVariable', 'indicatorPv', 'string')
			self.booleanProperty(elem, 'subscribe', True)
			if 'invisible' in self.widget.props:
				self.booleanProperty(elem, 'visible', False)
			if '3d' not in self.widget.props:
				self.booleanProperty(elem, 'flat', True)

			txt = ''
			if 'labelType' in self.widget.props and self.widget.props['labelType'] == 'literal':
				if 'offLabel' in self.widget.props and self.widget.props['offLabel'] != '':
					txt += self.widget.props['offLabel']
				if 'onLabel' in self.widget.props and self.widget.props['onLabel'] != '':
					if txt != '': txt += '/'
					txt += self.widget.props['onLabel']
			if txt == '':
				self.logger.warn('%s %s: EDM would fill labelText with pv state, but this tool cannot do that.  Attempting to use pv name; please examine this widget in Designer.' % (self.widgetType(), self.widgetName()))
				if 'controlPv' in self.widget.props:
					txt = self.widget.props['controlPv']
				elif 'indicatorPv' in self.widget.props:
					txt = self.widget.props['indicatorPv']
			self.stringProperty(elem, 'labelText', txt)

			self.property(elem, 'releaseText', 'offLabel', 'string')
			self.property(elem, 'labelText', 'offLabel', 'string')
			self.property(elem, 'pressText', 'onLabel', 'string')
			if 'buttonType' not in self.widget.props:
				self.booleanProperty(elem, 'checkable', True)
			''' When format is "Default", the default sent string ("1") causes an error, so we
				need "Integer" format instead.  This problem may be fixed at some point in EpicsQt. '''
			self.enumProperty(elem, 'format', 'Integer')
			#self.property(elem, 'useEnumNumeric', 'useEnumNumeric', 'unknowntype')
			''' Using updateOption == "State" seems to work best for most pvs '''
			self.enumProperty(elem, 'updateOption', 'State')

		else: # caQtDM
			if 'controlPv' in self.widget.props:
				self.stringProperty(elem, 'channel', self.widget.props['controlPv'])
			elif 'indicatorPv' in self.widget.props:
				self.stringProperty(elem, 'channel', self.widget.props['indicatorPv'])
			if 'offLabel' in self.widget.props:
				self.stringProperty(elem, 'label', self.widget.props['offLabel'])
			elif 'onLabel' in self.widget.props:
				self.stringProperty(elem, 'label', self.widget.props['onLabel'])
			self.property(elem, 'foreground', 'fgColor', 'color')
		#self.property(elem, 'indicatorPv', 'indicatorPv', 'unknowntype')
		#self.property(elem, 'offColor', 'offColor', 'unknowntype')
		#self.property(elem, 'colorPv', 'colorPv', 'unknowntype')
		#self.property(elem, 'offLabel', 'offLabel', 'unknowntype')
		self.property(elem, 'font', 'font', 'font')
		#self.property(elem, 'onColor', 'onColor', 'unknowntype')
		#self.property(elem, 'controlPv', 'controlPv', 'unknowntype')
		#self.property(elem, 'controlBitPos', 'controlBitPos', 'unknowntype')
		#self.property(elem, 'fgAlarm', 'fgAlarm', 'unknowntype')
		#self.property(elem, '3d', '3d', 'unknowntype')
		#self.property(elem, 'readBitPos', 'readBitPos', 'unknowntype')
		#self.property(elem, 'topShadowColor', 'topShadowColor', 'color')
		#self.property(elem, 'invisible', 'invisible', 'boolean')
		#self.property(elem, 'onLabel', 'onLabel', 'unknowntype')
		#self.property(elem, 'botShadowColor', 'botShadowColor', 'color')
		#self.property(elem, 'fgColor', 'fgColor', 'color')
		#self.property(elem, 'inconsistentColor', 'inconsistentColor', 'unknowntype')

		return elem

	def isBuiltInWidget(self):
		return False

	def isContainer(self):
		return False

	def widgetType(self):
		if self.framework() == 'EpicsQt':
			if 'buttonType' in self.widget.props and self.widget.props['buttonType'] == 'push':
				return 'QEPushButton'
			return 'QECheckBox'
		if 'buttonType' in self.widget.props and self.widget.props['buttonType'] == 'push':
			return 'caMessageButton'
		return 'caToggleButton'

	def widgetName(self):
		return 'button_%d' % activeButtonClass.count

	def widgetBaseClass(self):
		if self.widgetType() == 'QECheckBox':
			return 'QCheckBox'
		return 'QPushButton'
