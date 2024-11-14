import tkinter as tk
from models import Book, Author  # Предполагается, что ваши классы находятся в models.py
from views.menu import create_menu
from controllers.book_controller import BookController
from controllers.author_controller import AuthorController
from controllers.data_controller import DataController

# Основной класс для приложения
class BookShelfApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Книжкова полиця")
        # Устанавливаем окно в полноэкранный режим
        self.root.attributes("-fullscreen", True)
        # Инициализация списков
        self.book_list = []  # Список книг
        self.author_list = []  # Список авторов

        # Инициализация контроллеров с доступом к спискам
        self.book_controller = BookController(self, self.author_list, self.book_list)
        self.author_controller = AuthorController(self, self.author_list, self.book_list)
        self.data_controller = DataController(self, self.author_list, self.book_list)

        # Создаем меню
        create_menu(self.root, self)

        # Создаем список книг
        self.book_listbox = tk.Listbox(self.root, width=50, height=10)
        self.book_listbox.pack(padx=20, pady=10, side=tk.LEFT)

        # Кнопка для обновления списка книг
        self.refresh_button = tk.Button(self.root, text="Оновити список книг", command=self.update_book_list)
        self.refresh_button.pack(pady=5, side=tk.LEFT)

        # Обновляем список книг при запуске
        self.update_book_list()

        # Создаем область для отображения информации о книге
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(side=tk.LEFT, padx=20)

        # Метки для информации о книге
        self.title_label = tk.Label(self.info_frame, text="Название книги: ")
        self.title_label.pack()

        self.author_label = tk.Label(self.info_frame, text="Автор: ")
        self.author_label.pack()

        self.genre_label = tk.Label(self.info_frame, text="Жанр: ")
        self.genre_label.pack()

        self.rating_label = tk.Label(self.info_frame, text="Рейтинг: ")
        self.rating_label.pack()

        # Текстовое поле для отображения текста книги
        self.text_area = tk.Text(self.root, width=40, height=10)
        self.text_area.pack(side=tk.LEFT, padx=20)
        self.text_area.insert(tk.END, "Выберите книгу для просмотра текста.")

        # Обработчик для выбора книги
        self.book_listbox.bind('<<ListboxSelect>>', self.on_book_select)

    def update_book_list(self):
        # Очищаем текущий список
        self.book_listbox.delete(0, tk.END)

        # Добавляем книги в Listbox
        for book in self.book_list:
            self.book_listbox.insert(tk.END, f"{book.title} - {book.author.name}")

    def on_book_select(self, event):
        # Получаем индекс выбранной книги
        selected_index = self.book_listbox.curselection()
        if selected_index:
            book = self.book_list[selected_index[0]]

            # Обновляем метки с информацией о книге
            self.title_label.config(text=f"Название книги: {book.title}")
            self.author_label.config(text=f"Автор: {book.author.name}")
            self.genre_label.config(text=f"Жанр: {book.genre}")
            self.rating_label.config(text=f"Рейтинг: {book.rating}")

            # Очищаем и выводим текст книги
            self.text_area.delete(1.0, tk.END)

            # Открываем файл с текстом книги и выводим его в Text виджет
            try:
                with open(book.file_link, 'r', encoding='utf-8') as file:
                    text = file.read()
                    self.text_area.insert(tk.END, text)
            except Exception as e:
                self.text_area.insert(tk.END, f"Ошибка при открытии файла: {e}")

if __name__ == "__main__":
    root_window = tk.Tk()
    root_window.geometry("800x400")
    app = BookShelfApp(root_window)
    root_window.mainloop()
