import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QTextDocument, QFont
from PyQt5.QtWidgets import (QDockWidget, QPlainTextEdit, QFileSystemModel,
							 QTreeView, QFileDialog, QAction,
							 QMainWindow, QApplication, QMessageBox,
							 QHeaderView)


from custom_menu import Custom_menu
from messages import Message
from menu import Menu



class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		dockWidget = QDockWidget('Explorer', self)

		self.editor = QPlainTextEdit()
		self.editor.document().setDefaultFont(QFont("monospace"))
		self.editor.zoomIn(2)

		self.explorer = QTreeView()
		
		self.model = QFileSystemModel(self.explorer)
		self.root = self.model.setRootPath('../..')
		self.explorer.setModel(self.model)
		self.explorer.setRootIndex(self.root)
		self.file_path = None

		self.custom_menu = Custom_menu(self, self.explorer, self.model, self.editor, app)
		self.menu = Menu(self, self.explorer, self.editor, self.model, self.custom_menu)
		self.message = Message()

		# Other custom tweaks
		self.explorer.setSortingEnabled(True)
		self.explorer.setMinimumWidth(400)
		self.explorer.setContextMenuPolicy(Qt.CustomContextMenu)
		self.resize(1500, 900)

		# Enabling renaming on context menu
		self.model.setReadOnly(False) 
		self.explorer.setEditTriggers(self.explorer.NoEditTriggers)

		# Change default column width
		self.header = self.explorer.header()
		self.header.setSectionResizeMode(0, QHeaderView.Interactive)
		self.header.setDefaultSectionSize(200)
		self.header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
		self.header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

		# Setting editor as central widget
		self.setCentralWidget(self.editor)
		self.addDockWidget(Qt.LeftDockWidgetArea, dockWidget)

		# Setting view as widget of dock widget
		dockWidget.setWidget(self.explorer)
		dockWidget.setFloating(False)

		### Double click
		self.explorer.doubleClicked.connect(self.menu.on_double_click)

		### Right click

		self.explorer.customContextMenuRequested.connect(self.custom_menu.context_menu)



	def closeEvent(self, e):

		'''This function prevents from closing without saving,
		 it works with the "Close" event'''

		if not self.editor.document().isModified():
			return
		answer = self.message.ask_for_confirmation()
		if answer == QMessageBox.Save:
			if not self.menu.save():
				e.ignore()
		elif answer == QMessageBox.Cancel:
			e.ignore()



if __name__ == '__main__':

	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()

	sys.exit(app.exec_())