###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class activeExitButtonClass(BaseWidget):
	''' This class is a stub; no actual output will go to the ui file '''

	count = 0
	@staticmethod
	def incrcount():
		activeExitButtonClass.count += 1
		return activeExitButtonClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(activeExitButtonClass, self).__init__(widget)
		self.count = activeExitButtonClass.incrcount()

	def widgetUI(self, parent):
		return None

		#self.property(elem, 'exitProgram', 'exitProgram', 'boolean')
		#self.property(elem, 'bgColor', 'bgColor', 'color')
		''' apply to parent '''
		#self.property(elem, 'controlParent', 'controlParent', 'boolean')
		#self.property(elem, 'label', 'label', 'string')
		#self.property(elem, 'topShadowColor', 'topShadowColor', 'color')
		#self.property(elem, 'iconify', 'iconify', 'boolean')
		#self.property(elem, 'botShadowColor', 'botShadowColor', 'color')
		#self.property(elem, 'font', 'font', 'font')
		#self.property(elem, 'invisible', 'invisible', 'boolean')
		#self.property(elem, 'fgColor', 'fgColor', 'color')
		#self.property(elem, '3d', '3d', 'boolean')

		#return elem

	def isBuiltInWidget(self):
		''' Pretend this is a built-in widget so the custom widget def doesn't get written '''
		return True

	def isContainer(self):
		return False

	def widgetType(self):
		pass

	def widgetName(self):
		return 'qeactiveExitButtonClass_%d' % activeExitButtonClass.count

	def widgetBaseClass(self):
		pass

	def widgetHeader(self):
		pass
