###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class StackWidget(BaseWidget):
	''' Because of the semantics of QESimpleShape, the visibility properties
		of EDM widgets must fit a very specific set of constraints to use this
		class:

		- Same geometry, same class name (e.g. activeCircleClass)
		- Same visPv
		- 0 <= visMin <= 16, or, if visInvert is True, 0 <= visMax <= 16
		- no 2 visMin properties can be the same

		If all these conditions are not met, this class will not be used and
		separate widgets will be created.

		Even with this, there will be cases where the EDM properties cannot be
		reproduced very well, so buyer beware.

		Categories of EDM widgets that may be stacked:

		1.  Shapes (circles, rectangles) all assigned to the same pv with visibility
		dependent on different value ranges.  These can be reproduced with this class
		if the values are integers and 0-15; otherwise more work is needed.

		2.  Shapes assigned to different pvs, with visibility dependent on value ranges of
		those pvs.  These cannot be reproduced exactly with this class so a warning will
		be printed and all pvs will be concatenated into the variable property.

		3.  Labels with different text/colors dependent on a pv value.  These can be reproduced
		fairly well; however it is better to set up the pv with a proper enumeration.
		While a working label will be produced with a local enumeration, a warning will
		be printed.  Note colors will not change; this should really be handled by alarm
		limits on the pv.
	'''

	count = 0
	@staticmethod
	def incrcount():
		StackWidget.count += 1
		return StackWidget.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(StackWidget, self).__init__(widget)
		self.count = StackWidget.incrcount()

	def widgetUI(self, parent):

		''' Adjust w, h to max of contained labels '''
		if self.widget.stackType() == 'labels':
			w = int(self.widget.geometry['w'])
			h = int(self.widget.geometry['h'])
			for s in self.widget.stack:
				if int(s.geometry['w']) > w:
					w = int(s.geometry['w'])
				if int(s.geometry['h']) > h:
					h = int(s.geometry['h'])
			self.widget.geometry['w'] = str(w)
			self.widget.geometry['h'] = str(h)

		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''

		alarmpv = None
		alarmpvs = []
		vispv = None
		visMin = None
		visMax = None
		visInvert = None
		vispvs = []
		visMins = []
		visMaxs = []
		visInverts = []
		for w in self.widget.stack:
			if 'alarmPv' in w.props and w.props['alarmPv'] != '':
				if alarmpv is None:
					alarmpv = w.props['alarmPv']
				elif alarmpv != w.props['alarmPv']:
					alarmpvs.append(w.props['alarmPv'])
			if 'visPv' in w.props and w.props['visPv'] != '':
				if vispv is None:
					vispv = w.props['visPv']
					if 'visMin' in w.props:
						visMin = w.props['visMin']
					else:
						visMin = 'na'
					if 'visMax' in w.props:
						visMax = w.props['visMax']
					else:
						visMax = 'na'
					visInvert = str('visInvert' in w.props)
				elif vispv != w.props['visPv']:
					vispvs.append(w.props['visPv'])
					if 'visMin' in w.props:
						visMins.append(w.props['visMin'])
					else:
						visMins.append('na')
					if 'visMax' in w.props:
						visMaxs.append(w.props['visMax'])
					else:
						visMaxs.append('na')
					visInverts.append(str('visInvert' in w.props))

		if len(alarmpvs) > 1:
			self.logger.warn('Widget stack of %d widgets contains more than one alarmPv.  You must fix this manually in your .ui file.  The pvs will be listed in a property of the widget called "alarmPvs".' % (len(self.widget.stack)))
			alarmpvs.insert(0, alarmpv)
			self.stringListProperty(elem, 'alarmPvs', alarmpvs)
		if len(vispvs) > 0:
			self.logger.warn('Widget stack of %d widgets contains more than one visPv.  You must fix this manually in your .ui file.  The pvs will be listed in a property of the widget called "visPvs", along with the visMin/visMax properties for each.' % (len(self.widget.stack)))
			vispvs.insert(0, vispv)
			self.stringListProperty(elem, 'visPvs', vispvs)
			visMins.insert(0, visMin)
			self.stringListProperty(elem, 'visMins', visMins)
			visMaxs.insert(0, visMax)
			self.stringListProperty(elem, 'visMaxs', visMaxs)
			visInverts.insert(0, visInvert)
			self.stringListProperty(elem, 'visInverts', visInverts)

		if vispv is not None:
			self.stringProperty(elem, 'variable', vispv)
		elif alarmpv is not None:
			self.stringProperty(elem, 'variable', alarmpv)

		first = self.widget.firstWidget
		if self.widget.stackType() == 'labels':
			''' Can't use self.property.. '''
			if 'font' in first.props:
				self.fontProperty(elem, 'font', first.props['font'])
			enums = []
			min = 0
			max = 1
			for w in self.widget.stack:
				if 'visMin' in w.props:
					min = float(w.props['visMin'])
				if 'visMax' in w.props:
					max = float(w.props['visMax'])
				visInvert = 'visInvert' in w.props
				txt = ''
				if 'value' in w.props:
					txt = '\n'.join(list(w.props['value'].values()))
				enums.append((txt, min, max, visInvert))
				if 'visMin' not in w.props:
					min = max
				if 'visMax' not in w.props:
					max += 1
			enums = sorted(enums, key=lambda enum: enum[1])
			strgs = []
			for e in enums:
				if e[3]:
					strgs.append('<%g:"%s",>=%g:"%s"' % (e[1], e[0], e[2], e[0]))
				else:
					strgs.append('%g:"%s",<%g:"%s"' % (e[1], e[0], e[2], e[0]))

			strg = ','.join(strgs)
			self.stringProperty(elem, 'localEnumeration', strg, {'notr':'true'})
			self.enumProperty(elem, 'format', 'LocalEnumeration')

			lineWidth = 1
			if 'lineWidth' in first.props:
				lineWidth = int(first.props['lineWidth'])
			if 'border' in first.props and lineWidth >= 1:
				self.enumProperty(elem, 'frameShape', 'Box')
				self.intProperty(elem, 'lineWidth', lineWidth)

			if 'fillColor' in self.widget.firstWidget.props:
				applyBg = True
				bgcolor = self.widget.firstWidget['fillColor']
				for w in self.widget.stack:
					if 'useDisplayBg' in w.props:
						applyBg = False
						break
					if 'fillColor' in w.props:
						if w.props['fillColor'] != bgcolor:
							applyBg = False
							break
				if applyBg:
					ss = self.widgetType()+' { background-color: %s; }' % self.colors.getRGB(bgcolor)
					self.stringProperty(elem, 'defaultStyle', ss, {'notr':'true'})

			self.enumProperty(elem, 'displayAlarmStateOption', 'WhenInAlarm')
			self.intProperty(elem, 'indent', 0)

		else: # 'shapes'
			shape = 'circle'
			if first.type == 'activeCircleClass':
				shape = 'circle'
			else: # rectangle, or label
				shape = 'rectangle'
			self.enumProperty(elem, 'shape', shape)

			if 'lineWidth' in first.props:
				self.intProperty(elem, 'edgeWidth', first.props['lineWidth'])
			if 'edgeColour' in first.props:
				self.colorProperty(elem, 'edgeColour', first.props['lineColor'])
			# Turn off alarm display only if vispv or alarmpv was not found
			if vispv is None and alarmpv is None and 'lineAlarm' not in first.props:
				self.enumProperty(elem, 'edgeAlarmStateOption', 'WhenInAlarm')
			if vispv is None and alarmpv is None and 'fillAlarm' not in first.props:
				self.enumProperty(elem, 'displayAlarmStateOption', 'WhenInAlarm')

			min = 0
			max = 1
			for w in self.widget.stack:
				if 'visMin' in w.props:
					min = int(float(w.props['visMin']))
				if 'visMax' in w.props:
					max = int(float(w.props['visMax']))
				if max < 0 or min > 15:
					continue
				if min < 0: min = 0
				if max > 16: max = 16
				for i in range(min, max):
					if 'fillColor' in w.props:
						self.colorProperty(elem, 'colour%d' % i, w.props['fillColor'])
					elif 'lineColor' in w.props:
						self.colorProperty(elem, 'colour%d' % i, w.props['lineColor'])

		self.endWidget(elem)
		return elem

	def isBuiltInWidget(self):
		return False

	def isContainer(self):
		return False

	def widgetType(self):
		if self.widget.stackType() == 'labels':
			return 'QELabel'
		return 'QESimpleShape'

	def widgetName(self):
		return 'stack_%d' % StackWidget.count

	def widgetBaseClass(self):
		if self.widget.stackType() == 'labels':
			return 'QLabel'
		return 'QSimpleShape'
