from FileView import *
from VARIABLES import ALLOWED_INPUT
from HelperFunctions import stripPathToFilename, scanDir, listToFilter

from PySide6.QtWidgets import(
    QWidget,
    QGridLayout,
    QPushButton,
    QFileDialog
)

from PySide6.QtCore import(
    Signal
)

from PySide6.QtGui import(
    QShortcut,
    QKeySequence
)

class InputTab(QWidget):
    convert = Signal()

    def __init__(self, settings):
        super(InputTab, self).__init__()
        self.file_view = FileView(self)

        # Apply Settings
        self.disableSorting(settings["settings"]["sorting_disabled"])

        # Shortcuts
        self.select_all_sc = QShortcut(QKeySequence('Ctrl+A'), self)
        self.select_all_sc.activated.connect(self.file_view.selectAllItems)
        self.delete_all_sc = QShortcut(QKeySequence("Ctrl+Shift+X"), self)
        self.delete_all_sc.activated.connect(self.file_view.clear)

        # UI
        input_l = QGridLayout()
        self.setLayout(input_l)
        
        add_files_btn = QPushButton(self)
        add_files_btn.setText("Add Files")
        add_files_btn.clicked.connect(self.addFiles)

        add_folder_btn = QPushButton(self)
        add_folder_btn.setText("Add Folder")
        add_folder_btn.clicked.connect(self.addFolder)

        clear_list_btn = QPushButton(self)
        clear_list_btn.setText("Clear List")
        clear_list_btn.clicked.connect(self.clearInput)

        self.convert_btn = QPushButton(self)
        self.convert_btn.setText("Convert")
        self.convert_btn.clicked.connect(self.convert.emit)

        # Positions
        input_l.addWidget(add_files_btn,1,0)
        input_l.addWidget(add_folder_btn,1,1)
        input_l.addWidget(clear_list_btn,1,2)
        input_l.addWidget(self.convert_btn,1,3,1,2)
        input_l.addWidget(self.file_view,0,0,1,0)

    def addFiles(self):
        dlg = QFileDialog()
        dlg.setWindowTitle("Add Images")
        dlg.setFileMode(QFileDialog.ExistingFiles)
        dlg.setNameFilter(listToFilter("Images", ALLOWED_INPUT))

        self.file_view.beforeAddingItems()
        filepaths = ""
        if dlg.exec():
            filepaths = dlg.selectedFiles()
            for i in filepaths:
                file_data = stripPathToFilename(i)
                self.file_view.addItem(file_data[0], file_data[1], file_data[3])
        
        self.file_view.finishAddingItems()

    def addFolder(self):
        dlg = QFileDialog()
        dlg.setWindowTitle("Add Images from a Folder")
        dlg.setFileMode(QFileDialog.Directory)
        
        self.file_view.beforeAddingItems()
        if dlg.exec():
            files = scanDir(dlg.selectedFiles()[0])
            for i in files:
                file_data = stripPathToFilename(i)
                if file_data[1] in ALLOWED_INPUT:
                    self.file_view.addItem(file_data[0], file_data[1], file_data[3])
        
        self.file_view.finishAddingItems()

    def clearInput(self):
        self.file_view.clear()
    
    def disableSorting(self, disabled):
        self.file_view.disableSorting(disabled)