from PyQt5.QtDesigner import QPyDesignerCustomWidgetInterface

class UIParserWidgetInterface(QPyDesignerCustomWidgetInterface):

	def __init__(self, parent=None):
		super(UIParserWidgetInterface, self).__init__(parent)
		self.initialized = False

	def initialize(self, qDesignerFormEditorInterface):
		if self.initialized:
			return
		self.initialized = True

	def isInitialized(self):
		return self.initialized
		pass

	# These methods are not needed, but pure virtual in the base class:
	def isContainer(self):
		return False

	def icon(self):
		return None

	def domXml(self):
		return ""

	def group(self):
		return 'EPICS UI Parser'

	def includeFile(self):
		return ""

	def name(self):
		return 'EPICSUIParser'

	def toolTip(self):
		return 'Convert EPICS EDM files to Qt Designer UI'

	def whatsThis(self):
		return ""

	def createWidget(self, parent):
		return None

