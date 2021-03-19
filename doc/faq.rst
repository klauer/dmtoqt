.. _faq:

################################
Frequently Asked Questions (FAQ)
################################

.. _stack:

* **My EDM screen has some shapes (or labels) stacked on top of each other, so only one is visible depending on the state of a pv (or several).  That's broken in the Qt screen - what happened???**

	The EDM way of showing/hiding widgets based on the values of pvs is not well reproduced
	in Qt.  That's not really a limitation of Qt, but a design choice: it makes the display harder
	to maintain and embeds a certain amount of logic in the GUI.

	dmtoqt will attempt to map these cases to a single widget.  In most cases the alarm level
	of a pv will affect the color of the shape, or the enumeration value will affect the displayed
	value.  This is a better way to create screens, but may require some manual intervention on your
	part.

	dmtoqt maps overlapping widgets, as best it can, to "Stack" widgets.

.. _vispv:

* **My EDM screen hides/shows widgets based on the value of a pv, but the Qt screen doesn't.  What's going on?**

	EDM allows this, but the EpicsQt developers have made a philosophical decision
	to disallow it, because it means logic is embedded in the GUI.  While some
	attempts have been made to mimic EDM behavior, in the majority of cases it is
	better to put the logic in the IOC.  Please see [Stack Widgets](widgets.html#stack).

.. _findedmprops:

* **dmtoqt failed with an error like `widgets/widgetname.py not found`. What can I do?**

	This means you're using an EDM widget that has not been mapped in the dmtoqt distribution.
	You can add it if you wish; the process is not hard but requires some development skill.
	Please see widgets/widget_template.py for a starting point for a new widget, and @ref findedmprops
	for help generating a widget mapping class with possible EDM properties.  And, please,
	contribute your additions back to the project!

	If you're not that brave, your choices are (1) contact the dmtoqt developers for help,
	or (2) adjust your .edl file to use another type of widget.

.. _whatisedm:

* **What is EDM?  MEDM?**

	If you're asking that question, it's fairly certain you don't need this tool.
	However, [EDM](https://ics-web.sns.ornl.gov/edm/eum.html) is the Extensible Display Manager,
	a GUI tool for [EPICS](http://www.aps.anl.gov/epics/index.php).  It has been extremely successful
	as it provides an easy-to-use editing tool for EPICS-aware user interface screens, which is
	very fast and fault-tolerant.

	However, EDM is showing its age.  It depends on outdated and not-fully-supported technologies,
	and has a quirky feel for those who haven't used it before.

	[MEDM](http://www.aps.anl.gov/epics/extensions/medm/index.php) stands for Motif Editor and Display
	Manager.  It is similar to EDM and based entirely on the Motif window manager.  It has some of the
	same advantages as EDM, and (arguably to a greater degree) the same disadvantages.

	The EPICS community has made numerous efforts to modernize these tools.  Qt (see below) and
	[CSS](http://controlsystemstudio.org/) are, in some peoples' opinion, two of the more successful
	of these.

.. _whatisqt:

* **What is Qt?**

	[Qt](https://www.qt.io/) is a framework and toolset for creating cross-platform applications,
	including creating graphical user interfaces.  It is written in and can be extended with C++;
	there are also python bindings (see [PyQt](https://riverbankcomputing.com/software/pyqt/intro)).
	The extensibility of Qt has made writing add-on widgets relatively simple, and a couple of
	projects have produced useful sets of EPICS-aware widgets (see @ref whatisepicsqt and @ref whatiscaqtdm).

.. _whatisepicsqt:

* **What is EpicsQt?**

	[EpicsQt](https://github.com/qtepics) is a set of widgets and an interface layer to EPICS that
	makes it possible to create and edit GUI screens without writing any code.  It is a rich widget
	set and highly performant.  EpicsQt was originated by folks at the Australian Light Source and
	has been adopted at several sites around the world.

.. _whatiscaqtdm:

* **What is caQtDM?**

	[caQtDM](http://epics.web.psi.ch/software/caqtdm/) is another set of widgets and another interface
	layer to EPICS. Like EpicsQt, it makes it possible to create and edit GUI screens without writing
	any code, it is a rich widget set, and it is highly performant.  Unlike EpicsQt, it was designed
	from the start to provide a MEDM/EDM replacement, so the widgets were created to provide similar
	functionality to their MEDM/EDM counterparts.  This makes writing a conversion tool simpler, and
	such a tool is provided with caQtDM called edl2ui (or, for MEDM, adl2ui).  Because of the availability
	of those tools, and the dmtoqt author's preference for EpicsQt, the caQtDM conversion in dmtoqt
	has been deemphasised.

.. _whichisbetter:

* **Which is better: caQtDM or EpicsQt?**

	This is largely a question of personal preference.  caQtDM better mimics MEDM/EDM, so if you're used to
	the widget capabilities in those tools you may like it better.  EpicsQt is designed to leverage the
	strengths of Qt and EPICS, without trying to reproduce the advantages and disadvantages of MEDM/EDM.
	It is this author's opinion that the architecture of EpicsQt is better laid out and so will prove
	eaiser to maintain and extend in the future, so should last longer.  YMMV.

.. _docurl:

* **Typing "python dmtoqt.py -h" gives the location of the documentation.  Can I change that url?**

	Yes: Please see @ref DMTOQT_DOCURL.
