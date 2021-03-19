#!/usr/bin/env python
'''
.. module:: dmtoqt
	:synopsis: Entry point for the EDM to Qt converter.

'''

###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################

if __name__=='__main__':
	import argparse
	import sys
	import os
	import glob
	import logging
	from src.DMReader import DMReader
	from src.UIWriter import UIWriter
	from src.ColorsParser import ColorsParser
	from lxml import etree as ElementTree
	from src.widgets.BaseWidget import BaseWidget
	from version import version as v

	docurl = 'https://controls.als.lbl.gov/alscg/dmtoqt'
	if 'DMTOQT_DOCURL' in os.environ:
		docurl = os.environ['DMTOQT_DOCURL']

	argparser = argparse.ArgumentParser(description='dmtoqt (version %s): Convert EDM files to epicsqt-aware Qt ui files (for more details, please visit %s)' % (v, docurl))
	group = argparser.add_mutually_exclusive_group()
	group.add_argument('-v', '--verbose', help='Turn on verbose output', action='store_true')
	group.add_argument('-q', '--quiet', help='Be vewwy quiet', action='store_true')
	argparser.add_argument('-p', '--path', help='Path in which to look for input files and write output files', default=os.getcwd())
	argparser.add_argument('-c', '--colors', help='Path to colors.list file.  If not provided, will look in $EDMOBJECTS, $EDMPVOBJECTS, /etc/edm/edmobjects')
	argparser.add_argument('-f', '--framework', help='Use framework "EpicsQt" and/or "caQtDM".  If only one argument is provided, only that framework will be used; if both are specified the best match for each widget will be chosen. Default is to use EpicsQt only', nargs='+', default=['EpicsQt'])
	argparser.add_argument('file', help='File(s) to convert.  Glob-style wildcards may be used.  If no extension is provided, .edl will be added.  Output goes to {file}.ui', nargs='+')

	args = argparser.parse_args()

	level = logging.INFO
	if args.verbose:
		level = logging.DEBUG
	elif args.quiet:
		level = logging.WARNING
	logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=level, stream=sys.stdout)

	logger = logging.getLogger('dmtoqt')
	logger.info('dmtoqt version %s' % v)
	logger.info('Parsing %d file(s)' % len(args.file))

	colorsParser = ColorsParser()
	if args.colors:
		colorsParser.setPath(args.colors)
	if not colorsParser.readColorsFile():
		logger.warn('Unable to read colors file; colors may not appear correct')

	if args.framework is not None:
		BaseWidget.frameworks = args.framework

	success = 0
	failures = {}
	for fnpattern in args.file:
		logger.info('Input filename pattern: "%s"..' % fnpattern)
		for fname in glob.iglob(os.path.join(args.path, fnpattern)):
			logger.info('Input filename: "%s"..' % fname)
			idx = fname.rfind('.')
			if idx < 0:
				fname = fname+'.edl'
				logger.info('Added extension - filename = %s' % fname)
			elif idx < len(fname)-4 or idx >= len(fname)-1:
				logger.warn('Period found in filename %s but does not seem to indicate an extension (length = %d); adding one' % (f, len(fname) - idx))
				fname = fname+'.edl'
			reader = DMReader(fname)
			try:
				f = open(fname, 'r')
				if not reader.read(f):
					logger.critical('Failed to read file '+fname)
					failures[fname] = 'Failed to read file'
					continue
			except:
				logger.warn('Exception parsing file %s' % fname)
				failures[fname] = 'Exception parsing file'
				continue
			logger.debug('Parsed file %s; writing to ui' % fname)

			idx = fname.rfind('.')
			ofname = fname[0:idx]+'.ui'
			logger.info('Writing to %s' % ofname)
			writer = UIWriter(ofname)
			writer.setColors(colorsParser)
			if not writer.write(reader):
				logger.critical('Failed to write xml tree')
				failures[fname] = 'Failed to write xml tree'
				continue

			logger.info('Converted %s to %s' % (fname, ofname))
			success = success + 1

	logger.info('Finished; %d success, %d failed, %d total' % (success, len(args.file)-success, len(args.file)))
	if len(failures) > 0:
		logger.info('Failed files:')
		for fname, reason in list(failures.items()):
			logger.info('\t%s\t%s' % (fname, reason))


