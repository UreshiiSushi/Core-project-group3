from collections import UserList


class Notes:
    def __init__(self, title, description, tag):
        self.title = title
        self.description = description
        self.tag = tag

class Notebook:
    def __init__(self):
        self.notes = []

    def add_note(self, title, description, tag):
        ... #add code here

    def search_notes(self, keyword):
        ... #add code here

    def edit_note(self, note_index, new_title, new_description, new_tag):
        ... #add code here

    def delete_note(self, note_index):
        ... #add code here

    def sort_notes_by_tag(self):
        ... #add code here

def get_user_input(prompt):
    return input(prompt)

notebook = Notebook()

while True:
    print("Menu:")
    print("1. Add Note")
    print("2. Search note")
    print("3. Edit note")
    print("4. Delete Note")
    print("5. Sort Notes by tag")
    print("6. Exit")

    choice = get_user_input("Please choose: ")

    if choice == "1":
        title = get_user_input("Please enter title name: ")
        description = get_user_input("Please enter description: ")
        tag = get_user_input("Please enter tag: ")
        notebook.add_note(title, description, tag)
        print("Note has been added successfully!")

    elif choice == "2":
        keyword = get_user_input("Enter key word for search: ")
        found_notes = notebook.search_notes(keyword)
        if found_notes:
            print("Search results:")
            for note in found_notes:
                print(f"Title: {note.title}")
                print(f"Description: {note.description}")
                print(f"Tag: {note.tag}")
                print("==========")
        else:
            print("Note is not found.")

    elif choice == "3":
        note_index = int(get_user_input("Please enter note number you want to edit: "))
        new_title = get_user_input("Enter a new title: ")
        new_description = get_user_input("Enter a new description: ")
        new_tag = get_user_input("Enter a new tag: ")
        notebook.edit_note(note_index, new_title, new_description, new_tag)
        print("Note has been edited successfully!")

    elif choice == "4":
        note_index = int(get_user_input("Please enter note number you want to be removed: "))
        notebook.delete_note(note_index)
        print("Note has been removed successfully")
    elif choice == "5":
        sorted_notes = notebook.sort_notes_by_tag()
        if sorted_notes:
            print("Sorted notes:")
            for note in sorted_notes:
                print(f"Title: {note.title}")
                print(f"Description: {note.description}")
                print(f"Tag: {note.tag}")
                print("==========")
        else:
            print("No notes found.")

    elif choice == "6":
        break

    else:
        print("Wrong choise. Please try again.")
