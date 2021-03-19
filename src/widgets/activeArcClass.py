###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class activeArcClass(BaseWidget):
	''' Maps an EDM arc widget to a Qt widget.
		When using a caGraphics widget, has the
		following incompatibilities:

		- fill only works as Pie (no Chord)

		 When using a QEShape, incompatibilities are:

		- Line color cannot be changed (always black)
		- no alarm state
		- no visibility response
	'''

	count = 0

	@staticmethod
	def incrcount():
		activeArcClass.count += 1
		return activeArcClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(activeArcClass, self).__init__(widget)
		self.count = activeArcClass.incrcount()

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''
		if self.framework() == 'caQtDM':
			''' caGraphics-specific properties: '''
			if 'fill' in self.widget.props:
				self.stringProperty(elem, 'fillstyle', 'caGraphics::Filled')
			self.property(elem, 'foreground', 'fillColor', 'color')
			self.property(elem, 'lineSize', 'lineWidth', 'int')
			self.property(elem, 'spanAngle', 'totalAngle', 'int')
			self.property(elem, 'lineColor', 'lineColor', 'color')
			self.stringProperty(elem, 'colorMode', 'Static')
			self.stringProperty(elem, 'form', 'caGraphics::Arc')
		else:
			''' QEShape-specific properties: '''
			lineWidth = 1
			if 'lineWidth' in self.widget.props:
				lineWidth = int(self.widget.props['lineWidth'])
			if lineWidth == 0:
				self.booleanProperty(elem, 'drawBorder', 'false')
			x = lineWidth/2
			y = lineWidth/2
			self.pointProperty(elem, 'point1', x, y)
			x = int(self.widget.geometry['w']) - lineWidth
			y = int(self.widget.geometry['h']) - lineWidth
			self.pointProperty(elem, 'point2', x, y)
			if 'fill' in self.widget.props:
				self.property(elem, 'fill', 'fill', 'boolean')
				self.colorProperty(elem, 'color1', self.widget.props['fillColor'])
				if 'fillMode' in self.widget.props:
					self.stringProperty(elem, 'shape', 'QEShape::Pie')
				else:
					self.stringProperty(elem, 'shape', 'QEShape::Chord')
			else:
				self.stringProperty(elem, 'shape', 'QEShape::Arc')
			self.property(elem, 'lineWidth', 'lineWidth', 'int')
			self.property(elem, 'arcLength', 'totalAngle', 'float')
			''' no equivalent for lineColor '''

		''' Common properties: '''
		#self.property(elem, 'fillAlarm', 'fillAlarm', 'boolean')
		#self.property(elem, 'alarmPv', 'alarmPv', 'string')
		#self.property(elem, 'lineAlarm', 'lineAlarm', 'boolean')
		self.property(elem, 'startAngle', 'startAngle', 'float')

		return elem

	def isBuiltInWidget(self):
		return False

	def isContainer(self):
		return False

	def widgetType(self):
		if self.framework() == 'EpicsQt':
			return 'QEShape'
		return 'caGraphics'

	def widgetName(self):
		return 'arc_%d' % activeArcClass.count

	def widgetBaseClass(self):
		return 'QWidget'
