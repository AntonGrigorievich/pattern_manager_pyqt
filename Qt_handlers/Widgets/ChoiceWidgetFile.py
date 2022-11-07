import shutil
import zipfile
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QCheckBox
from app import db
from Qt_handlers.Widgets.SettingsWidgetFile import SettingsWidget

class ChoiceWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'Qt_handlers\ui_files\choice_widget.ui', self)
        self.initUI()

    def initUI(self):
        pass

    def choose_pattern(self):
        try:
            shutil.rmtree('extract')
        except Exception:
            pass
        os.mkdir('extract')
        res = self.sender()
        if res.isChecked():
            print(res.text)
            # file_zip = zipfile.ZipFile(f'patterns\\{res.text}.zip', 'rb')
            # file_zip.extractall('extract')
            # file_zip.close()
            # -----------------------
            # with zipfile.ZipFile(f'patterns\\{res.text}.zip') as file_zip:
            #     for item in file_zip.infolist():
            #         file_zip.extract(item, path='extract')
            # print(os.listdir(f'extract'))
            # -----------------------
            # file_zip = f'patterns\\{res.text}.zip'
            # if file_zip.endswith("tar.gz"):
            #     tar = tarfile.open(zipfile, "r:gz")
            # elif file_zip.endswith("tar"):
            #     tar = tarfile.open(zipfile, "r:")
            # tar.extractall('extract')
            # tar.close()
        try:
            direct = db.sql_get_pattern_orig_dir(db, res.text)
            print('dir:', direct)
            file_zip = zipfile.ZipFile(direct, 'r')
            file_zip.extractall('extract')
            print(os.listdir(f'extract'))
            file_zip.close()
            self.settings_widg = SettingsWidget()
            self.settings_widg.directory = direct
            self.settings_widg.folder_name = self.folder_name
            self.settings_widg.modules = os.listdir(f'extract')
            self.settings_widg.chckboxes = []
            for module in self.settings_widg.modules:
                checkbox = QCheckBox(module, self.settings_widg)
                checkbox.setText(module)
                checkbox.setStyleSheet('color: white;')
                checkbox.setChecked(True)
                self.settings_widg.chckboxes.append(checkbox)
                self.settings_widg.settings_layout.addWidget(checkbox)
            try:
                shutil.rmtree('extract')
            except Exception:
                pass
            self.settings_widg.show()
            self.hide()
        except Exception:
            self.choise_lable.setText('Failed to complete the query.')
        
