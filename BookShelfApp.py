import tkinter as tk
from views.menu import create_menu
from controllers.book_controller import BookController
from controllers.author_controller import AuthorController
from controllers.data_controller import DataController


# Основной класс для приложения
class BookShelfApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Книжкова полиця")

        # Инициализация списков
        self.book_list = []  # Список книг
        self.author_list = []  # Список авторов

        # Инициализация контроллеров с доступом к спискам
        self.book_controller = BookController(self, self.author_list, self.book_list)
        self.author_controller = AuthorController(self, self.author_list, self.book_list)
        self.data_controller = DataController(self, self.author_list, self.book_list)

        # Создаем меню
        create_menu(self.root, self)


if __name__ == "__main__":
    root_window = tk.Tk()
    root_window.geometry("400x300")
    app = BookShelfApp(root_window)
    root_window.mainloop()
