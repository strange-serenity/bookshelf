import tkinter as tk
from views.menu import create_menu
from controllers.book_controller import BookController
from controllers.author_controller import AuthorController
from controllers.data_controller import DataController
from PIL import Image, ImageTk  # Імпортуємо Pillow

class BookShelfApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Книжкова полиця")
        self.root.attributes("-fullscreen", True)
        self.book_list = []  # Список книг
        self.author_list = []  # Список авторів

        self.book_controller = BookController(self, self.author_list, self.book_list)
        self.author_controller = AuthorController(self, self.author_list, self.book_list)
        self.data_controller = DataController(self, self.author_list, self.book_list)

        create_menu(self.root, self)

        self.book_listbox = tk.Listbox(self.root, width=80, height=50)
        self.book_listbox.pack(padx=20, pady=10, side=tk.LEFT)

        self.refresh_button = tk.Button(self.root, text="Оновити список книг", command=self.update_book_list)
        self.refresh_button.pack(side=tk.LEFT)

        self.update_book_list()

        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(side=tk.LEFT, padx=20)

        self.title_label = tk.Label(self.info_frame, text="Назва книги: ")
        self.title_label.pack()

        self.author_label = tk.Label(self.info_frame, text="Автор: ")
        self.author_label.pack()

        self.genre_label = tk.Label(self.info_frame, text="Жанр: ")
        self.genre_label.pack()

        self.rating_label = tk.Label(self.info_frame, text="Рейтинг: ")
        self.rating_label.pack()

        self.text_area = tk.Text(self.root, width=60, height=50)
        self.text_area.pack(side=tk.RIGHT, padx=20)
        self.text_area.insert(tk.END, "Виберіть книгу для перегляду тексту.")

        self.book_listbox.bind('<<ListboxSelect>>', self.on_book_select)

        self.image_label = None  # Це буде зберігати посилання на поточне зображення

    def update_book_list(self):
        self.book_listbox.delete(0, tk.END)
        for book in self.book_list:
            self.book_listbox.insert(tk.END, f"{book.title} - {book.author.name}")

    def on_book_select(self, event):
        selected_index = self.book_listbox.curselection()
        if selected_index:
            book = self.book_list[selected_index[0]]

            # Оновлюємо мітки з інформацією про книгу
            self.title_label.config(text=f"Назва книги: {book.title}")
            self.author_label.config(text=f"Автор: {book.author.name}")
            self.genre_label.config(text=f"Жанр: {book.genre}")
            self.rating_label.config(text=f"Рейтинг: {book.rating}")

            # Завантажуємо та відображаємо зображення з використанням Pillow
            try:
                book_image = Image.open(f"{book.image_link}")
                book_image = ImageTk.PhotoImage(book_image)  # Перетворюємо зображення у формат, який підтримує tkinter
                if self.image_label:
                    self.image_label.destroy()  # Видаляємо старе зображення, якщо воно було
                self.image_label = tk.Label(self.root, image=book_image)
                self.image_label.image = book_image  # Зберігаємо посилання на зображення
                self.image_label.pack()
            except Exception as e:
                print(f"Помилка при завантаженні зображення: {e}")

            self.text_area.delete(1.0, tk.END)

            try:
                with open(book.file_link, 'r', encoding='utf-8') as file:
                    text = file.read()
                    self.text_area.insert(tk.END, text)
            except Exception as e:
                self.text_area.insert(tk.END, f"Помилка при відкритті файлу: {e}")


if __name__ == "__main__":
    root_window = tk.Tk()
    root_window.geometry("800x400")
    app = BookShelfApp(root_window)
    root_window.mainloop()
