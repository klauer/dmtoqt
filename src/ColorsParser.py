'''
.. module:: ColorsParser
	:synopsis: Defines the RGB and ColorsParser classes

'''
###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
import logging
import os
import sys
import re

class RGB:
	''' Container for a color defined as red/green/blue components '''

	def __init__(self, r, g, b, a=None):
		''' Constructor

		Args:
			r (integer): red value between 0 and 65535
			g (integer): green value between 0 and 65535
			b (integer): blue value between 0 and 65535
			a (integer): alpha value between 0 and 65535.  If None, color is fully opaque.
		'''
		self.r = self.mapColorComponent(str(r))
		self.g = self.mapColorComponent(str(g))
		self.b = self.mapColorComponent(str(b))
		if a is None:
			self.a = None
		else:
			self.a = self.mapColorComponent(str(a))

	def mapColorComponent(self, val):
		''' (Internal function) Map a color value from 16 to 8 bits
			EDM uses 16-bit integers for RGB values, while Qt (and everyone else)
			uses 8 bits
		'''
		i = int(val)/255
		if i > 255: i = 255
		if i < 0: i = 0
		return i

	def __str__(self):
		''' Convert the red/green/blue color components into
			a "#rrggbb" string suitable for use in a stylesheet.

		Returns:
			string: like "#rrggbb"
		'''
		r = hex(self.r)[2:]
		g = hex(self.g)[2:]
		b = hex(self.b)[2:]
		if len(r) < 2: r = '0'+r
		if len(g) < 2: g = '0'+g
		if len(b) < 2: b = '0'+b
		return "#%s%s%s" % (r, g, b)

class ColorsParser(object):
	''' Reads the EDM colors.list file so that proper
		colors can be written to the Qt ui file.
	'''

	def __init__(self):
		''' Constructor. '''
		self.logger = logging.getLogger(self.__class__.__name__)
		self.unkcolor = RGB('255', '255', '255')

	def getRGB(self, edmvalue):
		''' Attempt to find an RGB instance matching the EDM string

			Normally this is called with an EDM color string of the form "index xx",
			where xx is an integer index into the colors table.  If a matching
			color is found, the RGB instance is returned.

		Args:
			edmvalue (string or dict): If a string, should be in the "index xx" form; if a dict, shold have 'r', 'g', 'b', and 'a' keys.

		Returns:
			RGB: RGB instance on success.  If not, falls back to returning the original string.
		'''
		if isinstance(edmvalue, dict):
			return RGB(edmvalue['r'], edmvalue['g'], edmvalue['b'], edmvalue['a'])
		re_index = re.compile('^index (\d+)$')
		m = re_index.match(edmvalue.strip())
		if m:
			idx = int(m.group(1))
			if not idx in list(self.colors.keys()):
				self.logger.warn("Index %d not found in colors list; returning white" % idx)
				return self.unkcolor
			return self.colors[idx]['rgb']
		''' TODO: If color is not an index, what is the proper return? '''
		return edmvalue

	def readColorsFile(self):
		''' Read the colors list file.

			Checks the EDMOBJECTS and EDMPVOBJECTS environment variables; if
			one is set and points to a path containing a colors.list file,
			calls ColorsParser.read and returns True.  If not, or the read
			method fails, tries reading /etc/edm/edmObjects/colors.list.

		Returns:
			boolean: True on success, False otherwise
		'''
		paths = [
			os.getenv('EDMOBJECTS'),
			os.getenv('EDMPVOBJECTS'),
			'/etc/edm/edmObjects' # default
		]
		colorsFilename = None
		for path in paths:
			if path is None:
				continue
			colorsFilename = os.path.join(path, 'colors.list')
			if os.path.isfile(colorsFilename):
				if self.read(colorsFilename):
					return True
			colorsFilename = None
		if colorsFilename is None:
			self.logger.warn('Cannot find a colors.list file')
			return False
		self.logger.info('Colors file: %s' % colorsFilename)
		return True

	def read(self, fname):
		''' Read a colors list file.

			Attempts to read the given file and parse it for color values.

		Args:
			fname (string): The full path name

		Returns:
			boolean: True if successful and at least one color was found
	'''
		self.properties = {}
		self.colors = {}
		self.aliases = {}
		self.menumap = []
		self.inMenumap = False
		with open(fname) as f:
			for line in f:
				self.readline(line.strip())
		return len(self.colors) > 0

	def readline(self, line):
		''' Read a line from a colors list file

			Called from ColorsParser.read().
			Attempts to create a color mapping.

		Args:
			line (string): The line in the file
		Returns:
			boolean: True on success, False otherwise
		'''
		re_version = re.compile(r'^(\d+) (\d+) (\d+)$')
		re_property = re.compile(r'^([^=]+)=([^ ]+)')
		re_alias = re.compile(r'^alias ([^ ]+) (.+)$')
		''' color format: "static" index title { r g b } #[comment] '''
		re_color = re.compile(r'^static (\d+)\s+"([^"]+)"\s+{\s+(\d+)\s+(\d+)\s+(\d+) }\s+#.*$')

		if line == '':
			return True

		m = re_version.match(line)
		if m is not None:
			self.version = {
					'major': m.group(1),
					'minor': m.group(2),
					'release': m.group(3)
			}
			return True

		m = re_property.match(line)
		if m is not None:
			self.properties[m.group(1)] = m.group(2)
			return True

		m = re_alias.match(line)
		if m is not None:
			self.aliases[m.group(1)] = m.group(2)
			return True

		m = re_color.match(line)
		if m is not None:
			self.colors[int(m.group(1))] = {
					'name': m.group(2),
					'rgb': RGB(m.group(3), m.group(4), m.group(5))
			}
			return True

		if line == 'menumap {':
			self.inMenumap = True
			return True
		if self.inMenumap:
			if line == '}':
				self.inMenumap = False
				return True
			self.menumap.append(line)
			return True

		#self.logger.warn('no match for line: %s' % line)
		return False

if __name__ == '__main__':
	logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)

	parser = ColorsParser();
	if not parser.readColorsFile():
		print('Cannot read colors')
	for idx in parser.colors:
		print(str(idx)+': '+str(parser.colors[idx]))


