from datetime import datetime
import pickle
from pathlib import Path
from address_book import AddressBook, Record, DateError

from sort import sort_main
from address_book import addressbook_main
from note import note_main



greeting_message = """Welcome to Exponenta app. 
Here you can:
1. sort your folder with random files, 
2. make your own address book,
3. write some notes
Type 'menu' for choose or 'exit' to finish"""


menu_message = """Choose command:
1. Sort folder
2. Address Book
3. My notes
Enter number for choose or 'exit' to finish work
"""

def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except TypeError:
            return "Not enough params. Try again"
        except KeyError:
            return "Unknown name. Try again"
        except ValueError:
            return "Wrong phone number. Try again"
        except DateError:
            return "Birthday date error or no birthday data"
    return inner


def greeting(*args):
    return greeting_message


def stop_command(*args) -> str:
    return f"Good bye!"


def menu():
    return menu_message


def unknown(*args):
    return "Unknown command. Try again."

  
MAIN_MENU = {
    greeting: ("hello", "start"),
    menu: "menu",
    sort_main: ("sort", "1"),
    addressbook_main: ("address book", "2"),
    note_main: ("notes", "3"),
    stop_command: ("stop", "exit")
}


def parcer(text: str):
    for func, kw in MAIN_MENU.items():
        command = text.rstrip().split()
        if text.lower().startswith(kw) and kw == command[0].lower():
            return func, text[len(kw):].strip().split()
    return unknown, []


def main():

    while True:
        user_input = input(">>>")
        func, data = parcer(user_input)
        result = func(*data)
        print(result)
        if result == "Good bye!":
            break


if __name__ == "__main__":
    main()
