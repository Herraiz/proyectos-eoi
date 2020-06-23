import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import (
        Qt, QAbstractTableModel, QVariant)

app = QApplication(sys.argv)
treeView = QTreeView()
fileSystemModel = QFileSystemModel(treeView)
fileSystemModel.setReadOnly(False)
root = fileSystemModel.setRootPath('..')
treeView.setModel(fileSystemModel)
treeView.setRootIndex(root)
treeView.show()
app.exec_()