
from PyQt5.QtGui import QCursor, QKeySequence
from PyQt5.QtWidgets import QMenu, QAction, QMessageBox, QFileDialog

from messages import Message

class Menu(QMenu):

    def __init__(self, main, explorer, editor, model, custom_menu):
        super().__init__()
        self.explorer = explorer
        self.editor = editor
        self.model = model
        self.main = main
        self.message = Message()
        self.custom_menu = custom_menu

    def new_document(self):

        ''' This function creates a new document and saves if another one is open
            and have changes '''

        self.safe_close()
        self.editor.clear()
        self.main.file_path = None

    def save(self):

        ''' Standard save function. Will ask the file_path throught a dialog
        if there is no file_path '''

        if self.main.file_path is None:
            return self.show_save_dialog()
        else:
            with open(self.main.file_path, 'w') as f:
                f.write(self.editor.toPlainText())
            self.editor.document().setModified(False)
            return True


    def show_save_dialog(self):

        ''' Show the save dialog is there is no file_path'''

        self.filename, _ = QFileDialog.getSaveFileName(self, 'Save as...')
        if self.filename:
            self.main.file_path = self.filename
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
            self.main.file_path = self.filename