from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QKeySequence, QTextDocument, QFont
from PyQt5.QtWidgets import QFileSystemModel, QTreeView, QHeaderView


class Explorer(QTreeView):
    def __init__(self):
        super().__init__()
        self.model = QFileSystemModel(self)
        self.root = self.model.setRootPath('../..')
        self.setModel(self.model)
        self.setRootIndex(self.root)

        # Some custom tweaks
        self.setSortingEnabled(True)
        self.setMinimumWidth(400)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

		# Enabling renaming on context menu
        self.model.setReadOnly(False) 
        self.setEditTriggers(self.NoEditTriggers)

        # Change default column width
        self.header = self.header()
        self.header.setSectionResizeMode(0, QHeaderView.Interactive)
        self.header.setDefaultSectionSize(200)
        self.header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
