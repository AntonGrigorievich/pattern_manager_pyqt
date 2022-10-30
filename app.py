import sys
from database import sqlite3_db
from Qt_handlers import Widgets
from PyQt5.QtWidgets import QApplication

# обьявляем обьект класса database
db = sqlite3_db.DataBase
def on_startup():
    db.sql_start()

# Устанавливаем соединение обьекта db с базой данных
# и запускаем виджет авторизации/регистрации пользователя
if __name__ == '__main__':
    on_startup()
    app = QApplication(sys.argv)
    ex = Widgets.AuthWidget()
    ex.show()
    sys.exit(app.exec_())