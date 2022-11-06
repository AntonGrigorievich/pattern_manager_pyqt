import shutil
import zipfile
import os
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog, QInputDialog, \
    QMessageBox, QRadioButton
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from app import db

class TableEdit(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(r'Qt_handlers\ui_files\table_edit.ui', self)
        self.initUI()
    
    def initUI(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('database.db')
        self.db.open()
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('patterns')
        self.model.select()
        self.pattern_table.setModel(self.model)
        self.pattern_table.setColumnWidth(0, 265)
        self.pattern_table.setColumnWidth(1, 265)
        self.delete_button.clicked.connect(self.delete_item)
        self.drop_button.clicked.connect(self.drop_table)
        self.update_button.clicked.connect(self.update_table)

    def delete_item(self):
        pattern = self.query_lineedit.text()
        msgbox = QMessageBox()
        msgbox.setStyleSheet("color: white;")
        valid = msgbox.question(
            self, '', f"Are you sure you want to delete this item: {pattern}",
            QMessageBox.Yes, QMessageBox.No)
        # Если пользователь ответил утвердительно, выполняем запрос. 
        # Не забываем зафиксировать изменения
        if valid == QMessageBox.Yes:
            try:
                os.remove(f'patterns/{pattern}.zip')
                db.sql_remove_pattern(db, pattern)
                self.model.setTable('patterns')
                self.model.select()
                self.pattern_table.setModel(self.model)
                self.pattern_table.setColumnWidth(0, 265)
                self.pattern_table.setColumnWidth(1, 265)
            except Exception:
                self.table_edit_lable.setText('Failed to complete the query')
            

    def drop_table(self):
        msgbox = QMessageBox()
        msgbox.setStyleSheet("color: white;")
        valid = msgbox.question(
            self, '', f"Are you sure you want to drop whole table?",
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            for direct in db.sql_get_pattern_local_directorys(db):
                os.remove(direct)
            db.sql_drop_table(db, 'patterns')
            self.model.setTable('patterns')
            self.model.select()
            self.pattern_table.setModel(self.model)
            self.pattern_table.setColumnWidth(0, 265)
            self.pattern_table.setColumnWidth(1, 265)

    def update_table(self):
        self.model.select()
        self.pattern_table.setModel(self.model)
        self.pattern_table.setColumnWidth(0, 265)
        self.pattern_table.setColumnWidth(1, 265)
        self.table_edit_lable.setText('Table updated') 