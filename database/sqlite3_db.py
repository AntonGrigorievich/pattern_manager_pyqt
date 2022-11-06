import sqlite3

# создаем класс базы данных для упрощения работы с sql-запросами
class DataBase:
    # метод установки соединения с базой данных
    def sql_start(self):
        global db, curs
        db = sqlite3.connect('database.db')
        curs = db.cursor()
        if db:
            print('Database connected succesefully!')
        db.execute("""CREATE TABLE IF NOT EXISTS users (user_id INTEGER, user_login TEXT, user_passcode TEXT)""")
        db.execute("""CREATE TABLE IF NOT EXISTS patterns (pattern_name TEXT, folder_directory TEXT, orig_directory TEXT)""")
        db.commit()

    # метод очистки таблицы бд
    def sql_drop_table(self, table_name):
        curs.execute(f"""DROP TABLE {table_name}""")
        db.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (pattern_name TEXT, folder_directory TEXT, orig_directory TEXT)""")
        db.commit()

    # метод добавления пользователя в таблицу users
    def sql_add_user(self, login, id, passcode):
        curs.execute(f"""INSERT INTO users(user_id, user_login, user_passcode) VALUES (?, ?, ?)""", (id, login, passcode))
        db.commit()

    # метод получения данных о всех пользователях таблицы users
    def sql_get_users(self):
        curs.execute("""SELECT * FROM users""")
        return curs.fetchall()

    # метод получения логина пользователя
    def sql_get_users_logins(self):
        curs.execute("""SELECT user_login FROM users""")
        return [i[0] for i in curs.fetchall()]

    # метод получения пароля пользователя
    def sql_get_user_passcode(self, login):
        curs.execute(f"""SELECT user_passcode FROM users WHERE user_login = '{login}'""")
        return curs.fetchone()[0]

    # метод удаления пользователя из таблицы
    def sql_remove_user(self, user_login):
        curs.execute(f"""DELETE FROM users WHERE user_loggin = '{user_login}'""")
        db.commit()
    
    # метод добавления нового шаблона в таблицу patterns
    def sql_add_pattern(self, pattern_name, folder_name, orig_directory):
        curs.execute(f"""INSERT INTO patterns VALUES ('{pattern_name}', '{folder_name}', '{orig_directory}')""")
        db.commit()

    # метод получения имен всех шаблонов
    def sql_get_pattern_names(self):
        curs.execute("""SELECT pattern_name FROM patterns""")
        return [i[0] for i in curs.fetchall()]

    # метод получения директорий всех шаблонов
    def sql_get_pattern_directorys(self):
        curs.execute("""SELECT orig_directory FROM patterns""")
        return [i[0] for i in curs.fetchall()]

    def sql_get_pattern_local_directorys(self):
        curs.execute("""SELECT folder_directory FROM patterns""")
        return [i[0] for i in curs.fetchall()]

    # метод удаления шаблона из таблицы
    def sql_remove_pattern(self, pattern_name):
        curs.execute(f"""DELETE FROM patterns WHERE pattern_name = '{pattern_name}'""")
        db.commit()

    # метод для выполнения пользовательского запроса
    def sql_complte_user_query(self, query):
        curs.execute(query)
        db.commit()