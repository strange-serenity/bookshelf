import json
from tkinter import filedialog, messagebox
from models import Book, Author

class DataController:
    def __init__(self, app, author_list, book_list):
        self.app = app
        self.book_list = book_list
        self.author_list = author_list

    # Збереження даних у файл
    def save_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            data = {
                "books": [book.to_dict() for book in self.book_list],  # используем метод to_dict
                "authors": [author.to_dict() for author in self.author_list]  # используем метод to_dict
            }
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, default=str)
            messagebox.showinfo("Збереження", "Дані збережено успішно!")

    # Завантаження даних з файлу
    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                # Используем from_dict для восстановления объектов
                self.book_list = [Book.from_dict(book) for book in data["books"]]
                self.author_list = [Author.from_dict(author) for author in data["authors"]]
            messagebox.showinfo("Завантаження", "Дані завантажено успішно!")

    # Перегляд усіх книг
    def view_books(self):
        if self.book_list:
            messagebox.showinfo("Список книг", "\n".join(str(book) for book in self.book_list))
        else:
            messagebox.showinfo("Список книг", "Немає книг у бібліотеці.")

    # Перегляд усіх авторів
    def view_authors(self):
        if self.author_list:
            messagebox.showinfo("Список авторів", "\n".join(str(author) for author in self.author_list))
        else:
            messagebox.showinfo("Список авторів", "Немає авторів у бібліотеці.")
