## This file provides a starting point for defining a new widget type.
## To create a new widget type, copy this file to "widgets/widgetclassname.py",
## where widgetclassname is edm's "object" property.  Then replace
## "widget_template" everywhere it appears with widgetclassname, and
## implement the methods.
## Also, see :module:`findEDMProps.py`
###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################

from src.widgets.BaseWidget import BaseWidget
import src.widgets
import logging
from lxml import etree

class widget_template(BaseWidget):

	## Number of widgets of this type created so far; used in widgetName()
	count = 0

	@staticmethod
	def incrcount():
		''' Increments the static count variable and returns the
			result, so it can be used as an instance variable.
		'''
		widget_template.count += 1
		return widget_template.count

	def __init__(self, widget):
		''' Initializes the widget instance.  Sets the instance variables
			self.logger and self.count, and calls the super class ctor.
		'''
		self.logger = logging.getLogger(self.__class__.__name__)
		super(widget_template, self).__init__(widget)
		self.count = widget_template.incrcount()

	def widgetUI(self, parent):
		''' EDM Properties for this class

			This lists all EDM properties specific to this class,
			to be used in the widget class' widgetUI method.
			Paste this code into your widgetUI method, then
			adjust it to map to the appropriate Qt properties

			self.property arguments::

			* uiname: Qt name for the property
			* propname: EDM name, in self.widget.props
			* type: 'int', 'string', 'color', 'boolean'
		'''
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''
widget_properties

		self.endWidget(elem)
		return elem

	def isBuiltInWidget(self):
		''' True if this is a standard, Qt-provided widget.
			Most widgets will override this to return False.
		'''
		return False

	def isContainer(self):
		''' True if this is a container widget, e.g. QFrame '''
		return False

	def widgetType(self):
		''' The widget type to appear in the ui file, e.g. QELabel.
			Must be overridden.
		'''
		pass

	def widgetName(self):
		''' The name of this widget instance, e.g. "qelabel_1".

			Must be unique in the UI file, so the convention is to
			increment the trailing number for each widget.

			Must be overridden.
		'''
		return 'qewidget_template_%d' % widget_template.count

	def widgetBaseClass(self):
		''' The base class name of the widget, from Qt Designer's
			perspective, e.g. "QLabel".
			Must be overridden.
		'''
		pass
