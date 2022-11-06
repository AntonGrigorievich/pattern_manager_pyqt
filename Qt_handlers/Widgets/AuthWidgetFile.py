import shutil
import zipfile
import os
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog, QInputDialog, \
    QMessageBox, QRadioButton
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from app import db
from Qt_handlers.Widgets.MainWindowFile import MainWindow

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
            id = len(db.sql_get_users(db)) + 1
            if login not in db.sql_get_users_logins(db):
                db.sql_add_user(db, login, id, passcode)
                self.start_lable.setText('Successfully registered!')
                self.mainwin.show()
                self.hide()
            else:
                self.start_lable.setText('login is busy, please use another')

    def auth(self):
        if self.check_info():
            login = self.login.text()
            passcode = self.passcode.text()
            if login in db.sql_get_users_logins(db) and passcode == db.sql_get_user_passcode(db, login):
                self.start_lable.setText('Successfully authorised!')
                self.mainwin.show()
                self.hide()
            else:
                self.start_lable.setText('Wrong data, please try again')


    def initUI(self):
        pass