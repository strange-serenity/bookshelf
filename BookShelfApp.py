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
        self.root.geometry("1200x700")  # Установил размер окна
        self.book_list = []  # Список книг
        self.author_list = []  # Список авторов

        # Контроллеры
        self.book_controller = BookController(self, self.author_list, self.book_list)
        self.author_controller = AuthorController(self, self.author_list, self.book_list)
        self.data_controller = DataController(self, self.author_list, self.book_list)

        # Меню
        create_menu(self.root, self)

        # Список книг (слева)
        self.book_listbox = tk.Listbox(self.root, width=50, height=30)
        self.book_listbox.grid(row=0, column=0, padx=20, pady=10, sticky="n")

        # Кнопка обновления списка книг
        self.refresh_button = tk.Button(self.root, text="Оновити список книг", command=self.update_book_list)
        self.refresh_button.grid(row=1, column=0, pady=10, sticky="n")

        # Панель информации о книге (по центру)
        self.info_frame = tk.Frame(self.root, width=300, height=200, relief="groove", borderwidth=2)
        self.info_frame.grid(row=0, column=1, padx=20, pady=10, sticky="n")

        self.title_label = tk.Label(self.info_frame, text="Назва книги: ", anchor="w", font=("Arial", 12))
        self.title_label.pack(anchor="w", padx=10, pady=5)

        self.author_label = tk.Label(self.info_frame, text="Автор: ", anchor="w", font=("Arial", 12))
        self.author_label.pack(anchor="w", padx=10, pady=5)

        self.genre_label = tk.Label(self.info_frame, text="Жанр: ", anchor="w", font=("Arial", 12))
        self.genre_label.pack(anchor="w", padx=10, pady=5)

        self.rating_label = tk.Label(self.info_frame, text="Рейтинг: ", anchor="w", font=("Arial", 12))
        self.rating_label.pack(anchor="w", padx=10, pady=5)

        # Область для отображения текста книги (справа)
        self.text_area = tk.Text(self.root, width=60, height=30, wrap="word", font=("Arial", 10))
        self.text_area.grid(row=0, column=2, padx=20, pady=10, sticky="n")
        self.text_area.insert(tk.END, "Виберіть книгу для перегляду тексту.")

        # Область для отображения обложки книги (справа от текста)
        self.image_label = tk.Label(self.root, text="Обложка книги", width=30, height=15, relief="solid")
        self.image_label.grid(row=0, column=3, padx=20, pady=10, sticky="n")

        # Привязка событий
        self.book_listbox.bind('<<ListboxSelect>>', self.on_book_select)

    def update_book_list(self):
        self.book_listbox.delete(0, tk.END)
        for book in self.book_list:
            self.book_listbox.insert(tk.END, f"{book.title} - {book.author.name}")

    def on_book_select(self, event):
        selected_index = self.book_listbox.curselection()
        if selected_index:
            book = self.book_list[selected_index[0]]

            # Обновляем метки с информацией о книге
            self.title_label.config(text=f"Назва книги: {book.title}")
            self.author_label.config(text=f"Автор: {book.author.name}")
            self.genre_label.config(text=f"Жанр: {book.genre}")
            self.rating_label.config(text=f"Рейтинг: {book.rating}")

            # Загрузка изображения
            try:
                book_image = Image.open(f"{book.image_link}")
                book_image = book_image.resize((200, 300), Image.ANTIALIAS)
                book_image = ImageTk.PhotoImage(book_image)
                self.image_label.config(image=book_image)
                self.image_label.image = book_image
            except Exception as e:
                self.image_label.config(text="Не удалось загрузить обложку", image="")

            # Отображение текста книги
            self.text_area.delete(1.0, tk.END)
            try:
                with open(book.file_link, 'r', encoding='utf-8') as file:
                    text = file.read()
                    self.text_area.insert(tk.END, text)
            except Exception as e:
                self.text_area.insert(tk.END, f"Помилка при відкритті файлу: {e}")


if __name__ == "__main__":
    root_window = tk.Tk()
    app = BookShelfApp(root_window)
    root_window.mainloop()
