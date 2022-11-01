import shutil
import zipfile
import os
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog, QInputDialog
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from app import db


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
        self.pattern_table.setModel(self.model)
        self.pattern_table.setColumnWidth(0, 176)
        self.pattern_table.setColumnWidth(1, 177)
        self.create_button.clicked.connect(self.create_pattern)
        self.table_update_button.clicked.connect(self.update_table)
    
    def create_pattern(self):
        pattern_name, ok_pressed  =  QInputDialog.getText(self, "Insert pattern name", 
                                                "What will the pattern name be?")
        if pattern_name not in db.sql_get_pattern_names() and pattern_name.strip() != '':
            if ok_pressed:
                fname = QFileDialog.getOpenFileName(self, 'Выбратьz zip папку', '', '(*.zip)')[0]
                if fname not in db.sql_get_pattern_directorys() and fname.strip() != '':
                    file_zip = zipfile.ZipFile(f'patterns\\{pattern_name}.zip', 'w')

                    shutil.copy(fname, f'patterns\\{pattern_name}.zip')
                    file_zip.close()
                    db.sql_add_pattern(pattern_name, fname)
                    self.model.setTable('patterns')
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
        self.model.setTable('patterns')
        self.model.select()
        self.pattern_table.setModel(self.model)
        self.pattern_table.setColumnWidth(0, 176)
        self.pattern_table.setColumnWidth(1, 177)
        self.notify_lable.setText('Table updated')        



class AuthWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Qt_handlers\\ui_files\\auth_widget.ui', self)
        self.initUI()

        self.signin_button.clicked.connect(self.auth)
        self.signup_button.clicked.connect(self.register)
        self.login = self.login_lineedit
        self.passcode = self.passcode_lineedit
        self.mainwin = MainWindow()

    def check_info(self):
        if self.login.text() == '':
            return False
        if self.passcode.text() == '':
            return False
        return True

    def register(self):
        if self.check_info():
            login = self.login.text()
            passcode = self.passcode.text()
            id = len(db.sql_get_users()) + 1
            if login not in db.sql_get_users_logins():
                db.sql_add_user(login, id, passcode)
                self.start_lable.setText('Successfully registered!')
                self.mainwin.show()
                self.hide()
            else:
                self.start_lable.setText('login is busy, please use another')

    def auth(self):
        if self.check_info():
            login = self.login.text()
            passcode = self.passcode.text()
            if login in db.sql_get_users_logins() and passcode == db.sql_get_user_passcode(login):
                self.start_lable.setText('Successfully authorised!')
                self.mainwin.show()
                self.hide()
            else:
                self.start_lable.setText('Wrong data, please try again')


    def initUI(self):
        pass
