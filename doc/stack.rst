Stack Widgets
#############

In EDM, widgets are often stacked on top of each other and assigned a visibility pv, along
with a range of values, so that only one of the widgets is visible at any time.  When the pv
value changes, one or more widgets in the stack may be shown or hidden.

The EpicsQt widget set largely removes this design pattern in favor of displaying different
colors according to alarm levels, or of displaying the text matching a pv's enumerated state.
This means some of the logic is pushed to the EPICS database level, since alarm levels and
appropriate enumeration strings need to be configured.  This may seem like a problem, since it
means EPICS databases may need to be adjusted, but ultimately it vastly simplifies the user
interface layer and puts the information where it can be accessed by any client (or, indeed,
CA servers such as IOCs), not just graphical user interfaces.

When these cases are encountered, dmtoqt must make some decisions about how best to convert
the EDM widgets to Qt.  It tries to convert as much as possible to minimize the work
required of the user, but some cases cannot be converted completely.  When this happens,
dmtoqt attempts to warn the user and provide the information required to fix the problem.

What is a stack?
================

Determining whether a set of widgets constitute a stack is not always straightforward.  They
must overlap; however they may not always be exactly the same size or in the same position.
So dmtoqt does its best, with a fudge factor and some assumptions.

Another requirement to make a stack is, in most cases, that all widgets be the same type.
So dmtoqt recognizes two types of stacks: shapes, and labels.  Shapes are graphic objects
such as rectangles or circles that often (but not always) use the same visibility pv to
display the correct color.

Stacks of labels usually display different text, depending on the value of a pv.  While these
must overlap, dmtoqt does not assume they will be the same width, since the labels may consist
of different numbers of letters.

Mapping Stacks of Shapes
========================

A limited set of properties can lead to stacks of shapes that are simple to map: all refer to
the same pv and the values correspond to alarm levels.  But there is no requirement for users
to adhere to this: many stacks may refer to multiple pvs, for example.  So dmtoqt attempts
to provide the information required to reproduce the behavior in EDM, without trying to
understand what that behavior is.  It does this by creating a series of properties that will
not be recognized by Qt but will cause no errors.

These properties are each lists of strings, all with the same number of elements, which matches
the number of stacked widgets in the EDM screen.  They are:

1. visPvs: the pvs listed as visibility pvs in EDM.
2. visMins: the minimum values listed in EDM.
3. visMaxs: the maximum values listed in EDM.
4. visInverts: Each is "True" if EDM was configured as "Not visible if", or "False" otherwise.

After converting a screen and opening the resulting .ui file in Qt Designer, selecting a stack widget
and scrolling down in the Property Editor may reveal a "Dynamic Properties" section.  If this section
does not appear, then dmtoqt judged that it found all the required information and successfully mapped
it to Qt properties.  If the Dynamic Properties section does appear, it will contain the above properties.

(Dynamic Properties is where Designer puts properties it does not understand for a widget.  They have no
effect on the widget's behavior)

So, to recover the behavior from EDM, examine these Dynamic Properties to determine what EDM was trying
to convey.  If you are lucky, you will not need to do anything to your EPICS databases to reproduce
the behavior.  More often, though, you will need to either set alarm levels on existing pvs, or
create new pvs that combine the existing pvs in an appropriate way.

Mapping Stacks of Labels
========================

Stacks of labels are, in many cases, easier than shapes to map.  dmtoqt creates a QELabel, which would
normally display the enumerated value of a single pv.  However dmtoqt knows nothing about the pv's
enumeration so it fills in the Local Enumeration property in Qt with the text values of all the
labels in the stack.

It is recommended to examine this Local Enumeration property to determine if the enumeration could be
replaced with the pv's enumeration values.  If so, the following steps may be taken to display the
pv's enumerated values instead:

1. Set the *Local Enumeration* property back to its default, empty value
2. Set the *format* property back to its default value, *Default*.

Once this is done, any future changes to the pv's enumerated values will be reflected in the user interface,
making the UI much easier to maintain.

If it is not possible to follow the steps above, it is recommended to move the enumerated values from
the UI to the underlying pv, either by editing the pv's values or, if that's not feasible, creating
a new pv with the appropriate values.
