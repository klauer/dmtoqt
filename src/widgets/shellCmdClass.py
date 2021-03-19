###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import logging
from lxml import etree
from xml.sax.saxutils import escape

class shellCmdClass(BaseWidget):
	count = 0
	@staticmethod
	def incrcount():
		shellCmdClass.count += 1
		return shellCmdClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(shellCmdClass, self).__init__(widget)
		self.count = shellCmdClass.incrcount()

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		''' Add your widget-specific properties here '''
		if self.framework() == 'EpicsQt':
			self.property(elem, 'labelText', 'buttonLabel', 'string')
			self.property(elem, 'toolTip', 'buttonLabel', 'string')
			self.property(elem, 'statusTip', 'buttonLabel', 'string')
			if self.isMenuButton():
				entries = self.menuEntries(elem)
			elif 'numCmds' in self.widget.props:
				if 'commandLabel' in self.widget.props and len(self.widget.props['commandLabel']) > 0:
					self.stringProperty(elem, 'text', self.widget.props['commandLabel']['0'])
				cmd, args = self.parseCommand('0')
				self.stringProperty(elem, 'program', cmd)
				if len(args) > 0:
					self.stringProperty(elem, 'arguments', args)
				self.stringProperty(elem, 'programStartupOption', 'StdOutput')
			# closeDisplay: if true, set creationOption to NewWindow
			if 'closeDisplay' in self.widget.props and bool(self.widget.props['closeDisplay']):
				self.enumProperty('creationOption', 'NewWindow')
			# Reverse logic for invisible:
			if 'invisible' in self.widget.props:
				self.booleanProperty('visible', False)
		else: # caQtDM: use caShellCommand
			if 'buttonLabel' in self.widget.props:
				self.stringProperty(elem, 'label', self.widget.props['buttonLabel'])
			if 'commandLabel' in self.widget.props:
				labels = ';'.join(list(self.widget.props['commandLabel'].values()))
				self.stringProperty(elem, 'labels', labels)
			cmds = []
			args = []
			for cmd in list(self.widget.props['command'].values()):
				cmdargs = cmd.split()
				cmds.append(cmdargs[0])
				args.append(' '.join(cmdargs[1:]))
			self.stringProperty(elem, 'files', ';'.join(cmds))
			self.stringProperty(elem, 'args', ';'.join(args))
		# No equivalent
		#self.property(elem, 'autoExecPeriod', 'autoExecPeriod', '')
		#self.property(elem, 'lock', 'lock', '')
		# No equivalent
		#self.property(elem, 'execCursor', 'execCursor', '')
		#self.property(elem, 'labelText', 'commandLabel', 'string')
		#self.property(elem, 'bgColor', 'bgColor', 'color')
		self.property(elem, 'font', 'font', 'font')
		#self.property(elem, 'buttonLabel', 'buttonLabel', '')
		# No equivalent
		#self.property(elem, 'oneShot', 'oneShot', '')
		# No equivalent
		#self.property(elem, 'multipleInstances', 'multipleInstances', '')
		# No equivalent
		#self.property(elem, 'requiredHostName', 'requiredHostName', '')
		# No equivalent
		#self.property(elem, 'initialDelay', 'initialDelay', '')
		#self.property(elem, 'topShadowColor', 'topShadowColor', 'color')
		# No equivalent
		#self.property(elem, 'password', 'password', '')
		# No equivalent (but numCmds is parsed to produce QEPushButton or QEMenuButton)
		#self.property(elem, 'numCmds', 'numCmds', '')
		# No equivalent
		#self.property(elem, 'includeHelpIcon', 'includeHelpIcon', '')
		# No equivalent
		#self.property(elem, 'swapButtons', 'swapButtons', '')
		#self.property(elem, 'botShadowColor', 'botShadowColor', 'color')
		#self.property(elem, 'fgColor', 'fgColor', 'color')

		self.defaultStyle(elem)
		self.endWidget(elem)
		return elem

	## Override of BaseWidget::defaultStyle, to apply the stylesheet to
	## the underlying QPushButton instead of QEMenuButton.  This is necessary
	## because QEMenuButton does not inherit from QPushButton.
	## @param parent the XML element parent
	## @param props a dictionary of stylesheetprop=>edmprop names
	## @param pressedprops a dict of stylesheetprop=>edmprop names to be applied like "widgetType():pressed {}"
	## @return boolean True if the style is applied
	def defaultStyle(self, parent, props={'background-color':'bgColor', 'color':'fgColor'}, pressedprops={}):
		if not self.isMenuButton():
			return super(shellCmdClass, self).defaultStyle(parent, props, pressedprops)

		ss = 'QPushButton { '
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

	## Is this a menu button, or a push button?
	## That is, is it linked to more than one command?
	## @return True if a menu button
	def isMenuButton(self):
		return 'numCmds' in self.widget.props and int(self.widget.props['numCmds']) > 1

	## Parse a single command
	## @param key string The index into the commands array (a string representing an integer)
	## @return tuple of cmd, args
	def parseCommand(self, key):
		cmd = self.widget.props['command'][key]
		if cmd[0] == '"' and cmd[-1] == '"': cmd = cmd[1:-1]
		spl = cmd.split(' ')
		if len(spl) > 1:
			cmd = spl[0]
			args = ' '.join(spl[1:])
			return (cmd, args)
		else:
			return (cmd, '')

	## Produce XML for the widget's menu entries.
	## @param elem the parent XML element
	## @return the created sub element
	def menuEntries(self, elem):
		root = etree.Element('MenuButton', {'Version':'1'})
		for key in list(self.widget.props['command'].keys()):
			itemelem = etree.SubElement(root, 'Item', {'Name':self.widget.props['commandLabel'][key]})
			progelem = etree.SubElement(itemelem, 'Program')
			nameelem = etree.SubElement(progelem, 'Name')
			cmd, args = self.parseCommand(key)
			nameelem.text = cmd
			if len(args) > 1:
				argselem = etree.SubElement(progelem, 'Arguments')
				argselem.text = args
			stelem = etree.SubElement(progelem, 'Start_Option')
			# start option may be "None", "Terminal", "LogOut", or "StdOut".  Since this is a shell cmd
			# widget, "Terminal" is probably most appropriate.
			stelem.text = 'Terminal'
		strng = etree.tostring(root)
		return self.stringProperty(elem, 'menuEntries', strng)
	''' NOTE: A MenuButton can have 3 types of items: programs, uis, and pvs.  It can also have submenus.
		Here's some sample xml for the menuEntries text content:
<MenuButton Version="1">
 <Item Name="ll">
  <Program>
   <Name>ll</Name>
   <Arguments></Arguments>
   <Start_Option>None</Start_Option>
  </Program>
 </Item>
 <Item Name="ls">
  <Program>
   <Name>ls</Name>
   <Arguments></Arguments>
   <Start_Option>None</Start_Option>
  </Program>
 </Item>
 <Item Name="ll -a">
  <Program>
   <Name>ls</Name>
   <Arguments>-laF</Arguments>
   <Start_Option>None</Start_Option>
  </Program>
 </Item>
 <Item Name="ls -a">
  <Program>
   <Name>ls</Name>
   <Arguments>-a</Arguments>
   <Start_Option>None</Start_Option>
  </Program>
 </Item>
 <Menu Name="submenu1">
  <Item Name="requestwf">
   <Window>
	<UiFile>requestwf.ui</UiFile>
	<MacroSubstitutions>T=Test,SYS=LI11test</MacroSubstitutions>
	<Customisation></Customisation>
	<Create_Option>Open</Create_Option>
   </Window>
  </Item>
  <Item Separator="true" Name="write pv">
   <Variable>
	<Name>test</Name>
	<Value>1</Value>
	<Format>Integer</Format>
   </Variable>
  </Item>
 </Menu></MenuButton>
 '''

	def isBuiltInWidget(self):
		return False

	def isContainer(self):
		return False

	def widgetType(self):
		if self.framework() == 'EpicsQt':
			if self.isMenuButton():
				return 'QEMenuButton'
			return 'QEPushButton'
		return 'caShellCommand'

	def widgetName(self):
		return 'shellcmd_%d' % self.count

	def widgetBaseClass(self):
		if self.framework() == 'EpicsQt':
			if self.isMenuButton():
				return 'QWidget'
			return 'QPushButton'
		return 'QWidget'
