import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QTextDocument, QFont
from PyQt5.QtWidgets import (QDockWidget, QPlainTextEdit, QFileSystemModel,
							 QTreeView, QMainWindow,
							 QApplication, QMessageBox, QHeaderView)
							 


from custom_menu import Custom_menu
from messages import Message
from menu import Menu
from explorer import Explorer



class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		dockWidget = QDockWidget('Explorer', self)

		self.editor = QPlainTextEdit()
		self.editor.document().setDefaultFont(QFont("monospace"))
		self.editor.zoomIn(2)

		self.explorer = Explorer()
		self.model = QFileSystemModel(self.explorer)
		self.file_path = None

		# Menu bar
		self.file_menu = self.menuBar().addMenu("&File")
		self.help_menu = self.menuBar().addMenu("&Help")

		# Instances of Menus and message
		self.custom_menu = Custom_menu(self, self.model, self.editor, app)
		self.menu = Menu(self, self.editor, self.model)
		self.message = Message()

		self.resize(1500, 900)

		# Setting editor as central widget
		self.setCentralWidget(self.editor)
		self.addDockWidget(Qt.LeftDockWidgetArea, dockWidget)

		# Setting view as widget of dock widget
		dockWidget.setWidget(self.explorer)
		dockWidget.setFloating(False)

		### Double click
		self.explorer.doubleClicked.connect(self.custom_menu.on_double_click)

		### Right click
		self.explorer.customContextMenuRequested.connect(self.custom_menu.context_menu)


	def closeEvent(self, e): #TODO: Sacar closeevent y quitar menu, no hace falta.

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