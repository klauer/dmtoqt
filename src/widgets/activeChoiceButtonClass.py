###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class activeChoiceButtonClass(BaseWidget):
	''' Depending on the choice of framework produces
		either a QERadioGroup or a caChoice widget.
	'''

	count = 0
	@staticmethod
	def incrcount():
		activeChoiceButtonClass.count += 1
		return activeChoiceButtonClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(activeChoiceButtonClass, self).__init__(widget)
		self.count = activeChoiceButtonClass.incrcount()
		if self.framework() == 'EpicsQt':
			''' Issue a warning if height (before adjusting height below) is less
				than the min assumed by QERadioGroup '''
			h = int(self.widget.geometry['h'])
			if h < 40:
				self.logger.warn('QERadioGroup "%s": Height (%d) is less than the minimum (%d).  Please examine this element in Qt Designer and adjust as necessary.' % (self.widgetName(), h, 40))
			''' Allow space for the label above. '''
			self.widget.geometry['h'] = str(h + 20)
			y = int(self.widget.geometry['y'])
			self.widget.geometry['y'] =  str(y - 20)
			self.logger.warn('QERadioGroup "%s": Height has been adjusted from %d to %d to make room for the title.  Please examine this element in Qt Designer and adjust as necessary.' % (self.widgetName(), h, h+20))

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''

		if self.framework() == 'EpicsQt':
			self.property(elem, 'variable', 'controlPv', 'string')

			''' Override the minimumSize property (120x40) set by QERadioGroup '''
			mselem = etree.SubElement(elem, 'property', {'name':'minimumSize'})
			selem = etree.SubElement(mselem, 'size')
			welem = etree.SubElement(selem, 'width')
			welem.text = '0'
			helem = etree.SubElement(selem, 'height')
			helem.text = '40' # TODO: do we want to reduce this?

			cols = 1
			if 'orientation' in self.widget.props:
				cols = 2
			self.intProperty(elem, 'columns', str(cols))
			''' No equivalent to title in EDM, but setting it to a blank string
				results in "QERadioGroup".  So, set it to "." and let the user
				decide how best to fix it. '''
			''' UPDATE: As of Aug. 2017, the ALS copy of qeframework allows a blank
				title so we set it to "" (instead of ".") '''
			self.stringProperty(elem, 'title', '')
			self.enumProperty(elem, 'buttonStyle', 'Push')
			self.intProperty(elem, 'spacing', '0')
			if 'bgAlarm' not in self.widget.props:
				self.enumProperty(elem, 'displayAlarmStateOption', 'WhenInAlarm')
			ss = ''
			if 'selectColor' in self.widget.props:
				color = self.colors.getRGB(self.widget.props['selectColor'])
				ss += '%s QPushButton:checked { background-color: %s; } ' % (self.widgetType(), str(color))
			if 'bgColor' in self.widget.props:
				color = self.colors.getRGB(self.widget.props['bgColor'])
				ss += '%s QPushButton { background-color: %s; } ' % (self.widgetType(), str(color))
			if len(ss) > 0:
				self.stringProperty(elem, 'defaultStyle', ss)

		else: # caQtDM
			if 'controlPv' in self.widget.props:
				self.property(elem, 'channel', 'controlPv', 'string')
			else:
				self.property(elem, 'channel', 'indicatorPv', 'string')
			self.property(elem, 'foreground', 'fgColor', 'color')
			self.property(elem, 'background', 'bgColor', 'color')
			self.property(elem, 'bordercolor', 'selectColor', 'color')
			self.enumProperty(elem, 'alignment', 'center')
			if 'orientation' in self.widget.props:
				self.enumProperty(elem, 'stackingMode', 'Column')
			self.enumProperty(elem, 'fontScaleMode', 'None')

		#self.property(elem, 'visInvert', 'visInvert', 'boolean')
		#self.property(elem, 'visMax', 'visMax', 'string')
		#self.property(elem, 'bgColor', 'bgColor', 'color')
		#self.property(elem, 'indicatorPv', 'indicatorPv', 'unknowntype')
		#self.property(elem, 'colorPv', 'colorPv', 'unknowntype')
		#self.property(elem, 'font', 'font', 'font')
		#self.property(elem, 'controlPv', 'controlPv', 'unknowntype')
		#self.property(elem, 'fgAlarm', 'fgAlarm', 'unknowntype')
		#self.property(elem, 'visPv', 'visPv', 'string')
		#self.property(elem, 'topShadowColor', 'topShadowColor', 'color')
		#self.property(elem, 'selectColor', 'selectColor', 'unknowntype')
		#self.property(elem, 'visMin', 'visMin', 'string')
		#self.property(elem, 'bgAlarm', 'bgAlarm', 'unknowntype')
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
			return 'QERadioGroup'
		return 'caChoice'

	def widgetName(self):
		return 'choice_%d' % activeChoiceButtonClass.count

	def widgetBaseClass(self):
		return 'QWidget'
