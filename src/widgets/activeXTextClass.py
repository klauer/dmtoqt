###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree
import re

class activeXTextClass(BaseWidget):
	''' Depending on the widget properties and chosen framework, produces
		either a QESubstitutedLabel, a QLabel, or a caLabel
	'''

	count = 0
	@staticmethod
	def incrcount():
		activeXTextClass.count += 1
		return activeXTextClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(activeXTextClass, self).__init__(widget)
		self.count = activeXTextClass.incrcount()

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''

		if 'value' not in self.widget.props:
			self.logger.warn('%s: "value" property not set' % self.widgetName())

		''' Properties specific to caLabel: '''
		if self.framework() == 'caQtDM':
			if 'useDisplayBg' not in self.widget.props and 'bgColor' in self.widget.props:
				self.property(elem, 'background', 'bgColor', 'color')
			if 'fgColor' in self.widget.props:
				self.property(elem, 'foreground', 'fgColor', 'color')
				self.stringProperty(elem, 'colorMode', 'Static')
			if 'value' in self.widget.props:
				self.stringProperty(elem, 'text', "\n".join(list(self.widget.props['value'].values())))
		else:
			ss = self.widgetType()+' { '
			applyss = False
			if 'fgColor' in self.widget.props:
				applyss = True
				rgb = self.colors.getRGB(self.widget.props['fgColor'])
				ss += 'color: %s; ' % str(rgb)
			if 'useDisplayBg' not in self.widget.props and 'bgColor' in self.widget.props:
				applyss = True
				rgb = self.colors.getRGB(self.widget.props['bgColor'])
				ss += 'background-color: %s; ' % str(rgb)
			if applyss:
				ss += '}'
				self.stringProperty(elem, 'styleSheet', ss, {'notr':'true'})
			if self.widgetType() == 'QESubstitutedLabel' and 'value' in self.widget.props:
				self.stringProperty(elem, 'labelText', "\n".join(list(self.widget.props['value'].values())))
			elif 'value' in self.widget.props:
				self.stringProperty(elem, 'text', "\n".join(list(self.widget.props['value'].values())))

		''' QLabel properties (common to caLabel as well): '''
		''' Font needs to be set even if the same as top window, because it will likely
			get rescaled anyway, thereby overriding any bold/italic/etc. properties '''
		self.fontProperty(elem, 'font', self.widget.props['font'], force=True)

		self.property(elem, 'lineWidth', 'lineWidth', 'int')
		if 'border' in self.widget.props:
			self.stringProperty(elem, 'frameShape', 'QFrame::Box')

		''' Not sure what to do with these: '''
		#self.property(elem, 'alarmPv', 'alarmPv', 'string')
		#self.property(elem, 'fgAlarm', 'fgAlarm', 'unknowntype')
		#self.property(elem, 'useDisplayBg', 'useDisplayBg', 'unknowntype')
		#self.property(elem, 'bgAlarm', 'bgAlarm', 'unknowntype')


		self.endWidget(parent)
		return elem

	def isBuiltInWidget(self):
		return self.widgetType() == 'QLabel'

	def isContainer(self):
		return False

	def widgetType(self):
		if self.framework() == 'EpicsQt':
			if 'value' in self.widget.props:
				found = False
				re_macro = re.compile(r'.*\$\(.+\).*')
				for v in list(self.widget.props['value'].values()):
					m = re_macro.match(v)
					if m is not None:
						found = True
						break
				if found:
					return 'QESubstitutedLabel'
			return 'QLabel'
		return 'caLabel'

	def widgetName(self):
		return 'label_%d' % activeXTextClass.count

	def widgetBaseClass(self):
		if self.widgetType() == 'QLabel':
			return 'QWidget'
		return 'QLabel'
