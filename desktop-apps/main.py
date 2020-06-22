from os.path import expanduser
import sys

from PyQt5.QtGui import QKeySequence, QTextDocument, QFont, QCursor
from PyQt5.QtWidgets import (QDockWidget, QPlainTextEdit, QDirModel,
							 QTreeView, QDockWidget, QFileDialog,
							 QMainWindow, QApplication, QAction,
							 QMessageBox, QHeaderView, QMenu)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		# setting default window size
		self.resize(1700, 900)

		# menu bar
		self.file_menu = self.menuBar().addMenu("&File")
		self.file_path = None # esto igual no hace falta

		# Creating dock widget
		dockWidget = QDockWidget('PyFileExplorer', self)

		# Creating editor
		self.editor = QPlainTextEdit()
		self.editor.document().setDefaultFont(QFont("monospace"))
		self.editor.zoomIn(3)

		# Creating Treeview
		self.home = expanduser('..')
		self.model = QDirModel()
		self.explorer = QTreeView()
		self.explorer.setSortingEnabled(True) # allows to order by clicking on headers
		self.explorer.setModel(self.model)
		self.explorer.setRootIndex(self.model.index(self.home))
		self.explorer.setMinimumWidth(400)
		self.explorer.setContextMenuPolicy(Qt.CustomContextMenu)

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


		### ACTIONS
		
		## EXPLORER

		# Double click
		self.explorer.doubleClicked.connect(self.on_double_click)

		# Right click

		self.explorer.customContextMenuRequested.connect(self.custom_menu)

		## MENU BAR

		# New document
		self.new_action = QAction("&New document")
		self.new_action.triggered.connect(self.new_document)
		self.new_action.setShortcut(QKeySequence.New)
		self.file_menu.addAction(self.new_action)

		# Open document
		self.open_action = QAction("&Open file...")
		self.open_action.triggered.connect(self.show_open_dialog)
		self.open_action.setShortcut(QKeySequence.Open)
		self.file_menu.addAction(self.open_action)

		# Save document
		self.save_action = QAction("&Save")
		self.save_action.triggered.connect(self.save)
		self.save_action.setShortcut(QKeySequence.Save)
		self.file_menu.addAction(self.save_action)

		# Close PyFileBrowser
		self.close_action = QAction("&Close")
		self.close_action.triggered.connect(self.close)
		self.close_action.setShortcut(QKeySequence.Quit)
		self.file_menu.addAction(self.close_action)

	def closeEvent(self, e):

		'''This function prevents from closing without saving'''

		if not self.editor.document().isModified():
			return
		answer = self.ask_for_confirmation()
		if answer == QMessageBox.Save:
			if not self.save():
				e.ignore()
		elif answer == QMessageBox.Cancel:
			e.ignore()
	
	def on_double_click(self, index):
		'''
		This function get the file path of the double clicked item and if it
		meet the given requirements, open that file on the editor widget.

		Attention! We must use self.explorer_file_path becouse if 
		self.editor.document().isModified() is True, the self.ask_for_confirmation 
		will use the self.file_path variable and when you double click, 
		you set a value for the variable.
		'''

		self.explorer_file_path = self.model.filePath(index)
		# If you double click on a directory or an image, nothing will happend
		try:
			self.open_from_explorer()
		except IsADirectoryError:
			return
		except UnicodeDecodeError:
			return
	
	def open_from_explorer(self):
		'''
		This function open the file on the current self.file_path in the editor
		'''
		if self.editor.document().isModified():
			answer = self.ask_for_confirmation()
			if answer == QMessageBox.Save:
				if not self.save():
					return
			elif answer == QMessageBox.Cancel:
				return
		file_contents = ""
		# self.explorer_file_path = self.file_path
		with open(self.explorer_file_path, 'r') as f:
			file_contents = f.read()
		self.editor.setPlainText(file_contents)
		# We save the file_path again so that self.save () works correctly	
		self.file_path = self.explorer_file_path 

	def new_document(self):
		'''
		This function creates a new document and saves if another one is open
		 and have changes
		'''
		if self.editor.document().isModified():
			answer = self.ask_for_confirmation()
			if answer == QMessageBox.Save:
				if not self.save():
					return
			elif answer == QMessageBox.Cancel:
				return
		self.editor.clear()
		self.file_path = None


	def save(self):
		'''
		Standard save function. Will ask the file_path throught a dialog
		if there is no file_path
		'''

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


	def ask_for_confirmation(self): 

		''' Prevents leaving without saving '''

		answer = QMessageBox.question(self, "Confirm closing",
					"You have unsaved changes. Are you sure you want to exit?", 
					QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
		return answer
	

	def show_open_dialog(self):

		''' Function for open files saved on your device '''

		self.filename, _ = QFileDialog.getOpenFileName(self, 'Open...')
		if self.filename:
			file_contents = ""
			with open(self.filename, 'r') as f:
				file_contents = f.read()
			self.editor.setPlainText(file_contents)
			self.file_path = self.filename


	def custom_menu(self, event):

		''' Custom Context Menu function with some actions '''

		# Creamos el menú
		menu = QMenu(self)
		self.event = event
		print(self.event)
		# Abrimos el fichero
		open_action = QAction("&Abrir fichero")
		open_action.triggered.connect(self.menu_open_file)
		menu.addAction(open_action)

		menu.addAction("Renombrar")
		menu.addAction("Borrar")
		menu.addAction("Copiar ruta en el portapapeles")

		# Abrimos el menu en la posición del cursor	
		menu.exec_(QCursor.pos())

	def menu_open_file(self): # TODO: NO FUNCIONA

		'''
		With open the selected file on the editor if it's not a 
		directory or a image file
		'''

		self.explorer_file_path = self.model.filePath(self.event)
		if self.editor.document().isModified():
			answer = self.ask_for_confirmation()
			if answer == QMessageBox.Save:
				if not self.save():
					return
			elif answer == QMessageBox.Cancel:
				return
		file_contents = ""
		with open(self.explorer_file_path, 'r') as f:
			file_contents = f.read()
		self.editor.setPlainText(file_contents)	

if __name__ == '__main__':

	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()

	sys.exit(app.exec_())