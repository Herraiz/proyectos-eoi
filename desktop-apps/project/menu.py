
from PyQt5.QtGui import QCursor, QKeySequence
from PyQt5.QtWidgets import QMenu, QAction, QMessageBox

from messages import Message

class Menu(QMenu):

    def __init__(self, main, explorer, editor):
        super().__init__()
        self.explorer = explorer
        self.editor = editor
        self.main = main
        self.message = Message()
        self.file_menu = self.main.menuBar().addMenu("&File")
        self.help_menu = self.main.menuBar().addMenu("&Help")

        self.new_action = QAction("&New document")
        self.new_action.triggered.connect(self.new_document)
        self.new_action.setShortcut(QKeySequence.New)
        self.file_menu.addAction(self.new_action)

        # self.file_menu.addAction(self.open_action)
        # self.file_menu.addAction(self.save_action)
        # self.file_menu.addAction(self.close_action)
        # self.help_menu.addAction(self.about_action)
            

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