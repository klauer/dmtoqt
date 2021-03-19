'''
.. module:: UIWriter
	:synopsis: Defines the UIWriter class for writing to a Qt UI file.
'''

###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
import logging
from src.widgets.BaseWidget import BaseWidget
from src.widgets.activeWindowClass import activeWindowClass
from ColorsParser import ColorsParser
from imp import load_source
from lxml import etree
import sys

class UIWriter:

	def __init__(self, ofilename):
		''' Constructor

		Args:
			ofilename (string): The output file name
		'''
		self.logger = logging.getLogger('UIWriter')
		self.ofilename = ofilename

	def setColors(self, colorsParser):
		''' Set the ColorsParser object

		Args:
			colorsParser (ColorsParser): The colors parser object
		'''
		self.colors = colorsParser

	def write(self, reader):
		''' Writes the ui-specific xml to self.ofilename.

		Args:
			reader (src.DMReader.DMReader): instance holding the properties read from an EDM file

		Returns:
			boolean: True on success, False otherwise
		'''
		self.customwidgetdefs = {}
		self.topWidget = activeWindowClass(reader.mainWidget)
		self.customwidgetdefs['activeWindowClass'] = self.topWidget
		root = etree.Element('ui', {'version': '4.0'})
		classelem = etree.SubElement(root, 'class')
		if 'title' in reader.mainWidget.props:
			classelem.text = reader.mainWidget.props['title']
		else:
			classelem.text = self.ofilename
		for widget in reader.widgets:
			widget.adjustChildGeometries()
		self.topWidget.setColors(self.colors)
		topelem = self.topWidget.widgetUI(root)

		self.logger.info('Writing %d widget(s)' % len(reader.widgets))
		if not self.writeWidgets(self.topWidget, topelem, reader.widgets):
			self.logger.critical('Failed to write widgets')
			return False
		self.logger.info('Wrote %d widget(s)' % len(reader.widgets))

		parent = etree.SubElement(root, 'customwidgets')
		for cw in list(self.customwidgetdefs.values()):
			subelem = cw.customWidgetDef(parent)

		et = etree.ElementTree(root)
		et.write(self.ofilename, pretty_print=True, xml_declaration=True, encoding="UTF-8")
		return True

	def writeWidgets(self, topWidget, parentelem, children):
		''' Write the widgets.

			Internal function, not intended to be called from outside this class.
			May be called recursively if any children have their own children

		Args:
			topWidget (src.EDMWidget.EDMWidget): The top-level widget (used in determining font)
			parentelem (lxml.etree.elem): The parent XML element
			children ([src.EDMWidget.EDMWidget]): One or more child widgets

		Returns:
			boolean: True on success; False if an error occurs
		'''
		for widget in children:
			#widget.adjustChildGeometries()
			result = self.writeWidget(topWidget, widget, parentelem)
			if result is None:
				self.logger.critical('Failed to write widget')
				return False
			(wout, elem) = result
			if widget.hasChildren():
				''' Recursive call '''
				if not self.writeWidgets(wout, elem, widget.children):
					self.logger.critical('Failed to write child widgets')
					return False

		return True

	def writeWidget(self, topWidget, widget, parentelem):
		''' Write a single widget.

			Internal function, not intended to be called from outside this class.

			Uses the python load_source mechanism to load the widget type from the
			## widgets subdirectory, using the EDM widget type as the python file name.
			## This allows implementing new EDM widget types by adding appropriately named
			## python files to the widgets subdirectory.

		Args:
			 topWidget (src.EDMWidget.EDMWidget): The top-level widget (used in determining font)
			 widget (src.EDMWidget.EDMWidget): The widget to be written
			 parentelem (lxml.etree.elem): The parent XML element

		Returns:
			tuple: The ouput widget is the first element; the etree.elem returned from the widget's widgetUI method is the second element. None may be returned on a critical error.
		'''
		self.logger.debug('Widget type %s..' % widget.type)
		if widget.type not in list(self.customwidgetdefs.keys()):
			try:
				load_source('src.widgets', 'src/widgets/%s.py' % widget.type)
				import src.widgets
				wout = eval('src.widgets.'+widget.type+"(widget)", globals(), locals())
				if not wout:
					self.logger.critical('Cannot create object of type %s' % widget.type)
					return None
			except Exception as e:
				self.logger.critical('Exception writing widget type %s: %s' % (widget.type, e))
				return None
			self.customwidgetdefs[widget.type] = wout
		else:
			import src.widgets
			wout = eval('src.widgets.'+widget.type+'(widget)', globals(), locals())
		wout.setColors(self.colors)
		wout.setTopWidget(topWidget)
		welem = wout.widgetUI(parentelem)
		if welem is None:
			self.logger.warn('widgetUI returned None for type %s; this widget will not be rendered in the ui file.' % widget.type)
		return (wout, welem)
