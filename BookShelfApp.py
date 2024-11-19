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
        self.root.geometry("300x0")  # Встановив розмір вікна
        self.book_list = []  # Список книг
        self.author_list = []  # Список авторів

        # Контролери
        self.book_controller = BookController(self, self.author_list, self.book_list)
        self.author_controller = AuthorController(self, self.author_list, self.book_list)
        self.data_controller = DataController(self, self.author_list, self.book_list)

        # Меню
        create_menu(self.root, self)

if __name__ == "__main__":
    root_window = tk.Tk()
    app = BookShelfApp(root_window)
    root_window.mainloop()
