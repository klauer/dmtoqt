findEDMProps
############

Overview
========

findEDMProps is a simple tool to find widget classes in an EDM source tree
and enumerate their possible properties.  It is a developer's tool only.

Usage
=====

Invoke findEDMProps like::

	python findEDMProps.py [-h] [-v | -q] -p PATH [-c CLAZZ] [-o OUTPUT]

	Parse EDM source files for widget properties

	optional arguments:
	-h, --help            show this help message and exit
	-v, --verbose         Increase output
	-q, --quiet           Be vewwy quiet
	-p PATH, --path PATH  Path to EDM source
	-c CLAZZ, --clazz CLAZZ
					   Name of class to parse (default=all)
	-o OUTPUT, --output OUTPUT
					   Output path (default=./widgets/edmprops)

	The only required argument is -p/--path, which is the directory in
	which the EDM source code can be found.

Operation
=========

findEDMProps works by searching for calls to the loadR function in edm
source files.  This function loads property values into a widget configuration,
given the property name and a default value if it is not found in the input
(.edl) file.  Since all widgets use this function to load their properties,
it is a convenient shorthand for determining all possible property names.

Some attempts are made to map the properties to known types and to Qt properties;
however this is not fully implemented and in practice has not proven very useful.
See emdVarTypes.py for currently configured property mappings.

Once the properties are read for a widget, the widget mapping code is written to
a python file named after the EDM widget class name.  The file is written to the
output path provided to findEDMProps, or to ./widgets/edmprops.  The file
widgets/widget_template.py is used as a starting point, and all occurrences of
"widget_template" are replaced with the new class name.  In addition, there is a
line in widget_template.py, in the widgetUI method, that reads "widget properties".
This line is removed, and a series of calls to self.property are inserted in its
place.  These calls are of the form::

	self.property(elem, "propname", "propname", "type")

Here the first argument, elem is the parent XML element and should not be changed.
The first "propname" is the Qt property name; the second is the EDM property name;
"type" is the type.  The property names and type are filled in if found in edmVarTypes.py;
if not found, the EDM property name is used for both and the type is "unknownType".

It is the task of the developer to fill in the appropriate property mappings in the
widgetUI method, including any logic required.  Several helper functions are provided
in widgets/BaseWidget.py to make this easier, and it is recommended that developers
examine other widget types found in the widgets directory for instructive examples.

In addition to the widgetUI method, a few more methods must be provided:

* `def widgetName(self)`: returns a string for the widget name, which must be unique
	in the .ui file.  Placeholder code is provided that uses the `count` member variable
	to generate a unique name; it is recommended that the generated name be simplified.
	As an example, the default code for activeXTextClass would be::

		return 'activeXTextClass_%d' % self.count

	the class provided in this package shortens this to::

		return 'label_%d' % self.count

* `def widgetType(self)`: returns a string representing the name of the Qt type of the
	widget to be created.  There is often a one-to-one mapping of EDM widget type to Qt
	widget type; however for some types the mapping will vary, depending on the chosen
	framework and/or the EDM properties. See other widget mappings for examples.

* `def isBuiltInWidget(self)`: returns True if one of the standard Qt widgets is to be
	generated (e.g. QLabel, QWidget, etc.).  If widgetType() returns a widget from one
	of the frameworks, or another plugin, this method must return False.  Most widget
	mappings will leverage custom widgets and so will need to return False.

* `def isContainer(self)`: returns True if the generated widget can contain other widgets;
	for example, QFrame, QWidget, and QEPvFrame can all act as containers, while QLabel
	and QELabel cannot.

* `def widgetBaseClass(self)`: returns a string which is the name of the base class of
	the widget type returned from widgetType().

Deployment/testing
==================

Once the above methods have been filled in, the new widget mapping class can be placed in
the widgets directory, and dmtoqt will read it when parsing an EDM file that contains
that type of widget.  The developer then typically needs to open the resulting .ui file
in Qt Designer (and qegui or caQtDM), tweak the property mappings, re-run dmtoqt and re-open
the .ui file, until the best possible mapping is achieved.
