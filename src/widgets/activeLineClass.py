###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class activeLineClass(BaseWidget):
	''' Produces different widget types depending on the chosen framework and
		this widget's properties:

		* For a straight line with no visPv: a QLine
		* For a straight line with visPv and under caQtDM: a caPolyLine
		* For an arrow and EpicsQt: a QSimpleShape
		* For caQtDM: a caPolyLine
		* Absent all of the above preconditions: a QEShape
	'''

	count = 0
	@staticmethod
	def incrcount():
		activeLineClass.count += 1
		return activeLineClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(activeLineClass, self).__init__(widget)
		self.count = activeLineClass.incrcount()
		if self.widgetType() == 'Line':
			''' Adjust width/height to line thickness (EDM sets it to zero) '''
			n = 1
			if 'lineWidth' in self.widget.props:
				n = int(self.widget.props['lineWidth'])
			if self.samePoints('xPoints'):
				self.widget.geometry['w'] = str(n)
			else:
				self.widget.geometry['h'] = str(n)
		elif self.widgetType() == 'QEShape':
			''' Increment width and height by one each '''
			self.widget.geometry['w'] = str(int(self.widget.geometry['w']) + 1)
			self.widget.geometry['h'] = str(int(self.widget.geometry['h']) + 1)
		elif self.widgetType() == 'QSimpleShape':
			''' Arrow requires min width or height '''
			if int(self.widget.geometry['w']) <= 1:
				self.widget.geometry['w'] = str(16)
				self.widget.geometry['x'] = str(int(self.widget.geometry['x']) - 8)
			elif int(self.widget.geometry['h']) <= 1:
				self.widget.geometry['h'] = str(16)
				self.widget.geometry['y'] = str(int(self.widget.geometry['y']) - 8)

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''
		#self.property(elem, 'fill', 'fill', 'boolean')
		#self.property(elem, 'fillAlarm', 'fillAlarm', 'boolean')
		#self.property(elem, 'alarmPv', 'alarmPv', 'string')
		#self.property(elem, 'foreground', 'fillColor', 'color')
		#self.property(elem, 'closePolygon', 'closePolygon', 'boolean')
		#self.property(elem, 'yPoints', 'yPoints', 'unknowntype')
		#self.property(elem, 'numPoints', 'numPoints', 'int')
		#self.property(elem, 'xPoints', 'xPoints', 'unknowntype')
		#self.property(elem, 'arrows', 'arrows', 'unknowntype')
		#self.property(elem, 'lineAlarm', 'lineAlarm', 'boolean')
		#self.property(elem, 'lineColor', 'lineColor', 'color')
		#self.property(elem, 'lineSize', 'lineWidth', 'int')
		#self.property(elem, 'linestyle', 'lineStyle', 'enum')

		if self.widgetType() == 'Line':
			if self.samePoints('xPoints'):
				self.enumProperty(elem, 'orientation', 'Qt::Vertical')
			self.stringProperty(elem, 'frameShadow', 'QFrame::Plain')
			self.property(elem, 'lineWidth', 'lineWidth', 'int')

		elif self.framework() == 'caQtDM':
			self.property(elem, 'foreground', 'fillColor', 'color')
			self.property(elem, 'lineColor', 'lineColor', 'color')
			self.property(elem, 'lineSize', 'lineWidth', 'int')
			if 'xPoints' in self.widget.props:
				left = int(self.widget.geometry['x'])
				top = int(self.widget.geometry['y'])
				first = True
				pairs = ''
				for i in range(len(self.widget.props['xPoints'])):
					if first: first = False
					else: pairs += ';'
					x = int(self.widget.props['xPoints'][str(i)]) - left
					y = int(self.widget.props['yPoints'][str(i)]) - top
					pairs += '%d,%d' % (x, y)
				self.stringProperty(elem, 'xyPairs', pairs)

			if 'fill' in self.widget.props:
				self.stringProperty(elem, 'fillstyle', 'caPolyLine::Filled')

			if 'closePolygon' in self.widget.props:
				self.stringProperty(elem, 'polystyle', 'caPolyLine::Polygon')

			if 'lineStyle' in self.widget.props:
				self.stringProperty(elem, 'linestyle', 'caPolyLine::Dash')

			alarmpv = 'alarmPv' in self.widget.props
			if alarmpv:
				self.stringProperty(elem, 'colorMode', 'caPolyLine::Alarm')
				self.stringProperty(elem, 'channel', self.widget.props['alarmPv'], {'notr':'true'})

		elif self.widgetType() == 'QSimpleShape': # Draw an EpicsQt arrow
			shape = 'arrowUp'
			if int(self.widget.geometry['w']) == 16:
				if self.widget.props['arrows'] == 'to':
					if int(self.widget.props['yPoints']['0']) < int(self.widget.props['yPoints']['1']):
						shape = 'arrowDown'
					else:
						shape = 'arrowUp'
				else:
					if int(self.widget.props['yPoints']['0']) < int(self.widget.props['yPoints']['1']):
						shape = 'arrowUp'
					else:
						shape = 'arrowDown'
			elif int(self.widget.geometry['h']) == 16:
				if self.widget.props['arrows'] == 'to':
					if int(self.widget.props['xPoints']['0']) < int(self.widget.props['xPoints']['1']):
						shape = 'arrowRight'
					else:
						shape = 'arrowLeft'
				else:
					if int(self.widget.props['xPoints']['0']) < int(self.widget.props['xPoints']['1']):
						shape = 'arrowLeft'
					else:
						shape = 'arrowRight'
			self.enumProperty(elem, 'shape', shape)


		else: # EpicsQt
			shape = 'QEShape::Polyline'
			if 'fill' in self.widget.props:
				shape = 'QEShape::Polygon'
				if 'fillAlarm' in self.widget.props:
					shape = 'rectangle'
				elif 'lineColor' in self.widget.props and 'fillColor' in self.widget.props \
					and self.widget.props['lineColor'] == self.widget.props['fillColor']:
					self.booleanProperty(elem, 'drawBorder', False)
			self.enumProperty(elem, 'shape', shape)
			self.intProperty(elem, 'numPoints', len(self.widget.props['xPoints']))
			self.property(elem, 'lineWidth', 'lineWidth', 'int')
			left = int(self.widget.geometry['x'])
			top = int(self.widget.geometry['y'])
			for i in range(len(self.widget.props['xPoints'])):
				x = int(self.widget.props['xPoints'][str(i)]) - left
				y = int(self.widget.props['yPoints'][str(i)]) - top
				subelem = etree.SubElement(elem, 'property', {'name':'point%d' % (i+1), 'stdset':'0'})
				ptelem = etree.SubElement(subelem, 'point')
				xelem = etree.SubElement(ptelem, 'x')
				xelem.text = str(x)
				yelem = etree.SubElement(ptelem, 'y')
				yelem.text = str(y)
			alarmpv = 'alarmPv' in self.widget.props
			if alarmpv:
				self.stringProperty(elem, 'variable', self.widget.props['alarmPv'])
			else:
				self.colorProperty(elem, 'color1', self.widget.props['fillColor'])

		return elem

	## Determine if two points form a horizontal or vertical line; that is,
	## the x or y points are the "same", within a fudge factor
	## @param propname string The property name (either "xPoints" or "yPoints")
	## @return boolean True if self.widget.props[propname] are (approx.) the same.
	def samePoints(self, propname):
		if len(self.widget.props[propname]) != 2:
			return False
		return abs(int(self.widget.props[propname]['0']) - int(self.widget.props[propname]['1'])) <= 2

	def isBuiltInWidget(self):
		return False

	def isContainer(self):
		return False

	def widgetType(self):
		if 'xPoints' in self.widget.props and len(self.widget.props['xPoints']) == 2:
			if 'visPv' in self.widget.props and self.framework() == 'caQtDM':
				return 'caPolyLine'
			if 'arrows' in self.widget.props and self.framework() == 'EpicsQt':
				return 'QSimpleShape'
			if self.samePoints('xPoints') or self.samePoints('yPoints'):
				return 'Line'
		if self.framework() == 'caQtDM':
			return 'caPolyLine'
		''' QESimpleShape provides better alarm handling, so is a better choice even though the
			actual shape will come out wrong '''
		if 'alarmPv' in self.widget.props or 'fillAlarm' in self.widget.props:
			return 'QESimpleShape'
		return 'QEShape'

	def widgetName(self):
		return 'line_%d' % activeLineClass.count

	def widgetBaseClass(self):
		return 'QWidget'
