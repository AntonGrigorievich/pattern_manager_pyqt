import shutil
import zipfile
import os
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog, QInputDialog, \
    QMessageBox, QRadioButton
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from app import db

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'Qt_handlers\ui_files\settings_widget.ui', self)
        self.initUI()

    def initUI(self):
        self.confirm_button.clicked.connect(self.confirm)

    def confirm(self):
        pass