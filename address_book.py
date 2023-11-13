# from _collections_abc import Iterator
from collections import UserDict
from datetime import date, datetime
from itertools import islice
from pathlib import Path
import pickle
import re

# from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit import prompt

save_file = Path("phone_book.bin")

help_message = """Use next commands:
    <add> 'name' 'phone'  - add name and phone number to the dictionary
    <add_birthday> 'name' 'birthday' - add birthday date to the name in dictionary
    <add_phone> 'name' 'phone'  - add phone number to the name in dictionary
    <add_adr> 'name' 'adress' - add adress to the name in dictionary
    <change> 'name' 'phone' 'new_phone' - change phone number for this name
    <days_to_birthday> 'name' - return number days to birhday
    <birthday> 'num' - return records with birthday date in 'num' days
    <delete> 'name' - delete name and phones from the dictionary
    <find> 'info' - find all records includes 'info' in Name or Phone
    <search> 'str': min 3 symbols - find all records includes 'str' in Name or Phone or Adress
    <hello> - greeting
    <email> 'name' [email@domain.com] - add OR change email for specified Name
    <phone> 'name' - show phone number for this name
    <adress> 'name' - show adres for this name
    <remove_phone> 'name' 'phone' - remove phone for this name
    <remove_adr> 'name' - remove adress for this name 
    <show_all>  -  show all records in the dictionary
    <show_all> 'N' - show records by N records on page
    <exit> or <close> or <good_bye> - exit from module"""

greeting_message = """Welcome to Address Book.
Type command or 'help' for more information."""


class DateError(Exception):
    ...


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    ...


class Adress(Field):
    ...


class Email(Field):
    def __init__(self, email: str):
        self.__email = None
        self.email = email

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        if re.match(r"[a-zA-Z][a-zA-Z0-9-_.]+\@[a-zA-Z]+\.[a-zA-Z][a-zA-Z]+", email):
            self.__email = email
        else:
            raise ValueError(
                "Wrong email format. Use pattern <name@domain.com> for email"
            )

    def __str__(self):
        return f"{self.__email}"


class Birthday(Field):
    def __init__(self, birthday) -> None:
        self.__birthday = None
        self.birthday = birthday

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday):
        if isinstance(birthday, datetime):
            self.birthday = birthday
        else:
            raise DateError()

    def __str__(self):
        return f"Days to birthday: {self.days_to_birthday}"


class Phone(Field):
    def __init__(self, phone: str):
        self.__phone = None
        self.phone = phone

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone: str):
        if re.match(r"[0-9]{10}", phone):
            self.__phone = phone
        else:
            raise ValueError("Wrong phone format. It must contains 10 digits")


class Record:
    def __init__(
        self, name, phone: str = None, birthday_date: str = None, email: str = None, adress: str = None
    ):
        self.name = Name(name)
        self.phones: list(Phone) = []
        self.birthday = None
        self.email = None
        self.adress = None
        if phone:
            self.phones.append(Phone(phone))
        if birthday_date:
            self.birthday = birthday_date  # Birthday(birthday_date)
        if email:
            self.email = Email(email)

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))
        return f"Added phone {phone} to contact {self.name}"

    # methods for working with the User address
    def add_adress(self, adress: str):
        self.adress = Adress(adress)

    def show_adress(self):
        if self.adress:
            return f"{self.name}'s adress: {self.adress}"
        else:
            return f"{self.name}'s adress is empty"

    def del_adress(self):
        self.adress = None
    # End adress block

    def add_birthday(self, bd_date):
        self.birthday = bd_date

    def find_phone(self, phone: str):
        result = None
        for p in self.phones:
            if phone in p.phone:
                result = p
        return result

    def remove_phone(self, phone: str):
        search = self.find_phone(phone)
        if search in self.phones:
            self.phones.remove(search)
            return f"Removed phone {phone} from contact {self.name}."
        else:
            raise ValueError

    def edit_phone(self, phone: str, new_phone: str) -> str:
        edit_check = False
        for i in range(len(self.phones)):
            if self.phones[i].value == phone:
                edit_check = True
                self.phones[i] = Phone(new_phone)
                return f"Changed phone {phone} for contact {self.name} to {new_phone}"
        if not edit_check:
            raise ValueError

    def days_to_birthday(self) -> int:
        if self.birthday:
            now_date = date.today()
            future_bd = self.birthday
            future_bd = future_bd.replace(year=now_date.year)
            if future_bd > now_date:
                return (future_bd - now_date).days
            else:
                future_bd = future_bd.replace(year=future_bd.year + 1)
                return (future_bd - now_date).days
        else:
            raise DateError()

    def add_change_email(self, email: str = None) -> str:
        if email:
            self.email = Email(email)
            return (
                f"Email for contact {self.name} was succefully changed to {self.email}"
            )
        if not email:
            return f"{self.name.value} has an email {self.email}"

    def __str__(self):
        phones = "; ".join(p.phone for p in self.phones)
        return "Contact name: {}, birthday: {}, phones: {}, email: {}, adress: {}".format(
            self.name, self.birthday, phones, self.email, self.adress
        )


class AddressBook(UserDict):
    def __init__(self, data=None):
        super().__init__(data)
        self.counter = 0

    def add_record(self, rec: Record):
        if rec.name.value not in self.data.keys():
            self.data[rec.name.value] = rec
        else:
            raise ValueError

    def find(self, name: str):
        for k in self.data.keys():
            if name in k:
                return self.data.get(name)
        else:
            return None

    def search(self, search_str: str):
        keys = []
        if search_str.isdigit():
            print('Search Phone and Name and Adress')
            for key, record in self.items():
                if str(record.name).find(search_str) >= 0 or record.find_phone(search_str.lower()) != None or str(record.adress).lower().find(search_str.lower()) >= 0:
                    keys.append(key)
            return keys

        else:
            print('Search Name and Adress')
            for key, record in self.items():
                if str(record.name).lower().find(search_str.lower()) >= 0 or str(record.adress).lower().find(search_str.lower()) >= 0:
                    keys.append(key)
            return keys

    def delete(self, name: str):
        if name in self.data.keys():
            return self.data.pop(name)

    # def iterator(self, quantity: int = 1):
    #     values = list(map(str, islice(self.data.values(), None)))
    #     while self.counter < len(values):
    #         yield values[self.counter:self.counter+quantity]
    #         self.counter += quantity

    def iterator(self, quantity=None):
        self.counter = 0
        values = list(map(str, islice(self.data.values(), None)))
        while self.counter < len(values):
            if quantity:
                yield values[self.counter: self.counter + quantity]
                self.counter += quantity
            else:
                yield values
                break

    def save_book(self) -> str:
        with open(save_file, "wb") as file:
            pickle.dump(self.data, file)
        return f"Phonebook saved. Good bye!"

    def load_book(self) -> str:
        with open(save_file, "rb") as file:
            data = file.read()
            self.data = pickle.loads(data)
        return f"Phonebook loaded"
        # with open(save_file, "rb") as file:
        #     loaded_book = pickle.load(file)
        # for k, v in loaded_book.items():
        #     self.data[k] = v
        # return f"Phonebook loaded"


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except TypeError:
            return "Not enough params. Try again"
        except KeyError:
            return "Unknown name. Try again"
        except ValueError:
            return "Wrong format. Try again"  # Було Wrong phone number.
        except DateError:
            return "Birthday date error or no birthday data"
        except IndexError:
            return "Not enough params. Try again"

    return inner


def greeting():
    return greeting_message


def help():
    return help_message


@input_error
def add_birhday(*args):
    name = args[0].lower()
    try:
        birhday = datetime.strptime(args[1], "%d/%m/%Y")
    except:
        raise DateError()
    rec = phone_book.get(name)
    if rec:
        rec.add_birthday(birhday.date())
        return f"{args[0].capitalize()}'s birthday added {args[1]}"
    else:
        raise KeyError()


@input_error
def days_to_birthday(*args):
    name = args[0].lower()
    rec = phone_book.get(name)
    if rec:
        days = rec.days_to_birthday()
        return f"{days} days to {name.capitalize()}'s birthday"
    else:
        raise KeyError()


@input_error
def birthday_in(*args):
    num_days = int(args[0])
    for name in phone_book:
        rec = phone_book.get(name)
        try:
            days = rec.days_to_birthday()
            if days <= num_days:
                print(f"{rec} birthday in {days} days")
        except DateError:
            continue
    return f"Our birthday people in {num_days} days"


# save_file = Path("phone_book.bin")
phone_book = AddressBook()


@input_error
def add_record(name: str, phone: str):
    global phone_book
    record = Record(name, phone)
    phone_book.add_record(record)
    # if not phone.isdecimal():
    #     raise ValueError
    # phone_book[name] = phone
    return f"{record}"


@input_error
def change_record(name: str, phone: str, new_phone: str):
    global phone_book
    rec: Record = phone_book.find(name)
    if rec:
        return rec.edit_phone(phone, new_phone)
    # if not new_phone.isdecimal():
    #     raise ValueError
    # rec = phone_book[name]
    # if rec:
    #     phone_book[name] = new_phone
    # return f"Changed phone {name=} {new_phone=}"


@input_error
def add_change_email(name: str, email: str = None):
    global phone_book
    rec: Record = phone_book.find(name)
    if rec:
        return rec.add_change_email(email)
    return f"Contact {name} wasn`t found"


@input_error
def find(search: str) -> str or None:
    # global phone_book
    rec = []
    if search.isdigit():
        for k, v in phone_book.items():
            if v.find_phone(search):
                rec.append(phone_book[k])
    else:
        for k, v in phone_book.items():
            if search in k:
                rec = phone_book[k]
    if rec:
        result = "\n".join(list(map(str, rec)))
        return f"Finded \n{result}"


def show_all():
    global phone_book
    for p in phone_book.iterator():
        input(">>>Press Enter for next record")
        print(p)


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


# if all([save_file.exists(), save_file.stat().st_size> 0]):
#     print(load_book())


@input_error
def add_phone(*args):
    name = args[0].lower()
    new_phone = args[1]
    rec = phone_book.get(name)
    if rec:
        rec.add_phone(new_phone)
        return f"{args[0].capitalize()}'s phone added another one {args[1]}"
    else:
        raise KeyError()


@input_error
def add_record(name: str, phone: str):
    # global phone_book
    record = Record(name, phone)
    phone_book.add_record(record)
    # if not phone.isdecimal():
    #     raise ValueError
    # phone_book[name] = phone
    return f"{record}"


@input_error
def change_record(name: str, phone: str, new_phone: str):
    # global phone_book
    rec: Record = phone_book.find(name)
    if rec:
        return rec.edit_phone(phone, new_phone)
    # if not new_phone.isdecimal():
    #     raise ValueError
    # rec = phone_book[name]
    # if rec:
    #     phone_book[name] = new_phone
    # return f"Changed phone {name=} {new_phone=}"


@input_error
def find(search: str) -> str or None:
    # global phone_book
    rec = []
    if search.isdigit():
        for k, v in phone_book.items():
            if v.find_phone(search):
                rec.append(phone_book[k])
    else:
        for k, v in phone_book.items():
            if search in k:
                rec.append(phone_book[k])
                # rec = phone_book[k]
    if rec:
        result = "\n".join(list(map(str, rec)))
        return f"Finded \n{result}"
    else:
        return f"Nothing was found for your request."


def show_all(*args):
    try:
        if args[0]:
            for rec in phone_book.iterator(int(args[0])):
                print("\n".join([str(r) for r in rec]))
                input("Press Enter for next records")
    except:
        for rec in phone_book.iterator():
            print("\n".join([str(r) for r in rec]))


def save_book() -> str:
    return phone_book.save_book()


#     # global phone_book
# with open(save_file, "wb") as file:
#     pickle.dump(phone_book, file)
# return f"Phonebook saved"


def load_book() -> str:
    return phone_book.load_book()


#     # global phone_book
#     with open(save_file, "rb") as file:
#         loaded_book = pickle.load(file)
#     for k, v in loaded_book.items():
#         phone_book.data[k] = v
#     return f"Phonebook loaded"


@input_error
def add_adress(name, *args):
    # add addresses for an existing user
    adress: str = ' '.join(args)
    rec: Record = phone_book.get(name)
    if rec:
        rec.add_adress(adress)
        return f"{rec.name}'s added adress {adress}"
    else:
        raise KeyError()


def show_adress(*args):
    # show the address for an existing user
    name = args[0]
    rec: Record = phone_book.get(name)
    if rec:
        return rec.show_adress()
    else:
        raise KeyError()


def remove_adr(*args):
    # delete the address for the existing user
    name = args[0]
    rec: Record = phone_book.get(name)
    if rec:
        rec.del_adress()
        return f"{rec.name}'s del adress"
    else:
        raise KeyError()


@input_error
def search(str_search):
    if len(str_search) < 3:
        return f'minimum number of characters to search is 3'
    else:
        result = ''
        for key in phone_book.search(str_search):
            result += f'{str(phone_book[key])}\n'
        print(result)
        return f'Search {str_search}'


def stop_command(*_):
    return phone_book.save_book()


def unknown(*args):
    return "Unknown command. Try again."


COMMANDS = {
    greeting: "hello",
    add_birhday: "add_birthday",
    add_record: "add",
    add_phone: "add_phone",
    add_adress: "add_adress",
    show_adress: "adress",
    birthday_in: "birthday",
    change_record: "change",
    days_to_birthday: "days_to_birthday",
    find: "find",
    search: "search",
    help: "help",
    show_all: "show_all",
    save_book: "save",
    load_book: "load",
    remove_adr: "del_adress",
    stop_command: ("good_bye", "close", "exit", "stop"),
    add_change_email: "email",
}


def parcer(text: str):
    for func, kw in COMMANDS.items():
        command = text.rstrip().split()
        # ol.pripa було kw == command[0].lower() тоді не спрацьовувала умова для  ("good_bye", "close", "exit", "stop"), змінив на
        if text.lower().startswith(kw) and command[0].lower() in kw:
            return func, text[len(kw):].strip().split()
    return unknown, []


def addressbook_main():
    try:
        if all([save_file.exists(), save_file.stat().st_size > 0]):
            print(phone_book.load_book())
    except:
        ...
    while True:
        # menu_completer = WordCompleter(
        #     ['add', 'add_birthday', 'add_phone', 'birthday', 'change', 'days_to_birthday',
        #      'email', 'find', 'hello', 'help', 'show_all',
        #      'exit', 'close', 'good_bye'], ignore_case=True, WORD=True)  # , match_middle=True)

        menu_completer = NestedCompleter.from_nested_dict({
            'add': {'name phone': None},
            'add_phone': {'380'},
            'add_birthday': {'dd/mm/YYYY'},
            'birthday': {'num_days': None},
            'add_adress': {'name adress'},
            'adress': {'name': None},
            'change': {'name phone new_phone': None},
            'days_to_birthday': {'name': None},
            'email': {'name email@': None},
            'find': {'anything': None},
            'search': {'anything min 3 symbol': None},
            'hello': None,
            'help': None,
            'show_all': {'20'},
            'exit': None,
            'close': None,
            'good_buy': None
        })

        user_input = prompt("Enter user name and phone number or 'help' for help: ",
                            completer=menu_completer)
        # print('You said: %s' % user_input)

        func, data = parcer(user_input)
        result = func(*data)
        print(result)
        if result == "Phonebook saved. Good bye!":
            break


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()
    addressbook_main()

    # # Створення запису для John
    # john_record = Record("John")
    # john_record.add_phone("1234567890")
    # john_record.add_phone("5555555555")

    # # Додавання запису John до адресної книги
    # book.add_record(john_record)

    # # Створення та додавання нового запису для Jane
    # jane_record = Record("Jane")
    # jane_record.add_phone("9876543210")
    # book.add_record(jane_record)
    # bill_record = Record("Bill", "7234592343")
    # dow_record = Record("Dow")
    # book.add_record(bill_record)
    # book.add_record(dow_record)
    # # Виведення всіх записів у книзі
    # for name, record in book.data.items():
    #     print(record)

    # for b in book.iterator(4):
    #     print(b)

    # # Знаходження та редагування телефону для John
    # john = book.find("John")
    # print(john)
    # john.edit_phone("1234567890", "1112223333")

    # print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # # Пошук конкретного телефону у записі John
    # found_phone = john.find_phone("5555555555")
    # print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # # Додавання днів народження і вивід днів до нього
    # john.add_birthday("1993-12-01")
    # print(john.days_to_birthday())
    # jane_record.add_birthday("2004-09-11")
    # print(jane_record.days_to_birthday())
    # print(dow_record.days_to_birthday())

    # # Видалення запису Jane
    # book.delete("Jane")

    # # Тест емейлу
    # letter_to = Email("asdf@domain.com")
    # print(letter_to)
    # print(john_record.add_change_email("hjdshj@jsdhjk.com"))
    # print(john_record.add_change_email("a111@jsdhjk.com"))
    # print(john_record.add_change_email())
    # print(john_record.add_change_email("орлоо@jsdhjk.com"))
