###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################

from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class activeXTextDspClass(BaseWidget):
	''' Depending on the widget properties, produces either a
		QELabel, or a QELineEdit (no implementation for caQtDM)

		"Text Monitor" and "Text Control" share this EDM class; the widget type
		is appended with ":noedit" for Text Monitor
	'''

	count = 0
	@staticmethod
	def incrcount():
		activeXTextDspClass.count += 1
		return activeXTextDspClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(activeXTextDspClass, self).__init__(widget)
		self.count = activeXTextDspClass.incrcount()

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''

		# Common properties for text monitor/text control:
		self.property(elem, 'variable', 'controlPv', 'string')
		#self.property(elem, 'colorPv', 'colorPv', 'unknowntype')
		#self.property(elem, 'nullPv', 'nullPv', 'unknowntype')
		#self.property(elem, 'precision', 'precision', 'int')
		#self.property(elem, 'useDbPrecision', 'limitsFromDb', 'boolean')
		if 'precision' in self.widget.props and 'limitsFromDb' not in self.widget.props:
			self.intProperty(elem, 'precision', self.widget.props['precision'])
			self.booleanProperty(elem, 'useDbPrecision', False)
		elif 'format' in self.widget.props:
			if self.widget.props['format'] == 'hex':
				self.numberProperty(elem, 'radix', 16)
				self.numberProperty(elem, 'precision', 0)
		#self.property(elem, 'fieldLen', 'fieldLen', 'unknowntype')
		#self.property(elem, 'noExecuteClipMask', 'noExecuteClipMask', 'unknowntype')
		#self.property(elem, 'clipToDspLimits', 'clipToDspLimits', 'unknowntype')
		if 'showUnits' not in self.widget.props:
			self.booleanProperty(elem, 'addUnits', False)
		#self.property(elem, 'addUnits', 'showUnits', 'boolean')
		#self.property(elem, 'autoHeight', 'autoHeight', 'unknowntype')
		#self.property(elem, 'smartRefresh', 'smartRefresh', 'unknowntype')
		#self.property(elem, 'fastUpdate', 'fastUpdate', 'unknowntype') # do not throttle updates to 2Hz
		#self.property(elem, 'motifWidget', 'motifWidget', 'unknowntype') # enables several properties
		''' Some properties are implemented as a default stylesheet '''
		ss = self.widgetType() + ' {'
		applyss = False
		if 'fgColor' in self.widget.props:
			applyss = True
			rgb = self.colors.getRGB(self.widget.props['fgColor'])
			ss += ' color: %s; ' % str(rgb)
		if 'useDisplayBg' in self.widget.props and self.widgetType() == 'QELabel':
			applyss = True
			ss += 'background: transparent; '
		elif 'bgColor' in self.widget.props:
			applyss = True
			rgb = self.colors.getRGB(self.widget.props['bgColor'])
			ss += ' background-color: %s' % str(rgb)
		if applyss:
			ss += '}'
			self.stringProperty(elem, 'defaultStyle', ss, {'notr':'true'})

		#self.property(elem, 'fgColor', 'fgColor', 'color')
		self.enumProperty(elem, 'displayAlarmStateOption', 'WhenInAlarm', {'stdset':'0'})

		#self.property(elem, 'fgAlarm', 'fgAlarm', 'unknowntype')
		#self.property(elem, 'useAlarmBorder', 'useAlarmBorder', 'unknowntype')
		#self.property(elem, 'bgColor', 'bgColor', 'color')

		#self.property(elem, 'bgAlarm', 'bgAlarm', 'unknowntype')
		#self.property(elem, 'useDisplayBg', 'useDisplayBg', 'unknowntype')
		#self.property(elem, 'nullColor', 'nullColor', 'unknowntype')
		self.property(elem, 'font', 'font', 'font')

		#self.property(elem, 'useKp', 'useKp', 'unknowntype') # keypad
		#self.property(elem, 'characterMode', 'characterMode', 'unknowntype') # write PV on every keystroke
		#self.property(elem, 'inputFocusUpdates', 'inputFocusUpdates', 'unknowntype') # external PV values don't change edit value while focus
		#self.property(elem, 'changeValOnLoseFocus', 'changeValOnLoseFocus', 'unknowntype') # force enter key to update pv value
		#self.property(elem, 'autoSelect', 'autoSelect', 'unknowntype') # select text when widget gets focus
		#self.property(elem, 'updatePvOnDrop', 'updatePvOnDrop', 'unknowntype') # enable drag-drop of pv value
		if 'isPassword' in self.widget.props:
			self.stringProperty(elem, 'echoMode', 'QLineEdit::Password', {'notr':'true'})
		#self.property(elem, 'date', 'date', 'unknowntype') # use calendar popup
		#self.property(elem, 'dateAsFileName', 'dateAsFileName', 'unknowntype') # convert date format to filename (e.g. "jan 05 2003 11:10:05" becomes "jan05_2003_111005")
		#self.property(elem, 'file', 'file', 'unknowntype') # use file selection dlg
		#self.property(elem, 'defDir', 'defDir', 'unknowntype') # default dir for file selection dlg
		#self.property(elem, 'pattern', 'pattern', 'unknowntype') # filename patter for file selection dlg

		# id and changeCallback are used to construct a C function name like "idChange",
		# which is called from a user-supplied shared library.  Even if it were possible
		# to replicate that, it would not be worth the effort here.
		#self.property(elem, 'id', 'id', 'unknowntype')
		#self.property(elem, 'changeCallback', 'changeCallback', 'unknowntype')

		# newPos is not relevant, since Qt uses a different method of placing widgets
		#self.property(elem, 'newPos', 'newPos', 'unknowntype')

		return elem

	def isBuiltInWidget(self):
		return False

	def isContainer(self):
		return False

	def widgetType(self):
		# "Text Monitor" and "Text Control" share this EDM class; the widget type
		# is appended with ":noedit" for Text Monitor
		if self.widget.extra == ':noedit':
			return 'QELabel'
		return 'QELineEdit'

	def widgetName(self):
		return 'text_%d' % activeXTextDspClass.count

	def widgetBaseClass(self):
		if self.widgetType() == 'QELabel':
			return 'QLabel'
		return 'QLineEdit'

