Developers' Info
################

How dmtoqt works
================

dmtoqt has been designed to be easy to use without delving into internal details;
however it is also an open-source project and modifying or enhancing it should be
straightforward as well.  This page provides some information about the internals
of dmtoqt to help developers get started.

Code Layout
===========

dmtoqt is a python project with the following layout:

* Root Directory

	* dmtoqt.py: main entry point for the application; command-line parsing
	* DMReader.py: The DMReader class, which reads a .edl file and creates
		the EDMWidget objects
	* EDMWidget.py: The EDMWidget class.  One instance of EDMWidget is created for
		each widget found by DMReader and populated with the EDM properties.
	* StackedEDMWidget.py: The StackedEDMWidget class.  This consists of two or more
		EDMWidget instances, stacked on top of each other.
	* ColorsParser.py: The ColorsParser class, which holds the colors.list file and
		provides a mapping to html-style color names
	* UIWriter.py: Writes the .ui file, creating a widget class from the widgets directory
		for each EDMWidget
	* findEDMProps.py: A tool to find EDM properties and map them to equivalent Qt
		properties.  This provides only an approximation and is intended for developers
		wishing to create new widget mappings
	* edmVarTypes.py: Used by findEDMProps.py.

* widgets Directory

	* BaseWidget.py: The base class for all widget types; provides helper functions to
		generate XML for widget properties of various types
	* StackWidget.py: Produces xml for a single widget, that collapses two or more EDM
		widgets on top of each other
	* widget_template.py: Provides a template for new widget types used by findEDMProps.py.
	* additional widget classes: Each additional file is named for an EDM widget type
		and provides the mapping to Qt widget properties.


Design
======

dmtoqt is designed to ease the task of converting EDM screens to the Qt environment.
The task is divided into subtasks:

1. Parse command-line arguments
2. Read EDM file(s)
3. Assemble EDM widget configurations into distinct python objects
4. Manipulate the hierarchy of widget objects to collapse redundant and stacked widgets
5. Create mapping widget objects in python that can translate EDM properties into Qt-compatible XML syntax
6. Assemble all XML and write output file(s)

The mapping step is performed by a series of python classes in the widgets directory.  This
allows the creation of new widget mappings with minimal difficulty, and allows the new
types to be discovered automatically.  These widget mapping classes perform the bulk of
dmtoqt's work.

Most enhancements to dmtoqt will take the form of new or modified widget mapping classes.  To understand
how these work, please see the following:

* widget_template.py : A template that can be used as a starting point for new mapping classes.
	widget_template.py is also used by the @ref findEDMProps tool.
	Details about the methods that must be reimplemented are in widgets.widget_template.widget_template.
* widgets.BaseWidget.BaseWidget : The base class for all widget mapping classes; provides several helper functions
	and default implementations.
* EDMWidget.EDMWidget : A simple class that holds the EDM property values.
* ColorsParser.ColorsParser : Maps EDM colors to Qt colors.  In EDM, the colors are specified as indexes
	into a color table; these indexes are mapped to colors by the colors.list file.  In Qt, colors are specified
	explicitly in "#rrggbb" format using the (r)ed, (g)reen, and (b)lue components.
* ColorsParser.RGB : A simple class to hold the r, g, b, and alpha components of a color.  Provides a __str__ function
	to convert the color values to a Qt-compatible #rrggbb string.  A series of RGB
	instances are created by ColorsParser.


