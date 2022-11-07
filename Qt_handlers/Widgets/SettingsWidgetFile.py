import zipfile
import os
import shutil
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QWidget, QFileDialog

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'Qt_handlers\ui_files\settings_widget.ui', self)
        self.initUI()

    def initUI(self):
        self.confirm_button.clicked.connect(self.confirm)

    def confirm(self):
        self.prefered_modules = []
        for box in self.chckboxes:
            if box.isChecked():
                self.prefered_modules.append(box.text())
        direct = QFileDialog.getExistingDirectory(self, 'Where should we put your folder?', '.')
        try:
            os.mkdir(f'{direct}/{self.folder_name}')
            file_zip = zipfile.ZipFile(self.directory, 'r')
            file_zip.extractall(f'{direct}/{self.folder_name}')
            # print(os.listdir(f'extract'))
            for file in os.listdir(f'{direct}/{self.folder_name}'):
                if file not in self.prefered_modules:
                    try:
                        os.remove(f'{direct}/{self.folder_name}/{file}')
                    except Exception:
                        shutil.rmtree(f'{direct}/{self.folder_name}/{file}')
            self.hide()
        except Exception:
            self.examples_lable.setText("Couldn't make the folder, please try to change folder name")