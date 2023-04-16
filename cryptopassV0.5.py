from utils.cryptopass_database import connection
from utils.encryption import user_input
from prettytable import PrettyTable
import os

cursor = connection.cursor()


def menu():

    while True:
        print("1. Documentation")
        print("2. Add personal data")
        print("3. Display personal data")
        print("4. Exit")
        print("5. Delete a specific row")
        print("6. Delete all data")

        x = input("Enter option: ")

        if x == '1':
            with open('docs/documentation.txt', 'r') as file:
                content = file.read()
            print(content)

        elif x == '2':
            app_name = input('Enter app name: ')
            user_name = input('Enter your username: ')
            email = input('Enter your email: ')
            password = input('Enter your password: ')
            new_user = user_input(app_name, user_name, email, password)
            # Criptarea datelor utilizatorului
            new_user.encrypt()
            cursor.execute("""INSERT INTO personal_data(app_name, user_name, email, password, id) VALUES (?, ?, ?, ?, ?)""",
                           (new_user.app_name, new_user.user_name, new_user.email, new_user.password, new_user.id))
            connection.commit()

        elif x == '3':

            cursor.execute("""SELECT * FROM personal_data""")
            personal_data = cursor.fetchall()

            # define table structure
            table = PrettyTable()
            table.field_names = ["App Name",
                                 "Username", "Email", "Password", "ID"]

            # add data to table
            for row in personal_data:
                new_user = user_input(row[0], row[1], row[2], row[3], row[4])
                new_user.decrypt()
                table.add_row([new_user.app_name, new_user.user_name,
                              new_user.email, new_user.password, new_user.id])
                table.add_row(['', '', '', '', ''])

            print(table)
        elif x == '4':
            break

        elif x == '5':
            id_to_delete = input('Enter the id to delete: ')

            cursor.execute("""DELETE FROM personal_data WHERE id = ?""",
                           (id_to_delete,))
            connection.commit()

            print(cursor.rowcount, " row deleted.")

        elif x == '6':
            cursor.execute("""DROP TABLE personal_data""")
            os.remove('sql/horcrux.db')
            print('All data was removed forever')
            break
        else:
            print("Invalid option")


menu()
