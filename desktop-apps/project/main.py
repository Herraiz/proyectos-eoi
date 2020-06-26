import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QTextDocument, QFont
from PyQt5.QtWidgets import (QDockWidget, QPlainTextEdit, QFileSystemModel,
							 QTreeView, QFileDialog, QAction,
							 QMainWindow, QApplication, QMessageBox,
							 QHeaderView)


from custom_menu import Custom_menu
from messages import Message



class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.message = Message()
	

		# setting default window size
		self.resize(1500, 900)

		# menu bar & file_path
		self.file_menu = self.menuBar().addMenu("&File")
		self.file_path = None

		# Creating dock widget
		dockWidget = QDockWidget('Explorer', self)

		# Creating editor
		self.editor = QPlainTextEdit()
		self.editor.document().setDefaultFont(QFont("monospace"))
		self.editor.zoomIn(2)

		self.explorer = QTreeView()
		
		self.model = QFileSystemModel(self.explorer)
		self.root = self.model.setRootPath('../..')
		self.explorer.setModel(self.model)
		self.explorer.setRootIndex(self.root)

		self.custom_menu = Custom_menu(self, self.explorer, self.model, app)

		# Other custom tweaks
		self.explorer.setSortingEnabled(True) # allows to order by clicking on headers
		self.explorer.setMinimumWidth(400) # tweaking the explorer size
		self.explorer.setContextMenuPolicy(Qt.CustomContextMenu) # enable context menu

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


		# ACTIONS
		
		## EXPLORER

		### Double click
		self.explorer.doubleClicked.connect(self.on_double_click)

		### Right click

		self.explorer.customContextMenuRequested.connect(self.custom_menu.menu)

		## MENU BAR: FILE MENU

		### New document
		self.new_action = QAction("&New document")
		self.new_action.triggered.connect(self.new_document)
		self.new_action.setShortcut(QKeySequence.New)
		self.file_menu.addAction(self.new_action)

		### Open document
		self.open_action = QAction("&Open file...")
		self.open_action.triggered.connect(self.show_open_dialog)
		self.open_action.setShortcut(QKeySequence.Open)
		self.file_menu.addAction(self.open_action)

		### Save document
		self.save_action = QAction("&Save")
		self.save_action.triggered.connect(self.save)
		self.save_action.setShortcut(QKeySequence.Save)
		self.file_menu.addAction(self.save_action)

		### Close PyFileBrowser
		self.close_action = QAction("&Close")
		self.close_action.triggered.connect(self.close)
		self.close_action.setShortcut(QKeySequence.Quit)
		self.file_menu.addAction(self.close_action)

		## MENU BAR: HELP MENU

		### About

		self.help_menu = self.menuBar().addMenu("&Help")
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
			if not self.save():
				e.ignore()
		elif answer == QMessageBox.Cancel:
			e.ignore()
	
	def on_double_click(self, index): # TODO! not working

		''' Get the file path of the double clicked item and if it
		meet the given requirements, open that file on the editor widget.

		We must use self.explorer_file_path because if self.editor.document().isModified() 
		is True, the self.ask_for_confirmation  will use the self.file_path variable 
		and when you double click, you set a value for the variable. '''

		self.explorer_file_path = self.model.filePath(index)

		# If you double click on a directory or an image, nothing will happend
		try:
			self.open_from_explorer()

		except IsADirectoryError:
			return # default behavior
			
		except UnicodeDecodeError:
			self.message.unicode_decode_error()
	

	def new_document(self):

		''' This function creates a new document and saves if another one is open
		 and have changes '''

		self.safe_close()
		self.editor.clear()
		self.file_path = None


	def save(self):

		''' Standard save function. Will ask the file_path throught a dialog
		if there is no file_path '''

		if self.file_path is None:
			return self.show_save_dialog()
		else:
			with open(self.file_path, 'w') as f:
				f.write(self.editor.toPlainText())
			self.editor.document().setModified(False)
			return True
	

	def show_save_dialog(self):

		''' Show the save dialog is there is no file_path'''

		self.filename, _ = QFileDialog.getSaveFileName(self, 'Save as...')
		if self.filename:
			self.file_path = self.filename
			self.save()
			return True
		return False

	def safe_close(self):

		''' If the document is modified, call message.ask_for_confirmation '''

		if self.editor.document().isModified():
			answer = self.message.ask_for_confirmation()
			if answer == QMessageBox.Save:
				if not self.save():
					return
			elif answer == QMessageBox.Cancel:
				return

	

	def show_open_dialog(self):

		''' Function for open files saved on your device '''

		self.filename, _ = QFileDialog.getOpenFileName(self, 'Open...')
		if self.filename:
			file_contents = ""
			with open(self.filename, 'r') as f:
				file_contents = f.read()
			self.editor.setPlainText(file_contents)
			self.file_path = self.filename



if __name__ == '__main__':

	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()

	sys.exit(app.exec_())