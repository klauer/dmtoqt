from PyQt5.QtDesigner import QPyDesignerTaskMenuExtension
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import pyqtSlot

class UIParserTaskMenuExtension(QPyDesignerTaskMenuExtension):

	def __init__(self, parent):
		super(UIParserTaskMenuExtension, self).__init__(parent)

		self.importAction = QAction(self.tr("Import EPICS Screen.."), self)
		self.importAction.triggered.connect(self.doImport)

	def preferredEditAction(self):
		return self.createImportAction()

	def taskActions(self):
		return [self.createImportAction()]

	@pyqtSlot()
	def doImport(self):
		print('doImport()')

''' PURPOSE OF THIS FILE:
	This was created to test the ALS installation of PyQt5.  It worked
	(by invoking python3 UIParserTaskMenuExtension.py); however a C
	library needs to be installed in Qt Designer's plugins directory
	in order to really create python extensions.
'''
if __name__ == "__main__":
	ext = UIParserTaskMenuExtension(None)
	ext.importAction.triggered.emit()

