import curses
from utils.cryptopass_database import connection
from utils.encryption import user_input
from prettytable import PrettyTable


import os
import sys


if os.name == 'posix':
    if os.geteuid() != 0:
        print("For your data security, you need to run with root privileges.")
        os.execvp("sudo", ["sudo", "python3"] + sys.argv)
elif os.name == 'nt':
    import ctypes

    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("For your data security, you need to run with administrator privileges.")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)
else:
    print("This script requires elevated privileges to run.")
    print("Please run it with administrator privileges.")
    input("Press enter to exit.")

cursor = connection.cursor()


def menu():
    # Initialize curses
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(0)

    stdscr.addstr(0, curses.COLS // 2 - len("CryptoPass Personal Data Manager") //
                  2, "CryptoPass Personal Data Manager")

    stdscr.addstr(2, curses.COLS // 2 - len("Use arrow keys to navigate, Enter to select an option") //
                  2, "Use arrow keys to navigate, Enter to select an option")

    # Define the menu options
    menu_options = ["Documentation", "Add personal data", "Display personal data",
                    "Exit", "Delete a specific row", "Delete personal data"]
    current_option = 0

    while True:
        # Clear the screen and display the menu options
        stdscr.clear()
        stdscr.addstr(0, curses.COLS // 2 - len("CryptoPass Personal Data Manager") //
                      2, "CryptoPass Personal Data Manager")
        stdscr.addstr(2, curses.COLS // 2 - len("Use arrow keys to navigate, Enter to select an option") //
                      2, "Use arrow keys to navigate, Enter to select an option")

        for i, option in enumerate(menu_options):
            x = curses.COLS // 2 - len(option) // 2
            y = curses.LINES // 2 - len(menu_options) // 2 + i

            if i == current_option:
                stdscr.addstr(y, x, option, curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, option)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            current_option = max(0, current_option - 1)
        elif key == curses.KEY_DOWN:
            current_option = min(len(menu_options) - 1, current_option + 1)
        elif key == ord('\n'):

            if current_option == 0:

                stdscr.clear()
                try:
                    with open('docs/documentation.txt', 'r') as file:
                        content = file.read()
                        stdscr.addstr(0, 0, content)
                        stdscr.refresh()

                        max_y, max_x = stdscr.getmaxyx()
                        new_y = content.count('\n') + 1
                        if new_y > max_y:
                            curses.resizeterm(new_y, max_x)

                    stdscr.refresh()
                    stdscr.getch()

                    if new_y > max_y:
                        curses.resizeterm(max_y, max_x)
                        stdscr.refresh()
                except:

                    stdscr.addstr(
                        1, 0, "Error: the terminal size it's too small for documentation ")
                    stdscr.refresh()
                    stdscr.getch()

            elif current_option == 1:
                # Add personal data
                stdscr.clear()
                stdscr.addstr(0, 0, "Enter app name: ")
                curses.echo()
                app_name = stdscr.getstr().decode('utf-8')
                stdscr.addstr(1, 0, "Enter your username: ")
                user_name = stdscr.getstr().decode('utf-8')
                stdscr.addstr(2, 0, "Enter your email: ")
                email = stdscr.getstr().decode('utf-8')
                stdscr.addstr(3, 0, "Enter your password: ")
                password = stdscr.getstr().decode('utf-8')
                curses.noecho()
                new_user = user_input(app_name, user_name, email, password)
                new_user.encrypt()
                cursor.execute("""INSERT INTO personal_data ( app_name, user_name, email, password ) VALUES (?, ?, ?, ?)""",
                               (new_user.app_name, new_user.user_name, new_user.email, new_user.password))
                connection.commit()
            elif current_option == 2:
                # Display personal data
                stdscr.clear()
                cursor.execute("""SELECT * FROM personal_data""")
                personal_data = cursor.fetchall()

                # define table structure
                table = PrettyTable()
                table.field_names = ["App Name",
                                     "Username", "Email", "Password", 'ID']

                # add data to table
                for row in personal_data:
                    new_user = user_input(
                        row[0], row[1], row[2], row[3], row[4])
                    new_user.decrypt()
                    table.add_row([new_user.app_name, new_user.user_name,
                                   new_user.email, new_user.password, new_user.id])
                    table.add_row(['', '', '', '', ''])

                # create table string and split it into rows
                table_string = table.get_string()
                table_rows = table_string.split('\n')

                # print table rows to the screen
                for i, row in enumerate(table_rows):
                    stdscr.addstr(i, 0, row)

                stdscr.addstr(len(table_rows), 0, "Press any key to continue")
                stdscr.getch()
            elif current_option == 3:
                # Exit
                break

            elif current_option == 4:

                stdscr.clear()

                cursor.execute("""SELECT COUNT(*) FROM personal_data""")
                count = cursor.fetchone()[0]

                if count == 0:
                    stdscr.addstr("No records found in the database.\n")
                    stdscr.addstr("Press enter to continue.\n")
                    stdscr.refresh()
                    stdscr.getch()

                else:
                    # Prompt the user to enter an ID until a valid one is entered
                    while True:
                        stdscr.addstr("Enter the id to delete: ")
                        curses.echo()
                        id_to_delete = stdscr.getstr().decode()

                        # Check if the ID exists in the table
                        cursor.execute(
                            "SELECT id FROM personal_data WHERE id = ?", (id_to_delete,))
                        row = cursor.fetchone()
                        if row is None:
                            stdscr.addstr(
                                "Invalid ID. Please enter a valid ID.\n")
                            stdscr.refresh()
                        else:
                            # If the ID exists, delete the row and break out of the loop
                            cursor.execute(
                                "DELETE FROM personal_data WHERE id = ?", (id_to_delete,))
                            connection.commit()
                            stdscr.addstr(" row deleted.\n")
                            stdscr.addstr(
                                "Action completed. Press enter to continue.\n")
                            stdscr.refresh()
                            stdscr.getch()
                            break

            elif current_option == 5:

                cursor.execute("""DROP TABLE personal_data""")
                os.remove('sql/horcrux.db')
                stdscr.addstr(0, 0, "All data was removed forever")
                stdscr.refresh()
                break

    # Clean up curses
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    curses.curs_set(1)


menu()
