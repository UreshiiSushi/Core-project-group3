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


# Пример использования
if __name__ == "__main__":
    notebook = NoteBook()

    # Пример добавления записи с тегами
    input_text = "Сегодня я поучаствовал в #программирование. Было интересно!"
    notebook.add_note(input_text)

    # Пример добавления записи через пользовательский ввод
    NoteBook.add_note_from_user()
