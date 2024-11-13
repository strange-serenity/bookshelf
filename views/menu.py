import tkinter as tk

def create_menu(root, app):
    menu = tk.Menu(root)
    root.config(menu=menu)

    # Используем существующие контроллеры
    book_controller = app.book_controller
    author_controller = app.author_controller
    data_controller = app.data_controller

    # Меню для книг
    book_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Книги", menu=book_menu)
    book_menu.add_command(label="Додати книгу", command=book_controller.add_book)
    book_menu.add_command(label="Видалити книгу", command=book_controller.delete_book)
    book_menu.add_command(label="Оновити книгу", command=book_controller.update_book)
    book_menu.add_command(label="Пошук книги", command=book_controller.search_book)
    book_menu.add_command(label="Фільтрація за жанром", command=book_controller.filter_books)

    # Меню для авторов
    author_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Автори", menu=author_menu)
    author_menu.add_command(label="Додати автора", command=author_controller.add_author)
    author_menu.add_command(label="Видалити автора", command=author_controller.delete_author)
    author_menu.add_command(label="Оновити автора", command=author_controller.update_author)
    author_menu.add_command(label="Пошук за автором", command=author_controller.search_books_by_author)

    # Меню для загрузки/сохранения данных
    list_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Списки та збереження", menu=list_menu)
    list_menu.add_command(label="Зберегти дані", command=data_controller.save_data)
    list_menu.add_command(label="Завантажити дані", command=data_controller.load_data)
    list_menu.add_command(label="Перегляд усіх книг", command=data_controller.view_books)
    list_menu.add_command(label="Перегляд усіх авторів", command=data_controller.view_authors)

    # Выход
    menu.add_command(label="Вихід", command=root.quit)
