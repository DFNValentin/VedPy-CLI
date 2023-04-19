import sqlite3
import os

dir_sql = 'sql'
dir_location_sql = './' + dir_sql


if not os.path.exists(dir_location_sql):
    os.mkdir(dir_location_sql)
else:
    pass


<<<<<<< HEAD

=======
>>>>>>> master
connection = sqlite3.connect('sql/horcrux.db')

cursor = connection.cursor()


def create_table():

    try:

        cursor.execute("""CREATE TABLE personal_data (
            app_name text,
            user_name text, 
            email text, 
            password text, 
            id INTEGER PRIMARY KEY AUTOINCREMENT)""")

    except sqlite3.OperationalError:
        pass

    connection.commit()


create_table()
