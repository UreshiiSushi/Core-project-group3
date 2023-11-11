from datetime import datetime
import pickle
from pathlib import Path
from ab_classes import AddressBook, Record, DateError

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
        except DateError:
            return "Birthday date error or no birthday data"
    return inner


def greeting(*args):
    return greeting_message

#TODO: rebase to address book module
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


# @input_error
# def add_phone(*args):
#     name = args[0].lower()
#     new_phone = args[1]
#     rec = phone_book.get(name)
#     if rec:
#         rec.add_phone(new_phone)
#         return f"{args[0].capitalize()}'s phone added another one {args[1]}"
#     else:
#         raise KeyError()


# @input_error
# def add_record(name: str, phone: str):
#     # global phone_book
#     record = Record(name, phone)
#     phone_book.add_record(record)
#     # if not phone.isdecimal():
#     #     raise ValueError
#     # phone_book[name] = phone
#     return f"{record}"


# @input_error
# def change_record(name: str, phone: str, new_phone: str):
#     # global phone_book
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
#         for k, v in phone_book.items():
#             if search in k:
#                 rec.append(phone_book[k])
#                 # rec = phone_book[k]
#     if rec:
#         result = "\n".join(list(map(str, rec)))
#         return f"Finded \n{result}"
#     else:
#         return f'Nothing was found for your request.'


# def show_all(*args):
#     # for p in phone_book.iterator():
#     #     print(p)
#     #     input(">>>Press Enter for next record")
#     try:
#         if args[0]:
#             for rec in phone_book.iterator(int(args[0])):
#                 print("\n".join([str(r) for r in rec]))
#                 input("Press Enter for next records")
#     except:
#         for rec in phone_book.iterator():
#             print("\n".join([str(r) for r in rec]))


# def save_book() -> str:
#     # global phone_book
#     with open(save_file, "wb") as file:
#         pickle.dump(phone_book, file)
#     return f"Phonebook saved"


# def load_book() -> str:
#     # global phone_book
#     with open(save_file, "rb") as file:
#         loaded_book = pickle.load(file)
#     for k, v in loaded_book.items():
#         phone_book.data[k] = v
#     return f"Phonebook loaded"
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
    # addressbook_main: ("address book", "2"),
    # notes_main: ("notes", "3"),
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


# TODO: Rebase to address book module
# def help(*args):
#     message = '''Use next commands:
#     <add> 'name' 'phone'  - add name and phone number to the dictionary
#     <add_b> 'name' 'birthday' - add birthday date to the name in dictionary
#     <add_phone> 'name' 'phone'  - add phone number to the name in dictionary
#     <change> 'name' 'phone' 'new_phone' - change phone number for this name
#     <days_to_birthday> 'name' - return number days to birhday
#     <birthday> 'num' - return records with birthday date in 'num' days
#     delete 'name' - delete name and phones from the dictionary
#     <find> 'info' - find all records includes 'info' in Name or Phone
#     <hello> - greeting
#     seek 'name' 'phone' - find phone for name in the dictionary
#     phone 'name' - show phone number for this name
#     remove_phone 'name' 'phone' - remove phone for this name
#     <show_all>  -  show all records in the dictionary
#     <show_all> 'N' - show records by N records on page
#     <exit> or <close> or <good_bye> - exit from bot'''
#     return message


# @input_error
# def add_birhday(*args):
#     name = args[0].lower()
#     try:
#         birhday = datetime.strptime(args[1], "%d/%m/%Y")
#     except:
#         raise DateError()
#     rec = phone_book.get(name)
#     if rec:
#         rec.add_birthday(birhday.date())
#         return f"{args[0].capitalize()}'s birthday added {args[1]}"
#     else:
#         raise DateError()


# @input_error
# def days_to_birthday(*args):
#     name = args[0].lower()
#     rec = phone_book.get(name)
#     if rec:
#         days = rec.days_to_birthday()
#         return f"{days} days to {name.capitalize()}'s birthday"
#     else:
#         raise KeyError()


# @input_error
# def birthday_in(*args):
#     num_days = int(args[0])
#     for name in phone_book:
#         rec = phone_book.get(name)
#         try:
#             days = rec.days_to_birthday()
#             if days <= num_days:
#                 print(f"{rec} birthday in {days} days")
#         except DateError:
#             continue
#     return f"Our birthday people in {num_days} days"


# COMMANDS = {greeting: "hello",
#             add_birhday: "add_b",
#             add_record: "add",
#             add_phone: "add_phone",
#             birthday_in: "birthday",
#             change_record: "change",
#             days_to_birthday: "days_to_birthday",
#             find: "find",
#             help: "help",
#             show_all: "show_all",
#             save_book: "save",
#             load_book: "load",
#             stop_command: "good_bye",
#             stop_command: "close",
#             stop_command: "exit"
#             }


def parcer(text: str):
    for func, kw in COMMANDS.items():
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
