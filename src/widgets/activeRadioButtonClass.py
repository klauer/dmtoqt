###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class activeRadioButtonClass(BaseWidget):
	''' Produces a QERadioGroup (no implementation for caQtDM) '''

	count = 0
	@staticmethod
	def incrcount():
		activeRadioButtonClass.count += 1
		return activeRadioButtonClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(activeRadioButtonClass, self).__init__(widget)
		self.count = activeRadioButtonClass.incrcount()
		if self.framework() == 'EpicsQt':
			w = int(self.widget.geometry['w'])
			h = int(self.widget.geometry['h'])
			if w < 120 or h < 40:
				self.logger.warn('QERadioGroup "%s": Size (%dx%d) is less than the minimum (%dx%d).  Please examine this element in Qt Designer and adjust as necessary.' % (self.widgetName(), w, h, 120, 40))
			''' Allow space for the label above. '''
			self.widget.geometry['h'] = str(h + 20)
			y = int(self.widget.geometry['y'])
			self.widget.geometry['y'] =  str(y - 20)
			self.logger.warn('QERadioGroup "%s": Height has been adjusted from %d to %d to make room for the title.  Please examine this element in Qt Designer and adjust as necessary.' % (self.widgetName(), h, h+20))

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''
		''' EDM Properties for this class\n")
			This lists all EDM properties specific to this class,\n")
			to be used in the widget class' widgetUI method.\n")
			Paste this code into your widgetUI method, then\n")
			adjust it to map to the appropriate Qt properties\n")
			(self.property arguments:\n")
			 uiname: Qt name for the property\n")
			 propname: EDM name, in self.widget.props\n")
			 type: 'int', 'string', 'color', 'boolean')\n")
		'''
		self.property(elem, 'variable', 'controlPv', 'string')
		self.property(elem, 'font', 'font', 'font')
		self.intProperty(elem, 'columns', 1)
		self.intProperty(elem, 'spacing', 0)
		lbl = '_'
		if 'controlPv' in self.widget.props and len(self.widget.props['controlPv'].strip()) > 0:
			title = self.widget.props['controlPv'].strip()
		self.stringProperty(elem, 'title', title)
		if 'bgAlarm' not in self.widget.props and 'fgAlarm' not in self.widget.props:
			self.enumProperty(elem, 'displayAlarmStateOption', 'WhenInAlarm')
		#self.property(elem, 'bgColor', 'bgColor', 'color')
		#self.property(elem, 'bgAlarm', 'bgAlarm', 'unknowntype')
		#self.property(elem, 'buttonColor', 'buttonColor', 'unknowntype')
		#self.property(elem, 'selectColor', 'selectColor', 'unknowntype')
		#self.property(elem, 'topShadowColor', 'topShadowColor', 'color')
		#self.property(elem, 'botShadowColor', 'botShadowColor', 'color')
		#self.property(elem, 'fgAlarm', 'fgAlarm', 'unknowntype')
		#self.property(elem, 'fgColor', 'fgColor', 'color')

		return elem

	def isBuiltInWidget(self):
		return False

	def isContainer(self):
		return False

	def widgetType(self):
		return 'QERadioGroup'

	def widgetName(self):
		return 'radiogroup_%d' % activeRadioButtonClass.count

	def widgetBaseClass(self):
		return 'QWidget'

	def widgetHeader(self):
		return self.widgetType()+'.h'
