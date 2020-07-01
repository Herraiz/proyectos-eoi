import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QTextDocument, QFont
from PyQt5.QtWidgets import (QDockWidget, QPlainTextEdit, QFileSystemModel,
							 QTreeView, QFileDialog, QMainWindow, QAction,
							 QApplication, QMessageBox, QHeaderView)
							 


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

		# Menu bar
		self.file_menu = self.menuBar().addMenu("&File")
		self.help_menu = self.menuBar().addMenu("&Help")

		### Double click
		self.explorer.doubleClicked.connect(self.custom_menu.on_double_click)

		### Right click
		self.explorer.customContextMenuRequested.connect(self.custom_menu.context_menu)

		self.menu_actions()

	def menu_actions(self):

		self.new_action = QAction("&New document")
		self.new_action.triggered.connect(self.menu.new_document)
		self.new_action.setShortcut(QKeySequence.New)
		self.file_menu.addAction(self.new_action)

		self.open_action = QAction("&Open file...")
		self.open_action.triggered.connect(self.menu.show_open_dialog)
		self.open_action.setShortcut(QKeySequence.Open)
		self.file_menu.addAction(self.open_action)       

		self.save_action = QAction("&Save")
		self.save_action.triggered.connect(self.menu.save)
		self.save_action.setShortcut(QKeySequence.Save)
		self.file_menu.addAction(self.save_action)

		self.close_action = QAction("&Close")
		self.close_action.triggered.connect(self.close)
		self.close_action.setShortcut(QKeySequence.Quit)
		self.file_menu.addAction(self.close_action)

		self.about_action = QAction("&About")
		self.about_action.triggered.connect(self.message.show_about_dialog)
		self.help_menu.addAction(self.about_action) 

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