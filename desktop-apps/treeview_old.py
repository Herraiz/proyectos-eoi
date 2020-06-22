from os.path import expanduser
from PyQt5.QtGui import QKeySequence, QTextDocument, QFont
from PyQt5.QtWidgets import *
# from PyQt5.QtCore import QFile

home = expanduser('./Proyectos/proyectos-eoi/')

app = QApplication([])
app.setApplicationName('PyFileBrowser')

#### inicio pynotepad


editor = QPlainTextEdit()
editor.document().setDefaultFont(QFont("monospace"))

def ask_for_confirmation():
    answer = QMessageBox.question(right_window, "Confirm closing",
                "You have unsaved changes. Are you sure you want to exit?", 
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
    return answer

class MyEditorWindow(QMainWindow):
    def closeEvent(self, e):
        if not editor.document().isModified():
            return
        answer = ask_for_confirmation()
        if answer == QMessageBox.Save:
            if not save():
                e.ignore()
        elif answer == QMessageBox.Cancel:
            e.ignore()

# IMPORTANTE
window = QWidget()
left_window = QMainWindow()
right_window = MyEditorWindow()



file_menu = left_window.menuBar().addMenu("&File")
file_path = None

def new_document():
    global file_path
    if editor.document().isModified():
        answer = ask_for_confirmation()
        if answer == QMessageBox.Save:
            if not save():
                return
        elif answer == QMessageBox.Cancel:
            return
    editor.clear()
    file_path = None


new_action = QAction("&New document")
new_action.triggered.connect(new_document)
new_action.setShortcut(QKeySequence.New)
file_menu.addAction(new_action)

def show_open_dialog():
    global file_path
    filename, _ = QFileDialog.getOpenFileName(right_window, 'Open...')
    if filename:
        file_contents = ""
        with open(filename, 'r') as f:
            file_contents = f.read()
        editor.setPlainText(file_contents)
        file_path = filename

open_action = QAction("&Open file...")
open_action.triggered.connect(show_open_dialog)
open_action.setShortcut(QKeySequence.Open)
file_menu.addAction(open_action)

def save():
    if file_path is None:
        return show_save_dialog()
    else:
        with open(file_path, 'w') as f:
            f.write(editor.toPlainText())
        editor.document().setModified(False)
        return True

def show_save_dialog():
    global file_path
    filename, _ = QFileDialog.getSaveFileName(right_window, 'Save as...')
    if filename:
        file_path = filename
        save()
        return True
    return False

def open_from_filebrowser(file_path):
    file_contents = ""
    with open(file_path, 'r') as f:
        file_contents = f.read()
    editor.setPlainText(file_contents)


save_action = QAction("&Save")
save_action.triggered.connect(save)
save_action.setShortcut(QKeySequence.Save)
file_menu.addAction(save_action)

close_action = QAction("&Close")
close_action.triggered.connect(right_window.close)
close_action.setShortcut(QKeySequence.Quit)
file_menu.addAction(close_action)

def show_about_dialog():
    text = """
        <center>
            <h1>PyNotepad</h1><br/>
            <img src=logo.png width=200 height=200>
        </center>
        <p>Version 0.0.1</p>
    """
    QMessageBox.about(right_window, "About PyNotepad", text)


help_menu = left_window.menuBar().addMenu("&Help")
about_action = QAction("&About")
about_action.triggered.connect(show_about_dialog)
help_menu.addAction(about_action)

right_window.setCentralWidget(editor)

#### fin pynotepad

#### inicio tree view



model = QDirModel()
view = QTreeView()
# view.setExpandsOnDoubleClick(False) ## activa que se tenga que usar doble click para expandir
view.setSortingEnabled(True) # permite ordenar
view.resizeColumnToContents(True) # esto no rula
view.setModel(model)
view.setRootIndex(model.index(home))

def on_double_click(index):
    '''
    This function get the filepath of the double clicked item and if it
    meet the given requirements, open that file on the editor widget.
    '''
    global file_path
    file_path= model.filePath(index)
    open_from_filebrowser(file_path)

view.doubleClicked.connect(on_double_click)

#### fin treeview

layout2 = QVBoxLayout()
layout2.addWidget(left_window)

layout = QHBoxLayout()
layout2.insertLayout(1, layout, stretch=1)
layout.addWidget(view, 35)

layout.addWidget(right_window, 65)


window.setLayout(layout2)


window.resize(1700, 900)
window.show()
app.exec()