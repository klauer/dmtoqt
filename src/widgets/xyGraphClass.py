###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class xyGraphClass(BaseWidget):
	count = 0
	@staticmethod
	def incrcount():
		xyGraphClass.count += 1
		return xyGraphClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(xyGraphClass, self).__init__(widget)
		self.count = xyGraphClass.incrcount()

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''
		#self.property(elem, 'resetPv', 'resetPv', 'unknowntype')
		self.property(elem, 'font', 'font', 'font')
		#self.property(elem, 'border', 'border', 'boolean')
		if 'border' in self.widget.props:
			self.enumProperty(elem, 'frameShape', 'QFrame::Box')
		if 'bgColor' in self.widget.props:
			self.enumProperty(elem, 'displayAlarmStateOption', 'WhenInAlarm', {'stdset':'0'})
			self.property(elem, 'backgroundColor', 'bgColor', 'color')
			''' rgb = self.colors.getRGB(self.widget.props['bgColor'])
			if rgb is not None:
				subelem = etree.SubElement(elem, 'property', {'name':'canvasBackground'})
				brushelem = etree.SubElement(subelem, 'brush', {'brushstyle':'SolidPattern'})
				colorattr = {'alpha':'255'}
				if rgb.a is not None:
					colorattr.alpha = str(rgb.a)
				colorelem = etree.SubElement(brushelem, 'color', colorattr)
				redelem = etree.SubElement(colorelem, 'red')
				redelem.text = str(rgb.r)
				greenelem = etree.SubElement(colorelem, 'green')
				greenelem.text = str(rgb.g)
				blueelem = etree.SubElement(colorelem, 'blue')
				blueelem.text = str(rgb.b)
			'''
		#self.property(elem, 'triggerPv', 'triggerPv', 'unknowntype')
		#self.property(elem, 'autoScaleUpdateMs', 'autoScaleUpdateMs', 'unknowntype')
		self.property(elem, 'gridMajorColor', 'gridColor', 'color')
		self.property(elem, 'gridMinorColor', 'gridColor', 'color')
		#self.property(elem, 'lineThickness', 'lineThickness', 'unknowntype')
		#self.property(elem, 'traceCtlPv', 'traceCtlPv', 'unknowntype')
		#self.property(elem, 'nPts', 'nPts', 'unknowntype')
		self.property(elem, 'title', 'graphTitle', 'string')
		#self.property(elem, 'nPv', 'nPv', 'unknowntype')
		#self.property(elem, 'plotAreaBorder', 'plotAreaBorder', 'unknowntype')
		#self.property(elem, 'updateTimerMs', 'updateTimerMs', 'unknowntype')
		#self.property(elem, 'autoScaleThreshPct', 'autoScaleThreshPct', 'unknowntype')
		#self.property(elem, 'autoScaleBothDirections', 'autoScaleBothDirections', 'unknowntype')
		#self.property(elem, 'xPv', 'xPv', 'unknowntype')
		#self.property(elem, 'yPv', 'yPv', 'unknowntype')
		#self.property(elem, 'xSigned', 'xSigned', 'unknowntype')
		self.property(elem, 'gridEnableMajorX', 'xShowLabelGrid', 'boolean')
		self.property(elem, 'gridEnableMinorX', 'xShowMajorGrid', 'boolean')
		#self.property(elem, 'xShowMinorGrid', 'xShowMinorGrid', 'unknowntype')
		self.property(elem, 'xUnit', 'xLabel', 'string')
		#self.property(elem, 'xMax', 'xMax', 'unknowntype')
		#self.property(elem, 'xMajorsPerLabel', 'xMajorsPerLabel', 'unknowntype')
		#self.property(elem, 'xUserSpecScaleDiv', 'xUserSpecScaleDiv', 'unknowntype')
		#self.property(elem, 'xLabelIntervals', 'xLabelIntervals', 'unknowntype')
		#self.property(elem, 'xMin', 'xMin', 'unknowntype')
		#self.property(elem, 'xMinorsPerMajor', 'xMinorsPerMajor', 'unknowntype')
		#self.property(elem, 'showXAxis', 'showXAxis', 'unknowntype')
		#self.property(elem, 'xAxisSmoothing', 'xAxisSmoothing', 'unknowntype')
		#self.property(elem, 'xLablePrecision', 'xLablePrecision', 'unknowntype')

		''' Y axis(es): Only one Y axis in QEPlot, while EDM can do 2 '''
		if 'showYAxis' not in self.widget.props and 'showY2Axis' not in self.widget.props:
			self.booleanProperty(elem, 'axisEnableY', False)
		elif 'showYAxis' in self.widget.props and 'showY2Axis' in self.widget.props:
			self.logger.warn('QEPlot "%s": Y and Y2 axes will be combined into one.' % self.widgetName())
			# TODO: combine both y axes into one
			''' If either axis is auto-scaled, make this axis auto-scaled '''
			if ('yAxisSrc' in self.widget.props and self.widget.props['yAxisSrc'] == 'fromUser') \
				and ('y2AxisSrc' in self.widget.props and self.widget.props['y2AxisSrc'] == 'fromUser'):
				ymin = 0
				ymax = 1
				if 'yMin' in self.widget.props:
					ymin = float(self.widget.props['yMin'])
				if 'yMax' in self.widget.props:
					ymax = float(self.widget.props['yMax'])
				if 'y2Min' in self.widget.props:
					y2min = float(self.widget.props['y2Min'])
					if y2min < ymin:
						ymin = y2min
				if 'y2Max' in self.widget.props:
					y2max = float(self.widget.props['y2Max'])
					if y2max > ymax:
						ymax = y2max
				self.booleanProperty(elem, 'autoScale', False)
				self.doubleProperty(elem, 'yMin', ymin)
				self.doubleProperty(elem, 'yMax', ymax)
			ylabel = ''
			if 'yLabel' in self.widget.props and 'y2Label' in self.widget.props:
				ylabel = self.widget.props['yLabel']+' / '+self.widget.props['y2Label']
			elif 'yLabel' in self.widget.props:
				ylabel = self.widget.props['yLabel']
			elif 'y2Label' in self.widget.props:
				ylabel = self.widget.props['y2Label']
			self.stringProperty(elem, 'yUnit', ylabel)
		elif 'showY2Axis' in self.widget.props:
			''' Only Y2: map to primary Y '''
			self.yaxisUI(elem, 'y2')
		else:
			''' Only Y '''
			self.yaxisUI(elem, 'y')

		if 'yPv' in self.widget.props:
			i = 1
			for key, yPv in list(self.widget.props['yPv'].items()):
				self.stringProperty(elem, 'variable%d' % i, yPv)
				self.colorProperty(elem, 'traceColor%d' % i, self.widget.props['plotColor'][key])
				i += 1
				if i > 4:
					self.logger.warn('#Y variables exceeds 4; remaining variable(s) will be ignored')
					break

		#self.property(elem, 'yAxisPrecision', 'yAxisPrecision', 'unknowntype')
		#self.property(elem, 'yLabelIntervals', 'yLabelIntervals', 'unknowntype')
		#self.property(elem, 'yMax', 'yMax', 'unknowntype')
		self.property(elem, 'gridEnableMajorY', 'yShowLabelGrid', 'boolean')
		self.property(elem, 'gridEnableMinorY', 'yShowMajorGrid', 'boolean')
		#self.property(elem, 'yShowMinorGrid', 'yShowMinorGrid', 'unknowntype')
		#self.property(elem, 'yMinorsPerMajor', 'yMinorsPerMajor', 'unknowntype')
		#self.property(elem, 'yMin', 'yMin', 'unknowntype')
		#self.property(elem, 'ySigned', 'ySigned', 'unknowntype')
		#self.property(elem, 'showYAxis', 'showYAxis', 'unknowntype')
		#self.property(elem, 'yUserSpecScaleDiv', 'yUserSpecScaleDiv', 'unknowntype')
		#self.property(elem, 'yAxisSmoothing', 'yAxisSmoothing', 'unknowntype')
		#self.property(elem, 'yMajorsPerLabel', 'yMajorsPerLabel', 'unknowntype')
		#self.property(elem, 'showY2Axis', 'showY2Axis', 'unknowntype')
		#self.property(elem, 'useY2Axis', 'useY2Axis', 'unknowntype')
		#self.property(elem, 'y2MajorsPerLabel', 'y2MajorsPerLabel', 'unknowntype')
		#self.property(elem, 'y2AxisSmoothing', 'y2AxisSmoothing', 'unknowntype')
		#self.property(elem, 'y2Min', 'y2Min', 'unknowntype')
		#self.property(elem, 'y2AxisPrecision', 'y2AxisPrecision', 'unknowntype')
		#self.property(elem, 'y2UserSpecScaleDiv', 'y2UserSpecScaleDiv', 'unknowntype')
		#self.property(elem, 'y2LabelIntervals', 'y2LabelIntervals', 'unknowntype')
		#self.property(elem, 'y2ShowLabelGrid', 'y2ShowLabelGrid', 'unknowntype')
		#self.property(elem, 'y2ShowMajorGrid', 'y2ShowMajorGrid', 'unknowntype')
		#self.property(elem, 'y2ShowMinorGrid', 'y2ShowMinorGrid', 'unknowntype')
		#self.property(elem, 'y2Label', 'y2Label', 'unknowntype')
		#self.property(elem, 'y2MinorsPerMajor', 'y2MinorsPerMajor', 'unknowntype')
		#self.property(elem, 'y2Max', 'y2Max', 'unknowntype')
		#self.property(elem, 'numTraces', 'numTraces', 'unknowntype')
		#self.property(elem, 'fgColor', 'fgColor', 'color')

		return elem

	## Produces the XML for a y axis
	## @param elem the parent XML element
	## @axisname string The axis' name
	def yaxisUI(self, elem, axisname):
		if axisname+'AxisSrc' in self.widget.props and self.widget.props[axisname+'AxisSrc'] == 'fromUser':
			self.property(elem, 'yMin', axisname+'Min', 'float')
			self.property(elem, 'yMax', axisname+'Max', 'float')
			self.booleanProperty(elem, 'autoScale', False)
		self.property(elem, 'gridEnableMajorY', axisname+'ShowLabelGrid', 'boolean')
		self.property(elem, 'gridEnableMinorY', axisname+'ShowMajorGrid', 'boolean')
		#self.property(elem, 'yShowMinorGrid', 'yShowMinorGrid', 'unknowntype')
		self.property(elem, 'yUnit', axisname+'Label', 'string')
		#self.property(elem, 'yAxisPrecision', 'yAxisPrecision', 'unknowntype')
		#self.property(elem, 'yLabelIntervals', 'yLabelIntervals', 'unknowntype')
		#self.property(elem, 'yMinorsPerMajor', 'yMinorsPerMajor', 'unknowntype')
		#self.property(elem, 'ySigned', 'ySigned', 'unknowntype')
		#self.property(elem, 'showYAxis', 'showYAxis', 'unknowntype')
		#self.property(elem, 'yUserSpecScaleDiv', 'yUserSpecScaleDiv', 'unknowntype')
		#self.property(elem, 'yAxisSmoothing', 'yAxisSmoothing', 'unknowntype')
		#self.property(elem, 'yMajorsPerLabel', 'yMajorsPerLabel', 'unknowntype')

	def isBuiltInWidget(self):
		return False

	def isContainer(self):
		return False

	def widgetType(self):
		return 'QEPlot'

	def widgetName(self):
		return 'xygraph_%d' % xyGraphClass.count

	def widgetBaseClass(self):
		return 'QEFrame'

	def widgetHeader(self):
		return 'QEPlot.h'

	## Override of widgets.BaseWidget.customWidgetDef() to
	## also output the QwtPlot type
	def customWidgetDef(self, parent):
		elem = etree.SubElement(parent, 'customwidget')
		clselem = etree.SubElement(elem, 'class')
		clselem.text = 'QwtPlot'
		extelem = etree.SubElement(elem, 'extends')
		extelem.text = 'QFrame'
		hdrelem = etree.SubElement(elem, 'header')
		hdrelem.text = 'qwt_plot.h'
		elem = etree.SubElement(parent, 'customwidget')
		clselem = etree.SubElement(elem, 'class')
		clselem.text = self.widgetType()
		extelem = etree.SubElement(elem, 'extends')
		extelem.text = self.widgetBaseClass()
		hdrelem = etree.SubElement(elem, 'header')
		hdrelem.text = self.widgetHeader()
		return elem

