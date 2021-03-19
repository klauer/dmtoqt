dmtoqt: EDM to Qt Parser
########################

This documentation resides at https://controls.als.lbl.gov/alscg/dmtoqt/latest.

Overview
===========
dmtoqt takes EDM files (*.edl) as input, and writes Qt Designer UI files (*.ui).  It takes advantage
of EPICS-aware Qt widget frameworks to mimic the intent and appearance of the original EDM user interfaces
as closely as possible.

Synpopsis
==========

Invoke dmtoqt like::

	python dmtoqt.py --help
	usage: dmtoqt.py [-h] [-v | -q] [-p PATH] [-c COLORS]
					   [-f FRAMEWORK [FRAMEWORK ...]]
					   file [file ...]
	Convert EDM files to epicsqt-aware Qt ui files (for more details, please visit
	https://controls.als.lbl.gov/alscg/dmtoqt)
	positional arguments:
		file File(s) to convert. Glob-style wildcards may be used.
			 If no extension is provided, .edl will be added.
			 Output goes to {file}.ui
	optional arguments:
		-h, --helpshow this help message and exit
		-v, --verbose Turn on verbose output
		-q, --quiet Be vewwy quiet
		-p PATH, --path PATHPath in which to look for input files and write output
			files
		-c COLORS, --colors COLORS
			Path to colors.list file. If not provided, will look
			in $EDMOBJECTS, $EDMPVOBJECTS, /etc/edm/edmobjects
		-f FRAMEWORK [FRAMEWORK ...], --framework FRAMEWORK [FRAMEWORK ...]
			Use framework "EpicsQt" and/or "caQtDM". If only one
			argument is provided, only that framework will be
			used; if both are specified the best match for each
			widget will be chosen. Default is to use EpicsQt only

Running dmtoqt
==============

Normally, the only arguments required are the filename(s) of EDM files to be converted.
These may be glob-style wildcards, in which case all matching files will be read.

Examples:

One or more input files::

	python dmtoqt.py linac.edl booster.edl

Reads linac.edl and booster.edl from the current working directory, and produces
linac.ui and booster.ui in the same directory.  EpicsQt widgets will be produced.

Specifying a path::

	python dmtoqt.py -p /usr/local/epics opi/*.edl

Reads all .edl files in /usr/local/epics/opi, and writes .ui files in the same
directory.  The filenames will match the input filenames; that is, if a file
/usr/local/epics/opi/linac.edl exists, /usr/local/epics/opi/linac.ui will be written.

Forcing use of caQtDM Widgets::

	python dmtoqt.py -f caQtDM linac.edl

Reads linac.edl from the current directory, and writes linac.ui.  Only caQtDM
widgets will be used.  (CAUTION: caQtDM is not fully supported as of this writing)


Using multiple frameworks::

	python dmtoqt.py -f caQtDM EpicsQt linac.edl

Reads linac.edl from the current directory, and writes linac.ui.  Widgets will
be EpicsQt or caQtDM, depending on which framework is most suitable for the input EDM widget.
(CAUTION: Since caQtDM is not fully supported, this may not always provide optimal results.)
