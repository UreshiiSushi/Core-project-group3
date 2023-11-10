from collections import UserList


class NoteBook:
    def __init__(self):
        self.notes = []

    def add_note(self, text):
        tags = self.extract_tags(text)
        self.notes.append({"text": text, "tags": tags})
        print("Запись добавлена в блокнот.")

    def extract_tags(self, text):
        # Реализуйте функцию для извлечения тегов из строки
        tags = [word[1:] for word in text.split() if word.startswith("#")]
        return tags

    @staticmethod
    def add_note_from_user():
        notebook = NoteBook()
        input_text = input("Введите текст записи: ")
        notebook.add_note(input_text)

    def change_note(self, note_index, new_text):
        if 0 <= note_index < len(self.notes):
            tags = self.extract_tags(new_text)
            self.notes[note_index] = {"text": new_text, "tags": tags}
            print(f"Запись с индексом {note_index} изменена в блокноте.")
        else:
            print("Указанный индекс записи не существует.")

    def delete_note(self, note_index):
        if 0 <= note_index < len(self.notes):
            del self.notes[note_index]
            print(f"Запись с индексом {note_index} удалена из блокнота.")
        else:
            print("Указанный индекс записи не существует.")

    def find_notes(self, search_text):
        matching_notes = []
        for index, note in enumerate(self.notes):
            if search_text.lower() in note["text"].lower():
                matching_notes.append((index, note))

        if matching_notes:
            print("Найденные записи:")
            for index, note in matching_notes:
                print(f"Индекс: {index}, Текст: {note['text']}, Теги: {note['tags']}")
        else:
            print("Нет записей, соответствующих поисковому запросу.")


# Пример использования
if __name__ == "__main__":
    notebook = NoteBook()

    # Пример добавления записи с тегами
    input_text = "Сегодня я поучаствовал в #программирование. Было интересно!"
    notebook.add_note(input_text)

    # Пример добавления записи через пользовательский ввод
    NoteBook.add_note_from_user()
