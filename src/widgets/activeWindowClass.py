###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
from lxml import etree as ElementTree
import src.widgets
import logging
from lxml import etree

class activeWindowClass(BaseWidget):
	''' Depending on the chosen framework and widget properties,
		produces either a QEPvFrame, a QEFrame, or a QFrame.
		This is the top-level widget.
	'''
	count = 0
	@staticmethod
	def incrcount():
		activeWindowClass.count += 1
		return activeWindowClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(activeWindowClass, self).__init__(widget)
		self.count = activeWindowClass.incrcount()

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''
		#self.property(elem, 'ctlFgColor2', 'ctlFgColor2', 'color')
		#self.property(elem, 'ctlFgColor1', 'ctlFgColor1', 'color')
		#self.property(elem, 'snapToGrid', 'snapToGrid', 'unknowntype')
		#self.property(elem, 'disableScroll', 'disableScroll', 'unknowntype')
		#self.property(elem, 'showGrid', 'showGrid', 'unknowntype')
		#self.property(elem, 'btnFont', 'btnFont', 'font')
		#self.property(elem, 'bgColor', 'bgColor', 'color')
		self.property(elem, 'font', 'font', 'font')
		#self.property(elem, 'title', 'title', 'unknowntype')
		#self.property(elem, 'textColor', 'textColor', 'color')
		#self.property(elem, 'gridSize', 'gridSize', 'unknowntype')
		#self.property(elem, 'topShadowColor', 'topShadowColor', 'color')
		#self.property(elem, 'orthoLineDraw', 'orthoLineDraw', 'unknowntype')
		#self.property(elem, 'pvType', 'pvType', 'unknowntype')
		#self.property(elem, 'ctlFont', 'ctlFont', 'font')
		#self.property(elem, 'ctlBgColor2', 'ctlBgColor2', 'color')
		#self.property(elem, 'ctlBgColor1', 'ctlBgColor1', 'color')
		#self.property(elem, 'botShadowColor', 'botShadowColor', 'color')
		#self.property(elem, 'fgColor', 'fgColor', 'color')

		''' If this is a template edm file, set macro names in variableSubstitutions.
			We don't have the macro values, so this just serves as a placeholder '''
		if 'templateParams' in self.widget.props:
			params = '=,'.join(list(self.widget.props['templateParams'].values()))+'='
			pelem = self.stringProperty(elem, 'variableSubstitutions', params)

		self.defaultStyle(elem, {'background-color':'bgColor', 'textColor':'color'})
		return elem

	def alignment(self, parent):
		''' Override of BaseWidget::alignment, because EDM allows
			fontAlign but Qt doesn't.  So, we output nothing.  Note
			that the default alignment for widgets in EDM is left even
			if the activeWindowClass sets it to center or right.
		'''
		pass

	def isBuiltInWidget(self):
		return self.widgetType() == 'QFrame'

	def isContainer(self):
		return True

	def widgetType(self):
		if self.framework() == 'EpicsQt':
			if 'templateParams' in self.widget.props or 'templateInfo' in self.widget.props:
				return 'QEPvFrame'
			return 'QEFrame'
		return 'QFrame'

	def widgetName(self):
		return 'frame_%d' % activeWindowClass.count

	def widgetBaseClass(self):
		if self.widgetType() == 'QEPvFrame':
			return 'QEFrame'
		elif self.widgetType() == 'QEFrame':
			return 'QFrame'
		return 'QWidget'

if __name__ == '__main__':
	top = activeWindowClass()
