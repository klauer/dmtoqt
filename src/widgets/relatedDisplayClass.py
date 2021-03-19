###########################################################################
# Copyright (c) 2017 The Regents of the University of California
# This file is distributed subject to a Software License Agreement found
# in the file LICENSE that is included with this distribution.
###########################################################################
from src.widgets.BaseWidget import BaseWidget
import logging
import src.widgets
from lxml import etree

class relatedDisplayClass(BaseWidget):
	''' Depending on the chosen framework and widget properties, produces either a
		QEMenuButton, a QEPushButton, a caRelatedDisplay, or a QWidget
	'''

	count = 0
	@staticmethod
	def incrcount():
		relatedDisplayClass.count += 1
		return relatedDisplayClass.count

	def __init__(self, widget):
		self.logger = logging.getLogger(self.__class__.__name__)
		super(relatedDisplayClass, self).__init__(widget)
		self.count = relatedDisplayClass.incrcount()

	def menuEntries(self, elem):
		''' Constructs the xml for menu entries.

			Sample xml might look like::

				<MenuButton Version="1">
					<Item Name="requestwf">
						<Window>
							<UiFile>requestwf.ui</UiFile>
							<MacroSubstitutions>T=Test,SYS=LI11test</MacroSubstitutions>
							<Customisation></Customisation>
							<Create_Option>Open</Create_Option>
						</Window>
					</Item>
				</MenuButton>

		'''
		root = etree.Element('MenuButton', {'Version':'1'})
		for key in list(self.widget.props['displayFileName'].keys()):
			if key in self.widget.props['menuLabel']:
				label = self.widget.props['menuLabel'][key]
			else:
				''' No label; ignore this entry '''
				continue
			fname = self.widget.props['displayFileName'][key]
			if fname.endswith('.edl'):
				fname = fname[0:-4]
			fname += '.ui'
			itemelem = etree.SubElement(root, 'Item', {'Name':label})
			windelem = etree.SubElement(itemelem, 'Window')
			uielem = etree.SubElement(windelem, 'UiFile')
			uielem.text = fname
			mselem = etree.SubElement(windelem, 'MacroSubstitutions')
			if 'symbols' in self.widget.props and key in self.widget.props['symbols']:
				macros = self.widget.props['symbols'][key]
				mselem.text = macros
			custelem = etree.SubElement(windelem, 'Customization')
			createelem = etree.SubElement(windelem, 'Create_Option')
			co = 'NewWindow'
			if 'closeDisplay' in self.widget.props \
				and key in self.widget.props['closeDisplay'] \
				and self.widget.props['closeDisplay'][key] == '1':
				co = 'Open' # replaces current GUI
			createelem.text = co
		strng = etree.tostring(root)
		return self.stringProperty(elem, 'menuEntries', strng)

	def widgetUI(self, parent):
		elem = self.startWidget(parent)
		if self.framework() == 'EpicsQt':
			if 'buttonLabel' in self.widget.props:
				self.stringProperty(elem, 'labelText', self.widget.props['buttonLabel'])
				self.stringProperty(elem, 'toolTip', self.widget.props['buttonLabel'])
				self.stringProperty(elem, 'statusTip', self.widget.props['buttonLabel'])
			if 'displayFileName' in self.widget.props:
				if len(self.widget.props['displayFileName']) > 1:
					self.menuEntries(elem)
				else:
					fname = self.widget.props['displayFileName']['0']
					if fname.endswith('.edl'):
						fname = fname[0:-4]
					fname += '.ui'
					self.stringProperty(elem, 'guiFile', fname)
					if 'symbols' in self.widget.props and '0' in self.widget.props['symbols']:
						self.stringProperty(elem, 'prioritySubstitutions', self.widget.props['symbols']['0'])
				if self.widgetType() == 'QEPushButton':
					co = 'NewWindow'
					if 'closeDisplay' in self.widget.props \
						and '0' in self.widget.props['closeDisplay'] \
						and self.widget.props['closeDisplay']['0'] == '1':
						co = 'Open' # replaces current GUI
					self.enumProperty(elem, 'creationOption', co)
			self.defaultStyle(elem)
		else: # caRelatedDisplay
			if 'buttonLabel' in self.widget.props:
				self.stringProperty(elem, 'label', self.widget.props['buttonLabel'])
			nDsps = int(self.widget.props['numDsps'])
			if 'displayFileName' in self.widget.props:
				fnames = []
				labels = []
				rpl = []
				for fname in list(self.widget.props['displayFileName'].values()):
					if fname.endswith('.edl'):
						fname = fname[0:-3]+'ui'
					fnames.append(fname)
				if 'menuLabel' in self.widget.props:
					for label in list(self.widget.props['menuLabel'].values()):
						labels.append(label)
				if 'closeDisplay' in self.widget.props:
					for cd in list(self.widget.props['closeDisplay'].values()):
						if cd == '1': rpl.append('true')
						else: rpl.append('false')
				for i in range(len(fnames), nDsps):
					fnames.append('(none)')
				for i in range(len(labels), nDsps):
					labels.append('(none)')
				for i in range(len(rpl), nDsps):
					rpl.append('false')
				self.stringProperty(elem, 'files', ';'.join(fnames))
				self.stringProperty(elem, 'labels', ';'.join(labels))
				self.stringProperty(elem, 'removeParent', ';'.join(rpl))
		#self.property(elem, 'button3Popup', 'button3Popup', 'unknowntype')
		#self.property(elem, 'noEdit', 'noEdit', 'unknowntype')
		#self.property(elem, 'symbols', 'symbols', 'unknowntype')
		#self.property(elem, 'bgColor', 'bgColor', 'color')
		#self.property(elem, 'numDsps', 'numDsps', 'unknowntype')
		#self.property(elem, 'colorPv', 'colorPv', 'unknowntype')
		self.property(elem, 'font', 'font', 'font')
		#self.property(elem, 'buttonLabel', 'buttonLabel', 'string')
		#self.property(elem, 'replaceSymbols', 'replaceSymbols', 'unknowntype')
		#self.property(elem, 'pv', 'pv', 'unknowntype')
		#self.property(elem, 'propagateMacros', 'propagateMacros', 'unknowntype')
		#self.property(elem, 'useFocus', 'useFocus', 'unknowntype')
		#self.property(elem, 'allowDups', 'allowDups', 'unknowntype')
		#self.property(elem, 'xPosOffset', 'xPosOffset', 'unknowntype')
		#self.property(elem, 'topShadowColor', 'topShadowColor', 'color')
		#self.property(elem, 'yPosOffset', 'yPosOffset', 'unknowntype')
		#self.property(elem, 'displayFileName', 'displayFileName', 'unknowntype')
		#self.property(elem, 'closeAction', 'closeAction', 'unknowntype')
		#self.property(elem, 'invisible', 'invisible', 'boolean')
		#self.property(elem, 'icon', 'icon', 'unknowntype')
		#self.property(elem, 'menuLabel', 'menuLabel', 'unknowntype')
		#self.property(elem, 'closeDisplay', 'closeDisplay', 'unknowntype')
		#self.property(elem, 'value', 'value', 'unknowntype')
		#self.property(elem, 'cascade', 'cascade', 'unknowntype')
		#self.property(elem, 'swapButtons', 'swapButtons', 'unknowntype')
		#self.property(elem, 'numPvs', 'numPvs', 'unknowntype')
		#self.property(elem, 'botShadowColor', 'botShadowColor', 'color')
		#self.property(elem, 'fgColor', 'fgColor', 'color')
		return elem

	def widgetType(self):
		if self.framework() == 'EpicsQt':
			if self.isMenuButton():
				return 'QEMenuButton'
			return 'QEPushButton'
		return 'caRelatedDisplay'

	def widgetName(self):
		return 'relateddisplay_%d' % self.count

	def isBuiltInWidget(self):
		return False

	def widgetBaseClass(self):
		if self.framework() == 'EpicsQt':
			if self.isMenuButton():
				return 'QWidget'
			return 'QPushButton'
		return 'QWidget'

	def isMenuButton(self):
		return 'numDsps' in self.widget.props and int(self.widget.props['numDsps']) > 1
