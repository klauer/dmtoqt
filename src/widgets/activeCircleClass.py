###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class activeCircleClass(BaseWidget):
	''' Depending on the choice of framework and this widget's properties, produces
		either a QESimpleShape, QSimpleShape, or caGraphics widget.
	'''

	count = 0
	@staticmethod
	def incrcount():
		activeCircleClass.count += 1
		return activeCircleClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(activeCircleClass, self).__init__(widget)
		self.count = activeCircleClass.incrcount()

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''
		if self.framework() == 'EpicsQt':
			if self.widget.geometry['w'] == self.widget.geometry['h']:
				self.enumProperty(elem, 'shape', 'circle')
			else:
				self.enumProperty(elem, 'shape', 'ellipse')
			if self.widgetType() == 'QESimpleShape':
				self.property(elem, 'variable', 'alarmPv', 'string')
				if 'fillAlarm' not in self.widget.props:
					self.enumProperty(elem, 'displayAlarmStateOption', 'WhenInAlarm')
				if 'lineAlarm' not in self.widget.props:
					self.enumProperty(elem, 'edgeAlarmStateOption', 'WhenInAlarm')
			self.property(elem, 'edgeColour', 'lineColor', 'color')
			self.property(elem, 'colour0', 'fillColor', 'color')
			# Reverse the logic for invisible=>visible
			if 'invisible' in self.widget.props:
				self.booleanProperty(elem, 'visible', False)
			self.property(elem, 'edgeWidth', 'lineWidth', 'int')
			if 'fill' not in self.widget.props:
				self.colorProperty(elem, 'colour0', {'r': 255, 'g': 255, 'b': 255, 'a': 0})
		else: # caQtDM
			self.property(elem, 'lineColor', 'lineColor', 'color')
			self.property(elem, 'foreground', 'fillColor', 'color')
			if 'fill' in self.widget.props:
				self.enumProperty(elem, 'fillstyle', 'Filled')
			self.property(elem, 'lineSize', 'lineWidth', 'int')
			if 'lineStyle' in self.widget.props:
				self.enumProperty(elem, 'linestyle', 'Dash')
			self.enumProperty(elem, 'form', 'Circle')

		#self.property(elem, 'visMin', 'visMin', 'string')
		#self.property(elem, 'visPv', 'visPv', 'string')
		#self.property(elem, 'fillAlarm', 'fillAlarm', 'boolean')
		#self.property(elem, 'lineColor', 'lineColor', 'color')
		#self.property(elem, 'alarmPv', 'alarmPv', 'string')
		#self.property(elem, 'visMax', 'visMax', 'string')
		#self.property(elem, 'visInvert', 'visInvert', 'boolean')
		#self.property(elem, 'lineAlarm', 'lineAlarm', 'boolean')
		#self.property(elem, 'fillColor', 'fillColor', 'color')
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
		return 'circle_%d' % activeCircleClass.count

	def widgetBaseClass(self):
		if self.widgetType() == 'QESimpleShape':
			return 'QSimpleShape'
		return 'QWidget'
