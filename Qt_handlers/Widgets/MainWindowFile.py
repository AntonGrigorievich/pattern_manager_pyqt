import shutil
import zipfile
import os
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog, QInputDialog, \
    QMessageBox, QRadioButton
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from app import db
from Qt_handlers.Widgets.TableEditFile import TableEdit
from Qt_handlers.Widgets.ChoiceWidgetFile import ChoiceWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Qt_handlers\\ui_files\\pattern_manager.ui', self)  # Загружаем дизайн
        self.initUI()

    def initUI(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        # Укажем имя базы данных
        db.setDatabaseName('database.db')
        # И откроем подключение
        db.open()
        self.model = QSqlTableModel(self, db)
        self.model.setTable('patterns')
        self.model.select()
        self.edit_widg = TableEdit()
        self.pattern_table.setModel(self.model)
        self.pattern_table.setColumnWidth(0, 176)
        self.pattern_table.setColumnWidth(1, 177)
        self.create_button.clicked.connect(self.create_pattern)
        self.table_update_button.clicked.connect(self.update_table)
        self.edit_table_button.clicked.connect(self.show_table_edit)
        self.create_folder_button.clicked.connect(self.open_choice_widget)

    def create_pattern(self):
        pattern_name, ok_pressed  =  QInputDialog.getText(self, "Insert pattern name", 
                                                "What will the pattern name be?")
        if pattern_name not in db.sql_get_pattern_names(db) and pattern_name.strip() != '':
            if ok_pressed:
                fname = QFileDialog.getOpenFileName(self, 'Выбратьz zip папку', '', '(*.zip)')[0]
                # добавить проверку на ориг директорию
                if fname not in db.sql_get_pattern_directorys(db) and fname.strip() != '':
                    file_zip = zipfile.ZipFile(f'patterns\\{pattern_name}.zip', 'w')

                    shutil.copy(fname, f'patterns\\{pattern_name}.zip')
                    file_zip.close()
                    db.sql_add_pattern(db, pattern_name, f'patterns/{pattern_name}.zip', fname)
                    self.model.select()
                    self.pattern_table.setModel(self.model)
                    self.pattern_table.setColumnWidth(0, 176)
                    self.pattern_table.setColumnWidth(1, 177)
                    self.notify_lable.setText("""Pattern successfully made!""")
                else:
                    self.notify_lable.setText('Pattern by this directory aleady exists')

        elif pattern_name:
            self.notify_lable.setText('This name is invalid or already taken. Please choose another')

    def update_table(self):
        self.model.select()
        self.pattern_table.setModel(self.model)
        self.pattern_table.setColumnWidth(0, 176)
        self.pattern_table.setColumnWidth(1, 177)
        self.notify_lable.setText('Table updated') 

    def show_table_edit(self):
        self.edit_widg.update_table()  
        self.edit_widg.show()

    def open_choice_widget(self):
        self.choice_widg = ChoiceWidget()
        for pattern_name in db.sql_get_pattern_names(db):
            self.choice_widg.button = QRadioButton(self)
            self.choice_widg.button.toggled.connect(self.choice_widg.choose_pattern)
            self.choice_widg.button.text = pattern_name
            self.choice_widg.button.setText(pattern_name)
            self.choice_widg.button.setStyleSheet('color: white;')
            self.choice_widg.choicewidget_layout.addWidget(self.choice_widg.button)
        self.choice_widg.show()