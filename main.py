import pickle
from pathlib import Path
from ab_classes import AddressBook, Record

from sort import sort_main
#from ab_classes import addressbook_main
#from note import notes_main



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
    return inner


def greeting(*args):
    return greeting_message

#region rebase to ab_classes.py
# # save_file = Path("phone_book.bin")
# # phone_book = AddressBook()

# @input_error
# def add_record(name: str, phone: str):
#     global phone_book
#     record = Record(name, phone)
#     phone_book.add_record(record)
#     # if not phone.isdecimal():
#     #     raise ValueError
#     # phone_book[name] = phone
#     return f"{record}"


# @input_error
# def change_record(name: str, phone: str, new_phone: str):
#     global phone_book
#     rec: Record = phone_book.find(name)
#     if rec:
#         return rec.edit_phone(phone, new_phone)
#     # if not new_phone.isdecimal():
#     #     raise ValueError
#     # rec = phone_book[name]
#     # if rec:
#     #     phone_book[name] = new_phone
#     # return f"Changed phone {name=} {new_phone=}"


# @input_error
# def find(search: str) -> str or None:
#     # global phone_book
#     rec = []
#     if search.isdigit():
#         for k, v in phone_book.items():
#             if v.find_phone(search):
#                 rec.append(phone_book[k])
#     else:
#         for k,v in phone_book.items():
#             if search in k: 
#                 rec = phone_book[k]
#     if rec:
#         result = "\n".join(list(map(str, rec)))
#         return f"Finded \n{result}"


# def show_all():
#     global phone_book
#     for p in phone_book.iterator():
#         input(">>>Press Enter for next record")
#         print(p)


# def save_book() -> str:
#     global phone_book
#     with open(save_file, "wb") as file:
#         pickle.dump(phone_book, file)
#     return f"Phonebook saved"


# def load_book() -> str:
#     global phone_book
#     with open(save_file, "rb") as file:
#         loaded_book = pickle.load(file)
#     for k, v in loaded_book.items():
#         phone_book.data[k] = v
#     return f"Phonebook loaded"

# # if all([save_file.exists(), save_file.stat().st_size> 0]):
# #     print(load_book())
#endregion

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
    notes_main: ("notes", "3"),
    stop_command: ("stop", "exit")
}
# rebase to ab_classes.py
# COMMANDS = {greeting: "hello",
#             add_record: "add",
#             change_record: "change",
#             find: "find",
#             show_all: "show all",
#             save_book: "save",
#             load_book: "load",
#             stop_command: ("good bye", "close", "exit")
#             }


def parcer(text: str):
    for func, kw in MAIN_MENU.items():
        if text.lower().startswith(kw):
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
