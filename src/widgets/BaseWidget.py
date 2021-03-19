###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################

import logging
from lxml import etree
import re
from src.ColorsParser import RGB

class BaseWidget(object):
	''' The base class for all widgets.  Defines several helper functions
		to make writing new widget classes easy.
	'''

	# Possible values for supported frameworks
	frameworks = ['EpicsQt', 'caQtDM']

	def __init__(self, widget):
		''' Constructor

		Args:
			widget (EDMWidget): the EDMWidget instance
		'''
		self.widget = widget
	
	def setColors(self, colors):
		''' Set a ColorsParser object for the colors; these
			may be used to generate the widget configuration.

		Args:
			colors (ColorsParser): a ColorsParser instance
		'''
		self.colors = colors

	def setTopWidget(self, topWidget):
		''' Set the top widget instance

		Args:
			topWidget (src.widgets.activeWindowClass.activeWindowClass): an activeWindowClass instance
		'''
		self.topWidget = topWidget

	def property(self, elem, uiname, edmname, type):
		''' Map an EDM property name/value to the Qt equivalent,
			if the EDM property is set.

			Does nothing if the property does not appear in the .edl file.
			Uses the appropriate member xxxProperty function according to
			the type parameter, mapping the property name from edmname
			to uiname.

		Args:
			elem (lxml.etree.elem): The parent XML element
			uiname (string): The property name in Qt
			edmname (string): The property name in EDM
			type (string): The type of this parameter.  Possible values:

				* int
				* float
				* number
				* string
				* stringList
				* boolean
				* set
				* color
				* font

		Returns:
			lxml.etree.elem: The created XML sub element, or None if an error occurs
		'''
		subelem = None
		if type == 'unknowntype':
			return subelem
		if edmname in list(self.widget.props.keys()):
			prop = self.widget.props[edmname]
			if type == 'int':
				subelem = self.intProperty(elem, uiname, prop)
			elif type == 'float':
				subelem = self.doubleProperty(elem, uiname, prop)
			elif type == 'number':
				subelem = self.numberProperty(elem, uiname, prop)
			elif type == 'string':
				subelem = self.stringProperty(elem, uiname, prop)
			elif type == 'stringList':
				subelem = self.stringListProperty(elem, uiname, prop)
			elif type == 'boolean':
				subelem = self.booleanProperty(elem, uiname, prop)
			elif type == 'set':
				subelem = self.setProperty(elem, uiname, prop)
			elif type == 'color':
				subelem = self.colorProperty(elem, uiname, prop)
			elif type == 'font':
				subelem = self.fontProperty(elem, uiname, prop)
			else:
				self.logger.warn('Unknown type for property "%s"("%s"); skipping' % (edmname, uiname))
				return None
			if subelem is None:
				self.logger.warn('Failed to write property "%s"("%s")' % (edmname, uiname))
		return subelem

	def stringProperty(self, elem, name, value, txtattrs={}):
		''' Maps a property as a string

		Args:
			elem (lxml.etree.elem): The parent XML element
			name (string): The name of the property as seen in Qt Designer
			value (string): The value
			txtattrs (dict): (optional) Text attributes to apply to the property, e.g. {"notr":"true"} to turn off translation

		Returns:
			lxml.etree.elem: The created XML sub element
		'''
		subelem = etree.SubElement(elem, 'property', {'name': name})
		strelem = etree.SubElement(subelem, 'string', txtattrs)
		''' Any ampersands must be doubled so that Qt displays them correctly '''
		strelem.text = value.replace('&', '&&')
		return subelem

	def stringListProperty(self, elem, name, values):
		''' Maps a property as a list of strings.

		Args:
			elem (lxml.etree.elem): The parent XML element
			name (string): The name of the property as seen in Qt Designer
			values ([string]): The value(s)

		Returns:
			lxml.etree.elem: The created XML sub element
		'''
		subelem = etree.SubElement(elem, 'property', {'name':name})
		slelem = etree.SubElement(subelem, 'stringList')
		for s in values:
			selem = etree.SubElement(slelem, 'string')
			''' Any ampersands must be doubled so that Qt displays them correctly '''
			selem.text = s.replace('&', '&&')
		return subelem

	def intProperty(self, elem, name, value):
		''' Maps a property as a integer.

		Args:
			elem (lxml.etree.elem): The parent XML element
			name (string): The name of the property as seen in Qt Designer
			value (integer): The value

		Returns:
			lxml.etree.elem: The created XML sub element
		'''
		subelem = etree.SubElement(elem, 'property', {'name': name})
		strelem = etree.SubElement(subelem, 'number')
		strelem.text = str(int(float(value)))
		return subelem

	def doubleProperty(self, elem, name, value):
		''' Maps a property as a double.

		Args:
			elem (lxml.etree.elem): The parent XML element
			name (string): The name of the property as seen in Qt Designer
			value (float): The value

		Returns:
			lxml.etree.elem: The created XML sub element
		'''
		subelem = etree.SubElement(elem, 'property', {'name': name})
		strelem = etree.SubElement(subelem, 'double')
		strelem.text = str(float(value))
		return subelem

	def numberProperty(self, elem, name, value):
		''' Maps a property as a generic number.

		Args:
			elem (lxml.etree.elem): The parent XML element
			name (string): The name of the property as seen in Qt Designer
			value (int, float, or string): The value

		Returns:
			lxml.etree.elem: The created XML sub element
		'''
		subelem = etree.SubElement(elem, 'property', {'name': name})
		strelem = etree.SubElement(subelem, 'number')
		strelem.text = str(value)
		return subelem

	def booleanProperty(self, elem, name, value):
		''' Maps a property as a boolean.

		Args:
			elem (lxml.etree.elem): The parent XML element
			name (string): The name of the property as seen in Qt Designer
			value (boolean): The value

		Returns:
			lxml.etree.elem: The created XML sub element
		'''
		subelem = etree.SubElement(elem, 'property', {'name': name})
		strelem = etree.SubElement(subelem, 'bool')
		strelem.text = str(value).lower()
		return subelem

	def setProperty(self, elem, name, value):
		''' Maps a property as a set.

		Args:
			elem (lxml.etree.elem): The parent XML element
			name (string): The name of the property as seen in Qt Designer
			value (string): The value

		Returns:
			lxml.etree.elem: The created XML sub element
		'''
		subelem = etree.SubElement(elem, 'property', {'name': name})
		strelem = etree.SubElement(subelem, 'set')
		strelem.text = str(value).lower()
		return subelem

	def enumProperty(self, elem, name, value, attrs={}):
		''' Maps a property as an enumeration.

			This is used for properties that can be selected from a dropdown list
			in Qt Designer.  Internally the property values are defined by the
			Qt widget as a C enum type, so the value must match a known member
			of the enum.

		Args:
			elem (lxml.etree.elem): The parent XML element
			name (string): The name of the property as seen in Qt Designer
			value (string): The value
			attrs (dict): (optional) Text attributes to apply to the property, e.g. {"stdset":"false"} to
			indicate a non-standard property.

		Returns:
			lxml.etree.elem: The created XML sub element
		'''
		attrs['name'] = name
		subelem = etree.SubElement(elem, 'property', attrs)
		strelem = etree.SubElement(subelem, 'enum')
		strelem.text = str(value)
		return subelem

	def colorProperty(self, elem, name, value):
		''' Maps a property as a color.

			See: :class:`src.ColorsParser`

		Args:
			elem (lxml.etree.elem): The parent XML element
			name (string): The name of the property as seen in Qt Designer
			value (string): The value

		Returns:
			lxml.etree.elem: The created XML sub element, or None if an error occurs
		'''
		if value == 'transparent':
			rgb = RGB(65535, 65535, 65535, 0)
		else:
			rgb = self.colors.getRGB(value)
		if isinstance(rgb, str):
			self.logger.warn('Color returned from getRGB is a string "%s"; setting property %s as a string' % (rgb, name))
			return self.stringProperty(elem, name, value)
		elif rgb is None:
			self.logger.warn('getRGB returned None for property %s; skipping' % name)
			return None
		subelem = etree.SubElement(elem, 'property', {'name': name})
		colorattr = {}
		if rgb.a is not None:
			colorattr = {'alpha': str(rgb.a)}
		colorelem = etree.SubElement(subelem, 'color', colorattr)
		redelem = etree.SubElement(colorelem, 'red')
		redelem.text = str(rgb.r)
		greenelem = etree.SubElement(colorelem, 'green')
		greenelem.text = str(rgb.g)
		blueelem = etree.SubElement(colorelem, 'blue')
		blueelem.text = str(rgb.b)
		return subelem

	def fontProperty(self, elem, name, value, topName=None, force=False):
		''' Maps a property as a font.

			Normally EDM sets font properties like "index xx", where xx is an integer.
			In this case the ColorsParser class is used to map to a font name, point size, and
			attributes.

			If the font matches the top widget's font, by default nothing will be output
			to simplify the .ui file.  This can be overridden by setting force=True.
			The value of the top widget's font is determined by looking for self.widget.props[name];
			if topName is not None it will override name.

		Args:
			elem (lxml.etree.elem): The parent XML element
			name (string): The name of the property as seen in Qt Designer
			value (string): The value
			topName (string): (optional) Top widget's font property name, if different from name
			force (boolean): (optional) True to force writing of font property even if it matches the top widget's font

		Returns:
			lxml.etree.elem: The created XML sub element, or True if the font matches	the top widget and was not written.
		'''
		if not force and 'topWidget' in self.__dict__:
			if topName is None:
				topName = name
			if topName in self.topWidget.widget.props:
				topFont = self.topWidget.widget.props[topName]
				if topFont == value:
					return True # don't write font if already at top level

		# family-weight-type-points
		re_font = re.compile(r'([^-]+)-([^-]+)-([^-]+)-([0-9.]+)')
		m = re_font.match(value)
		if m is None:
			self.logger.warn('Property %s: Ignoring unexpected font value: "%s"' % (name, value))
			return None
		family = 'Sans Serif'
		if m.group(1) == 'helvetica' or m.group(1) == 'utopia':
			pass
		elif m.group(1) == 'new century schoolbook' or m.group(1) == 'times':
			family = 'Serif'
		elif m.group(1) == 'courier':
			family = 'Fixed'
		else:
			self.logger.warn('Property %s: Unrecognized font family, falling back to Serif ("%s")' % (name, value))

		bold = italic = underline = strikeout = False
		''' EDM fonts are heavier than Qt's, so ignore bold '''
		'''if m.group(2) == 'bold':
			bold = True'''
		if m.group(3) == 'i':
			italic = True

		pointsize = int(round(float(m.group(4))))
		''' Fudge: font appear to work better if scaled 2/3 '''
		if pointsize > 6:
			pointsize = int(pointsize*2/3 + 0.5)

		subelem = etree.SubElement(elem, 'property', {'name': name})
		fontelem = etree.SubElement(subelem, 'font')
		familyelem = etree.SubElement(fontelem, 'family')
		familyelem.text = family
		pointsizeelem = etree.SubElement(fontelem, 'pointsize')
		pointsizeelem.text = str(pointsize)
		boldelem = etree.SubElement(fontelem, 'bold')
		boldelem.text = str(bold).lower()
		italicelem = etree.SubElement(fontelem, 'italic')
		italicelem.text = str(italic).lower()
		underlineelem = etree.SubElement(fontelem, 'underline')
		underlineelem.text = str(underline).lower()
		strikeoutelem = etree.SubElement(fontelem, 'strikeout')
		strikeoutelem.text = str(strikeout).lower()

		return subelem

	def pointProperty(self, elem, name, x, y):
		''' Maps a property as a point (x-y pair).
			Used, for example, in QEShape with name = "point1", "point2", ... "point10"

		Args:
			elem (lxml.etree.elem): The parent XML element
			name (string): The name of the property as seen in Qt Designer
			x (int or string): The x-coordinate
			y (int or string): The y-coordinate

		Returns:
			lxml.etree.elem: The created XML sub element
		'''
		subelem = etree.SubElement(elem, 'property', {'name':name, 'stdset':'0'})
		ptelem = etree.SubElement(subelem, 'point')
		xelem = etree.SubElement(ptelem, 'x')
		xelem.text = str(x)
		yelem = etree.SubElement(ptelem, 'y')
		yelem.text = str(y)
		return subelem

	def startWidget(self, parent):
		''' Helper to simplify ui output for custom widgets.  Call
			this from your widget's widgetUI method.

		Args:
			parent (lxml.etree.elem): the parent XML element

		Returns:
			lxml.etree.elem: The created XML sub element
		'''
		self._widgetelem = etree.SubElement(parent, 'widget', {'class': self.widgetType(), 'name': self.widgetName()})
		self.geometry(self._widgetelem)
		self.alignment(self._widgetelem)
		self.visPvUI(self._widgetelem)
		return self._widgetelem

	def endWidget(self, parent):
		''' Finish the widget.  Currently does nothing

		Args:
			parent (lxml.etree.elem): the parent XML element

		Returns:
			lxml.etree.elem: parent
		'''
		return parent

	def alignment(self, parent):
		''' Set the font alignment property.
			Called from BaseWidget.startWidget; normally you should not need this method.

		Args:
			parent (lxml.etree.elem): The parent XML element
		'''
		if 'fontAlign' not in self.widget.props:
			return
		subelem = etree.SubElement(parent, 'property', {'name': 'alignment'})
		setelem = etree.SubElement(subelem, 'set', {'notr': 'true'})
		fa = self.widget.props['fontAlign']
		value = 'Qt::AlignLeft|Qt::AlignVCenter'
		if fa == 'center':
			value = 'Qt::AlignCenter'
		elif fa == 'right':
			value = 'Qt::AlignRight|Qt::AlignVCenter'
		setelem.text = value

	def geometry(self, parent):
		''' Helper to simplify ui output for custom widgets.  Called
			from BaseWidget.startWidget; normally you should not need this method.

		Args:
			parent (lxml.etree.elem): The parent XML element

		Returns:
			lxml.etree.elem: The created XML sub element
		'''
		subelem = etree.SubElement(parent, 'property', {'name': 'geometry'})
		rectelem = etree.SubElement(subelem, 'rect')
		xelem = etree.SubElement(rectelem, 'x')
		xelem.text = self.widget.geometry['x']
		yelem = etree.SubElement(rectelem, 'y')
		yelem.text = self.widget.geometry['y']
		welem = etree.SubElement(rectelem, 'width')
		welem.text = self.widget.geometry['w']
		helem = etree.SubElement(rectelem, 'height')
		helem.text = self.widget.geometry['h']
		return subelem

	def defaultStyle(self, parent, props={'background-color':'bgColor', 'color':'fgColor'}, pressedprops={}):
		''' Set the defaultStyle property.
			This is a property commonly used in EpicsQt widgets that is
			interpreted as a stylesheet.

		Args:
			parent (lxml.etree.elem): The XML element parent
			props (dict): A dictionary of stylesheetprop=>edmprop names
			pressedprops (dict): A dictionary of stylesheetprop=>edmprop names to be applied like "widgetType():pressed {}"

		Returns:
			boolean: True if the property was written, False otherwise.
		'''
		ss = self.widgetType()+' { '
		applyss = False
		for ssprop, edmprop in list(props.items()):
			if edmprop in self.widget.props:
				applyss = True
				if ssprop.endswith('color'):
					rgb = self.colors.getRGB(self.widget.props[edmprop])
					ss += '%s: %s; ' % (ssprop, str(rgb))
				else:
					ss += '%s: %s; ' % (ssprop, self.widget.props[edmprop])
		pressedss = self.widgetType()+':pressed { '
		applypressedss = False
		for ssprop, edmprop in list(pressedprops.items()):
			if edmprop in self.widget.props:
				applypressedss = True
				if ssprop.endswith('color'):
					rgb = self.colors.getRGB(self.widget.props[edmprop])
					ss += '%s: %s; ' % (ssprop, str(rgb))
				else:
					ss += '%s: %s; ' % (ssprop, self.widget.props[edmprop])
		if applypressedss:
			ss += '} %s }' % pressedss
			self.booleanProperty(parent, 'checkable', True)
		elif applyss:
			ss += '}'
		if applyss:
			self.stringProperty(parent, 'defaultStyle', ss, {'notr':'true'})
		return applyss

	def customWidgetDef(self, parent):
		''' Write the custom widget definition.
			This function must be called once for each widget type, not
			once per widget instance, to output the custom widget's name,
			base type, and header file in C.
			While new widget types do not need this function, they do need
			to implement the widgetType(), widgetBase(), and widgetHeader() functions
			that are used here.

		Args:
			parent (lxml.etree.elem): The parent XML element

		Returns:
			lxml.etree.elem: The created XML subelement
		'''
		if self.isBuiltInWidget():
			return None
		elem = etree.SubElement(parent, 'customwidget')
		clselem = etree.SubElement(elem, 'class')
		clselem.text = self.widgetType()
		extelem = etree.SubElement(elem, 'extends')
		extelem.text = self.widgetBaseClass()
		hdrelem = etree.SubElement(elem, 'header')
		hdrelem.text = self.widgetHeader()
		if self.isContainer():
			ctrelem = etree.SubElement(elem, 'container')
			ctrelem.text = '1'
		return elem

	def visPvUI(self, elem):
		''' Does nothing if the output widget type is not a CaQtDM widget,
			or if 'visPv' is not in self.widget.props.

			Handles the EDM properties:
			visPv, visMin, visMax, visInvert

			Writes the Qt properties:
			channel, visibilityCalc, visibility

		Args:
			elem (lxml.etree.elem): The parent XML element
		'''
		if self.framework() != 'caQtDM':
			return
		if not 'visPv' in self.widget.props:
			return

		self.stringProperty(elem, 'channel', self.widget.props['visPv'], {'notr':'true'})
		min = max = '0'
		if 'visMin' in self.widget.props:
			min = self.widget.props['visMin']
		if 'visMax' in self.widget.props:
			max = self.widget.props['visMax']
		calc = '(A>=%s)&&(A<%s)' % (min, max)
		if 'visInvert' in self.widget.props:
			calc = '(A<%s)||(A>%s)' % (min, max)
		self.stringProperty(elem, 'visibilityCalc', calc, {'notr':'true'})
		self.enumProperty(elem, 'visibility', 'Calc')

	def framework(self):
		''' Determine the current Qt Widget framework.
			Uses BaseWidget.frameworks, which is set according to the command line
			argument -f/--framework, to determine the most appropriate framework
			to use for the current widget.  Prefers EpicsQt, unless both frameworks
			may be used and self.widget.props['visPv'] is set.

		Returns:
			string: The current widget framework
		'''
		if 'EpicsQt' in BaseWidget.frameworks and 'caQtDM' in BaseWidget.frameworks:
			if 'visPv' in self.widget.props:
				return 'caQtDM'
			return 'EpicsQt'
		elif 'EpicsQt' in BaseWidget.frameworks:
			return 'EpicsQt'
		return 'caQtDM'

	def widgetUI(self, parent):
		''' Workhorse of this class; should be overridden.
			Writes all properties
			for this widget to the ui file.  Default implementation writes
			the widget tag and the geometry.  Most classes will want to
			implement to call BaseWidget.startWidget, then set any custom
			properties, and finally to call BaseWidget.endWidget.

		Args:
			parent (lxml.etree.elem): The parent XML element

		Returns:
			lxml.etree.elem: The created XML sub-element
		'''
		elem = self.startWidget(parent)
		self.endWidget(elem)
		return elem

	def isBuiltInWidget(self):
		''' True if this is a standard, Qt-provided widget.
			Most widgets defined here will override this to
			return False; the exception is when they output
			a standard, non-EPICS-aware widget like QLabel.

		Returns:
			boolean: True if a Qt standard widget; False otherwise
		'''
		return True

	def isContainer(self):
		''' True if this is a container widget, e.g. QFrame
			Most widgets can ignore this function.
		'''
		return False

	def widgetType(self):
		''' The widget type to appear in the ui file, e.g. QELabel.
			Must be overridden.

		Returns:
			string: The widget type
		'''
		pass

	def widgetName(self):
		''' The name of this widget instance, e.g. "qelabel_1".
			Must be overridden.
			Must be unique in the UI file, so the convention is to
			increment the trailing number for each widget, using the
			static count property.

		Returns:
			string: The widget name
		'''
		pass

	def widgetBaseClass(self):
		''' The base class name of the widget, from Qt Designer's
			perspective, e.g. "QLabel".
			Must be overridden.

		Returns:
			string: The name of the widget's base class
		'''
		pass

	def widgetHeader(self):
		''' The C/C++ header file describing the widget, so that
			Qt Designer can determine the allowable properties,
			e.g. "QELabel.h"
			May be overridden; default is widgetType().h, which
			is usually correct.

		Returns:
			string: The name of the C header file
		'''
		return self.widgetType()+'.h'
