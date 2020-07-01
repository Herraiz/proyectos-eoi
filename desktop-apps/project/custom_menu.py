import os
import shutil

from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMenu, QAction, QMessageBox

from messages import Message
from menu import Menu



class Custom_menu(QMenu):

    def __init__(self, main, explorer, model, editor, app):
        super().__init__()
        self.menu = Menu(main, explorer, editor, model)
        self.explorer = explorer
        self.model = model
        self.main = main
        self.editor = editor
        self.app = app
        self.message = Message()
        self.index = None
        self.index_path = None


    def context_menu(self, point):

        ''' Custom Context Menu function with some actions '''

        open_action = QAction("Open")
        open_action.triggered.connect(self.menu_open)
        self.addAction(open_action)

        rename_action = QAction("Rename")
        rename_action.triggered.connect(self.menu_rename)
        self.addAction(rename_action)

        delete_action = QAction("Delete")
        delete_action.triggered.connect(self.menu_delete_file)
        self.addAction(delete_action)

        copy_action = QAction("Copy path to clipboard")
        copy_action.triggered.connect(self.menu_copy_file_path)
        self.addAction(copy_action)

        self.exec_(QCursor.pos())


    def on_double_click(self, index):

        ''' Get the file path of the double clicked item and if it
        meet the given requirements, open that file on the editor widget '''

        self.index = index
        self.index_path = self.model.filePath(index)

        try:
            self.open_from_explorer(self.index_path)

        except IsADirectoryError:
            return # default behavior
            
        except UnicodeDecodeError:
            self.message.unicode_decode_error()

    def menu_open(self):

        ''' Open the selected file on the editor '''

        # Extracting the file_path (as explorer_file_path)
        self.index = self.explorer.currentIndex()
        self.index_path = self.model.filePath(self.index)

        try:
            self.open_from_explorer(self.index_path)

        except IsADirectoryError:
            self.explorer.expand(self.index) 

        except UnicodeDecodeError:
            self.message.unicode_decode_error()


    def menu_rename(self):

        ''' Renaming selected file or directory '''

        self.index = self.explorer.currentIndex()
        self.explorer.edit(self.index)


    def menu_delete_file(self):
        
        ''' Delete selected file or directory '''

        self.index = self.explorer.currentIndex()
        self.index_path = self.model.filePath(self.index)
        filename = self.model.fileName(self.index)

        try:
            os.remove(self.index_path)

        except IsADirectoryError: # for empty folders
            try:
                os.rmdir(self.index_path)

            except OSError: # for remove recursively a directory
                    answer = self.message.ask_for_delete_confirmation(filename)
                    if answer == QMessageBox.Yes:
                        shutil.rmtree(self.index_path)
                    elif answer == QMessageBox.Cancel:
                        return

    def menu_copy_file_path(self):

        ''' Extract the path and paste it on the clipboard '''
        
        self.index = self.explorer.currentIndex()
        self.index_path = self.model.filePath(self.index)
        self.app.clipboard().setText(self.index_path)


    def open_from_explorer(self, path):

        ''' This function open the file at the given path on the editor '''
        
        self.menu.safe_close()
        file_contents = ""
        with open(path, 'r') as f:
            file_contents = f.read()
        self.editor.setPlainText(file_contents)

        # We save the file_path again so that save() works correctly	
        self.main.file_path = path 
