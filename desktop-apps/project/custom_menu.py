import os
import shutil

from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMenu, QAction, QMessageBox

from messages import Message


class Custom_menu(QMenu):

    def __init__(self, main, explorer, model, app):
        super().__init__()
        self.explorer = explorer
        self.model = model
        self.main = main
        self.app = app
        self.message = Message()


    def menu(self, point):

        ''' Custom Context Menu function with some actions '''


        ## ACTIONS

        ## Opening the document
        open_action = QAction("Open")
        open_action.triggered.connect(self.menu_open)
        self.addAction(open_action)

        ## Rename file
        rename_action = QAction("Rename")
        rename_action.triggered.connect(self.menu_rename)
        self.addAction(rename_action)

        ## Copy file path to clipboard
        delete_action = QAction("Delete")
        delete_action.triggered.connect(self.menu_delete_file)
        self.addAction(delete_action)

        ## Copy file path to clipboard
        copy_action = QAction("Copy path to clipboard")
        copy_action.triggered.connect(self.menu_copy_file_path)
        self.addAction(copy_action)

        # Opening the context menu at the cursor position
        self.exec_(QCursor.pos())


    def menu_open(self):

        ''' Open the selected file on the editor.
        If it's a image file, don't do nothing. 
        If it's a directory, it expands it '''

        # Extracting the file_path (as explorer_file_path)
        index = self.explorer.currentIndex()
        self.explorer_file_path = self.model.filePath(index)

        try:
            self.open_from_explorer()

        except IsADirectoryError:
            self.explorer.expand(index) 

        except UnicodeDecodeError:
            self.message.unicode_decode_error()


    def menu_rename(self):

        ''' Renaming selected file or directory '''

        index = self.explorer.currentIndex()
        self.explorer.edit(index)


    def menu_delete_file(self):
        
        ''' Delete selected file or directory '''

        index = self.explorer.currentIndex()
        self.explorer_file_path = self.model.filePath(index)
        filename = self.model.fileName(index)

        try:
            os.remove(self.explorer_file_path)

        except IsADirectoryError: # for empty folders
            try:
                os.rmdir(self.explorer_file_path)

            except OSError: # for remove recursively a directory
                    answer = self.message.ask_for_delete_confirmation(filename)
                    if answer == QMessageBox.Yes:
                        shutil.rmtree(self.explorer_file_path)
                    elif answer == QMessageBox.Cancel:
                        return

    def menu_copy_file_path(self):

        ''' Extract the path and paste it on the clipboard '''
        
        index = self.explorer.currentIndex()
        self.explorer_file_path = self.model.filePath(index)
        self.app.clipboard().setText(self.explorer_file_path)


    def open_from_explorer(self):

        ''' This function open the file on the current self.file_path in the editor '''
        
        self.main.safe_close()
        file_contents = ""
        # self.explorer_file_path = self.file_path
        with open(self.explorer_file_path, 'r') as f:
            file_contents = f.read()
        self.main.editor.setPlainText(file_contents)
        # We save the file_path again so that self.save() works correctly	
        self.file_path = self.explorer_file_path 
