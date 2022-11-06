import shutil
import zipfile
import os
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog, QInputDialog, \
    QMessageBox, QRadioButton
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from app import db

class ChoiceWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'Qt_handlers\ui_files\choice_widget.ui', self)
        self.initUI()

    def initUI(self):
        self.pattern_choose_button.clicked.connect(self.choose_pattern)

    def choose_pattern(self):
        res = self.sender()
        if res.isChecked():
            print(res.text)