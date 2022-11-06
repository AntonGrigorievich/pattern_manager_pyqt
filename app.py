import sys
from database import sqlite3_db
from Qt_handlers.Widgets.AuthWidgetFile import *
from PyQt5.QtWidgets import QApplication

# обьявляем обьект класса database
db = sqlite3_db.DataBase
def on_startup():
    db.sql_start(db)

# Устанавливаем соединение обьекта db с базой данных
# и запускаем виджет авторизации/регистрации пользователя
if __name__ == '__main__':
    on_startup()
    app = QApplication(sys.argv)
    ex = AuthWidget()
    ex.show()
    sys.exit(app.exec_())
