from prompt_toolkit.shortcuts import radiolist_dialog

from address_book import addressbook_main
from note import note_main
from sort import sort_main


def main():
    result = 0
    while result is not None:
        result = radiolist_dialog(
            title="Welcome to Exponenta app.",
            text='''Here you can:
        1. sort your folder with random files, 
        2. make your own address book,
        3. write some notes
        What would you like to do ? ''',
            values=[
                ("sort", "Sort directory"),
                ("addressbook", "Address book"),
                ("notebook", "Notebook"),
            ]
        ).run()
        print(result)
        if result == "addressbook":
            addressbook_main()
        elif result == "notebook":
            note_main()
        elif result == "sort":
            sort_main()


if __name__ == "__main__":
    main()
