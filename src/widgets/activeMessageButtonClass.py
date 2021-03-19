###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class activeMessageButtonClass(BaseWidget):
	''' Produces a QEPushButton (no implementation for caQtDM) '''
	count = 0
	@staticmethod
	def incrcount():
		activeMessageButtonClass.count += 1
		return activeMessageButtonClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(activeMessageButtonClass, self).__init__(widget)
		self.count = activeMessageButtonClass.incrcount()

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''
		''' When format is "Default", the default sent string ("1") causes an error, so we
			need "Integer" format instead.  This problem may be fixed at some point in EpicsQt. '''
		self.enumProperty(elem, 'format', 'Integer')
		#self.property(elem, 'useEnumNumeric', 'useEnumNumeric', 'unknowntype')
		''' Using updateOption == "State" seems to work best for most pvs '''
		self.enumProperty(elem, 'updateOption', 'State')

		self.defaultStyle(elem, {'background-color':'offColor'}, {'background-color':'onColor'})
		#self.property(elem, 'offColor', 'offColor', 'unknowntype')
		#self.property(elem, 'onColor', 'onColor', 'unknowntype')
		#self.property(elem, 'toggle', 'toggle', 'unknowntype')
		#self.property(elem, 'colorPv', 'colorPv', 'unknowntype')
		self.property(elem, 'font', 'font', 'font')
		self.property(elem, 'variable', 'controlPv', 'string')
		#self.property(elem, 'lock', 'lock', 'unknowntype')
		if '3d' not in self.widget.props:
			self.booleanProperty(elem, 'flat', True)
		#self.property(elem, '3d', '3d', 'unknowntype')
		#self.property(elem, 'closeOnRelease', 'closeOnRelease', 'unknowntype')
		#self.property(elem, 'topShadowColor', 'topShadowColor', 'color')
		if 'invisible' in self.widget.props:
			self.booleanProperty(elem, 'visible', False)
		#self.property(elem, 'invisible', 'invisible', 'boolean')
		self.property(elem, 'password', 'password', 'string')
		if 'onLabel' in self.widget.props and 'offLabel' in self.widget.props:
			lbl = self.widget.props['offLabel']
			if lbl != self.widget.props['onLabel']:
				lbl += ','+self.widget.props['onLabel']
				self.stringProperty(elem, 'localEnumeration', lbl)
				self.enumProperty(elem, 'format', 'LocalEnumeration')
			else:
				self.stringProperty(elem, 'labelText', lbl)
		#self.property(elem, 'onLabel', 'onLabel', 'unknowntype')
		#self.property(elem, 'offLabel', 'offLabel', 'unknowntype')
		#self.property(elem, 'closeOnPress', 'closeOnPress', 'unknowntype')
		if ('pressValue' in self.widget.props and isinstance(self.widget.props['pressValue'], str)) and ('releaseValue' in self.widget.props and isinstance(self.widget.props['releaseValue'], str)):
			if self.widget.props['pressValue'] != self.widget.props['releaseValue']:
				self.property(elem, 'pressText', 'pressValue', 'string')
				self.property(elem, 'releaseText', 'releaseValue', 'string')
				self.booleanProperty(elem, 'writeOnPress', True)
				self.booleanProperty(elem, 'writeOnRelase', True)
				self.booleanProperty(elem, 'writeOnClick', False)
			else:
				self.property(elem, 'clickText', 'pressValue', 'string')
		elif 'pressValue' in self.widget.props and isinstance(self.widget.props['pressValue'], str):
			self.property(elem, 'clickText', 'pressValue', 'string')
		elif 'releaseValue' in self.widget.props and isinstance(self.widget.props['releaseValue'], str):
			self.property(elem, 'clickText', 'releaseValue', 'string')

		#self.property(elem, 'botShadowColor', 'botShadowColor', 'color')
		#self.property(elem, 'fgColor', 'fgColor', 'color')

		return elem

	def isBuiltInWidget(self):
		return False

	def isContainer(self):
		return False

	def widgetType(self):
		return 'QEPushButton'

	def widgetName(self):
		return 'messagebutton_%d' % activeMessageButtonClass.count

	def widgetBaseClass(self):
		return 'QPushButton'

	def widgetHeader(self):
		return self.widgetType()+'.h'
