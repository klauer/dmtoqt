#!/usr/bin/env python
from __future__ import print_function
'''
.. module:: findEDMProps
	:synopsis: Defines findEDMProps, a helper to list EDM Properties from EDM widgets

	Searches the EDM source directory tree for widget classes, finds and lists
	their possible properties.
	For more details please see @ref findEDMProps.

'''
###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################

import os
import sys
import logging
import argparse
import subprocess
import re
from src.edmVarTypes import Variable, knownVariableTypes

class Property(dict):
	''' Simple name-value pair '''
	def __init__(self, name):
		self.name = name
		self.variable = None

class PropertySet:
	''' Collection of properties

		See also:
			:class:`edmVarTypes.Variable`
	'''
	def __init__(self, classname):
		self.classname = classname
		self.properties = {}
		self.variables = {}

	def addProperty(self, propname, typeval):
		self.properties[propname] = Property(propname)
		found = False
		if propname in list(self.variables.keys()):
			self.properties[propname].variable = self.variables[propname]
			found = True
		elif propname in list(knownVariableTypes.keys()):
			self.properties[propname].variable = knownVariableTypes[propname]
			found = True
		if not found:
			logging.warn('Variable %s not found on class %s' % (propname, self.classname))

widgetProperties = {}
re_method = re.compile(r'^int ([^:]+)::createFromFile')
re_loadR = re.compile(r' *tag\.loadR\( *"([^"]+)",? ?([^)]*)\);')

def processSrc(root, fname, classnames):
	''' Reads a C source file in the EDM source tree, searching for
		calls to "tag.loadR".  When these are found, a property name
		and initial value is determined.
	'''
	logging.debug('processSrc: %s', os.path.join(root, fname))
	'''
	if fname != 'act_win.cc':
		try:
			output = subprocess.check_output(['grep', '^int \w\+::createFromFile', os.path.join(root, fname)])
		except Exception as e:
			return False
	'''

	classname =  properties = None
	lineno = 0
	with open(os.path.join(root, fname)) as f:
		foundMethod = False
		for line in f:
			lineno += 1
			line = line.strip()
			if not foundMethod:
				# Special case for top-level window
				if line == 'int activeWindowClass::loadWinGeneric (':
					classname = 'activeWindowClass'
				else:
					m = re_method.match(line)
					if m is None:
						continue
					classname = m.group(1)
				if classnames is not None and len(classnames) > 0:
					if not classname in classnames:
						continue
				foundMethod = True
				properties = PropertySet(classname)
				continue
			m = re_loadR.match(line)
			if m is None:
				continue
			if m.group(1) == 'beginObjectProperties':
				logging.info('Line %d: Found begin Object properties for class %s', lineno, classname)
				continue
			if m.group(1) == 'endObjectProperties':
				logging.info('Line %d: Found end object properties for class %s', lineno, classname)
				break
			if m.group(1) == 'beginScreenProperties':
				logging.info('Line %d: Found begin Screen properties for class %s', lineno, classname)
				continue
			if m.group(1) == 'endScreenProperties':
				logging.info('Line %d: Found end Screen properties for class %s', lineno, classname)
				break
			logging.info('Line %d: class %s: property %s => %s', lineno, classname, m.group(1), m.group(2))
			properties.addProperty(m.group(1), m.group(2))
	if classname is not None and properties is not None:
		widgetProperties[classname] = properties


if __name__=="__main__":
	parser = argparse.ArgumentParser(description='Parse EDM source files for widget properties')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-v', '--verbose', help='Increase output', action='store_true')
	group.add_argument('-q', '--quiet', help='Be vewwy quiet', action='store_true')
	parser.add_argument('-p', '--path', help='Path to EDM source', required=True)
	parser.add_argument('-c', '--clazz', help='Name of class to parse (default=all)')
	parser.add_argument('-o', '--output', help='Output path (default=./widgets/edmprops)', default='widgets/edmprops')

	args = parser.parse_args()

	level = logging.INFO
	if args.quiet:
		level = logging.WARN
	elif args.verbose:
		level = logging.DEBUG
	logging.basicConfig(level=level)

	if not os.path.isdir(args.path):
		print(('EDM path (%s) does not appear to be valid' % args.path))
		sys.exit(-2)

	if not os.path.isdir(args.output):
		print(('Ouput path %s does not appear to be a directory; attempting to create' % args.output))
		try:
			os.mkdir(args.output)
		except:
			print(('Exception creating output directory %s' % args.output))
			sys.exit(-2)

	for root, dirs, files in os.walk(args.path):
		for fname in files:
			if fname.endswith('.cc'):
				processSrc(root, fname, args.clazz)

	print(('Found %d widget type(s)' % len(widgetProperties)))
	with open(os.path.join('widgets', 'widget_template.py'), 'r') as f:
		template = f.read()

	for classname, propset in list(widgetProperties.items()):
		print(('%s:' % classname))
		classtemplate = template.replace('widget_template', classname)
		for propname, prop in list(propset.properties.items()):
			print(('\t%s:' % (propname)), end=' ')
			if prop.variable is not None and prop.variable.type is not None:
				print((' type: %s' % (prop.variable.type)))
			else:
				print(' ** no type **')
		propstr = ''
		for propname, prop in list(propset.properties.items()):
			# Exclude version and geometry
			if propname in ('major', 'minor', 'release', 'x', 'y', 'w', 'h'):
				continue
			if prop.variable is None:
				propstr += "\t\t#self.property(elem, '%s', '%s', 'unknowntype')\n" % (propname, propname)
			else:
				propstr += "\t\tself.property(elem, '%s', '%s', '%s')\n" % (propname, propname, prop.variable.type)
		fulltemplate = classtemplate.replace('widget_properties', propstr)

		with open(os.path.join(args.output, classname+'.edmprops.py'), 'w') as f:
			f.write(fulltemplate)

