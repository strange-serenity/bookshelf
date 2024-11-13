import tkinter as tk
from views.menu import create_menu
from controllers.book_controller import BookController
from controllers.author_controller import AuthorController
from controllers.data_controller import DataController


# Основной класс для приложения
class BookShelfApp:
    def __init__(self):
        self.root = root
        self.root.title("Книжкова полиця")

        # Инициализация списков
        self.book_list = []  # Список книг
        self.author_list = []  # Список авторов

        # Инициализация контроллеров с доступом к спискам
        self.book_controller = BookController(self, self.book_list)
        self.author_controller = AuthorController(self, self.author_list, self.book_list)
        self.data_controller = DataController(self, self.book_list, self.author_list)

        # Создаем меню
        create_menu(root, self)


if __name__ == "__main__":
    root = tk.Tk()
    app = BookShelfApp(root)
    root.mainloop()