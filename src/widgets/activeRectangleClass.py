###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class activeRectangleClass(BaseWidget):
	''' Depending on the chosen framework and this widget's properties,
		produces either a QESimpleShape, a QSimpleShape, or a caGraphics widget.
	'''
	count = 0
	@staticmethod
	def incrcount():
		activeRectangleClass.count += 1
		return activeRectangleClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(activeRectangleClass, self).__init__(widget)
		self.count = activeRectangleClass.incrcount()
		''' EDM can set rect width/height to zero, which renders a line '''
		self.shape = 'rect'
		if int(self.widget.geometry['w']) == 0:
			self.shape = 'vline'
			self.widget.geometry['w'] = '1'
		if int(self.widget.geometry['h']) == 0:
			self.shape = 'hline'
			self.widget.geometry['h'] = '1'

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''
		if self.framework() == 'EpicsQt':
			if self.widgetType() == 'QESimpleShape':
				self.property(elem, 'variable', 'alarmPv', 'string')
				if 'fillAlarm' not in self.widget.props:
					self.enumProperty(elem, 'displayAlarmStateOption', 'WhenInAlarm', {'stdset':'0'})
				if 'lineAlarm' not in self.widget.props:
					self.enumProperty(elem, 'edgeAlarmStateOption', 'WhenInAlarm', {'stdset':'0'})
			self.property(elem, 'edgeColour', 'lineColor', 'color')
			# Reverse the logic for invisible=>visible
			if 'invisible' in list(self.widget.props.keys()):
				isVisible = not bool(str(self.widget.props['invisible']))
				self.booleanProperty(elem, 'visible', isVisible)
			self.property(elem, 'edgeWidth', 'lineWidth', 'int')
			if 'fill' in self.widget.props:
				self.property(elem, 'colour0', 'fillColor', 'color')
			else:
				subelem = self.colorProperty(elem, 'colour0', {'r': 255, 'g': 255, 'b': 255, 'a': 0})
				if subelem is None:
					self.logger.warn('Failed to write property colour0 with alpha=0')
		else: # caQtDM
			self.property(elem, 'lineColor', 'lineColor', 'color')
			self.property(elem, 'foreground', 'fillColor', 'color')
			if 'fill' in self.widget.props:
				self.enumProperty(elem, 'fillstyle', 'Filled')
			self.property(elem, 'lineSize', 'lineWidth', 'int')
			if 'lineStyle' in self.widget.props:
				self.enumProperty(elem, 'linestyle', 'Dash')

		#self.property(elem, 'visMin', 'visMin', 'string')
		#self.property(elem, 'visPv', 'visPv', 'string')
		#self.property(elem, 'fillAlarm', 'fillAlarm', 'boolean')
		#self.property(elem, 'lineColor', 'lineColor', 'color')
		#self.property(elem, 'alarmPv', 'alarmPv', 'string')
		#self.property(elem, 'visMax', 'visMax', 'string')
		#self.property(elem, 'visInvert', 'visInvert', 'boolean')
		#self.property(elem, 'lineAlarm', 'lineAlarm', 'boolean')
		#self.property(elem, 'fillColor', 'fillColor', 'color')
		#self.property(elem, 'invisible', 'invisible', 'boolean')
		#self.property(elem, 'lineWidth', 'lineWidth', 'int')
		#self.property(elem, 'lineStyle', 'lineStyle', 'enum')
		#self.property(elem, 'fill', 'fill', 'boolean')

		return elem

	def isBuiltInWidget(self):
		return False

	def isContainer(self):
		return False

	def widgetType(self):
		if self.framework() == 'EpicsQt':
			if (('fillAlarm' in self.widget.props) or ('lineAlarm' in self.widget.props)) and ('alarmPv' in self.widget.props):
				return 'QESimpleShape'
			return 'QSimpleShape'
		return 'caGraphics'

	def widgetName(self):
		return '%s_%d' % (self.shape, activeRectangleClass.count)

	def widgetBaseClass(self):
		if self.widgetType() == 'QESimpleShape':
			return 'QSimpleShape'
		return 'QWidget'
