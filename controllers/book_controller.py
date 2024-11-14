import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from constants.countries import COUNTRIES
from constants.genres import GENRES
from models import Author, Book


class BookController:
    def __init__(self, app, author_list, book_list):
        self.app = app
        self.book_list = book_list
        self.author_list = author_list

    def add_book(self):
        # Проверка на наличие авторов
        if not self.author_list:
            messagebox.showwarning("Помилка", "Список авторів порожній. Спочатку додайте автора.")
            return

        # Создаем окно для ввода информации о книге
        add_book_window = tk.Toplevel(self.app.root)
        add_book_window.title("Додавання книги")

        # Устанавливаем, чтобы это окно было поверх основного
        add_book_window.grab_set()  # Захват фокуса
        add_book_window.transient(self.app.root)  # Сделать окно зависимым от основного

        # Поле для ввода названия книги
        tk.Label(add_book_window, text="Назва книги:").grid(row=0, column=0, padx=10, pady=5)
        title_entry = tk.Entry(add_book_window)
        title_entry.grid(row=0, column=1, padx=10, pady=5)

        # Меню для выбора автора
        tk.Label(add_book_window, text="Автор:").grid(row=1, column=0, padx=10, pady=5)
        author_var = tk.StringVar(value=self.author_list[0].name)
        author_menu = tk.OptionMenu(add_book_window, author_var, *[author.name for author in self.author_list])
        author_menu.grid(row=1, column=1, padx=10, pady=5)

        # Меню для выбора жанра
        tk.Label(add_book_window, text="Жанр:").grid(row=2, column=0, padx=10, pady=5)
        genre_var = tk.StringVar(value=GENRES[0])
        genre_menu = tk.OptionMenu(add_book_window, genre_var, *GENRES)
        genre_menu.grid(row=2, column=1, padx=10, pady=5)

        # Меню для выбора страны
        tk.Label(add_book_window, text="Країна:").grid(row=3, column=0, padx=10, pady=5)
        country_var = tk.StringVar(value=COUNTRIES[0])
        country_menu = tk.OptionMenu(add_book_window, country_var, *COUNTRIES)
        country_menu.grid(row=3, column=1, padx=10, pady=5)

        # Поле для выбора файла книги
        tk.Label(add_book_window, text="Файл книги:").grid(row=4, column=0, padx=10, pady=5)
        file_entry = tk.Entry(add_book_window)
        file_entry.grid(row=4, column=1, padx=10, pady=5)

        def select_file():
            filename = filedialog.askopenfilename(title="Виберіть файл книги")
            if filename:
                file_entry.insert(0, filename)

        tk.Button(add_book_window, text="Вибрати файл", command=select_file).grid(row=4, column=2, padx=10, pady=5)

        # Поле для выбора изображения
        tk.Label(add_book_window, text="Зображення обкладинки:").grid(row=5, column=0, padx=10, pady=5)
        image_entry = tk.Entry(add_book_window)
        image_entry.grid(row=5, column=1, padx=10, pady=5)

        def select_image():
            filename = filedialog.askopenfilename(title="Виберіть зображення обкладинки")
            if filename:
                image_entry.insert(0, filename)

        tk.Button(add_book_window, text="Вибрати зображення", command=select_image).grid(row=5, column=2, padx=10,
                                                                                         pady=5)

        # Поле для ввода рейтинга
        tk.Label(add_book_window, text="Оцінка (1-5):").grid(row=6, column=0, padx=10, pady=5)
        rating_entry = tk.Entry(add_book_window)
        rating_entry.grid(row=6, column=1, padx=10, pady=5)

        # Функция для обработки нажатия кнопки ОК
        def on_ok():
            title = title_entry.get().strip()
            author_name = author_var.get().strip()
            genre = genre_var.get().strip()
            country = country_var.get().strip()
            file_link = file_entry.get().strip()
            image_link = image_entry.get().strip()
            rating_str = rating_entry.get().strip()

            # Проверка, что все поля заполнены
            if not (title and author_name and genre and country and file_link and image_link and rating_str):
                messagebox.showwarning("Помилка", "Заповніть усі поля.")
                return

            # Проверка, что рейтинг корректный
            try:
                rating = int(rating_str)
                if rating < 1 or rating > 5:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Помилка", "Оцінка повинна бути числом від 1 до 5.")
                return

            # Поиск объекта автора
            author = next((author for author in self.author_list if author.name == author_name), None)
            if not author:
                messagebox.showwarning("Помилка", "Автор не знайдений у списку.")
                return

            # Добавление книги
            book = Book(title, author, genre, file_link, image_link, rating)
            self.book_list.append(book)
            messagebox.showinfo("Успіх", "Книгу успішно додано!")
            add_book_window.destroy()

        # Кнопка ОК для добавления книги
        tk.Button(add_book_window, text="OK", command=on_ok).grid(row=7, column=1, pady=10)

        # Кнопка для отмены
        tk.Button(add_book_window, text="Скасувати", command=add_book_window.destroy).grid(row=7, column=2, pady=10)

    # Метод видалення книги за назвою
    def delete_book(self):
        if not self.book_list:
            messagebox.showinfo("Помилка", "Немає книг для видалення.")
            return

        # Создание окна для выбора книги
        delete_window = tk.Toplevel(self.app.root)
        delete_window.title("Вибір книги для видалення")

        # Создание списка книг
        listbox = tk.Listbox(delete_window, selectmode=tk.SINGLE)
        for book in self.book_list:
            listbox.insert(tk.END, book.title)

        listbox.pack(padx=20, pady=10)

        def on_delete():
            try:
                # Получаем выбранную книгу
                selected_index = listbox.curselection()[0]
                selected_book_title = self.book_list[selected_index].title

                # Удаляем выбранную книгу из списка
                self.book_list = [book for book in self.book_list if book.title != selected_book_title]
                messagebox.showinfo("Результат", f"Книгу '{selected_book_title}' видалено.")
                delete_window.destroy()
            except IndexError:
                messagebox.showwarning("Помилка", "Будь ласка, виберіть книгу для видалення.")

        # Кнопка для удаления
        delete_button = tk.Button(delete_window, text="Видалити", command=on_delete)
        delete_button.pack(pady=5)

        # Кнопка для закриття вікна без змін
        cancel_button = tk.Button(delete_window, text="Скасувати", command=delete_window.destroy)
        cancel_button.pack(pady=5)

    def update_book(self):
        if not self.book_list:
            messagebox.showinfo("Помилка", "Немає книг для оновлення.")
            return

        # Окно выбора книги для обновления
        select_book_window = tk.Toplevel(self.app.root)
        select_book_window.title("Вибір книги для оновлення")

        # Устанавливаем, чтобы это окно было поверх основного
        select_book_window.grab_set()  # Захват фокуса
        select_book_window.transient(self.app.root)  # Сделать окно зависимым от основного

        # Создаем список книг
        tk.Label(select_book_window, text="Оберіть книгу:").pack()
        book_titles = [book.title for book in self.book_list]
        listbox = tk.Listbox(select_book_window, selectmode=tk.SINGLE)
        for title in book_titles:
            listbox.insert(tk.END, title)
        listbox.pack(padx=20, pady=10)

        def on_select():
            try:
                selected_index = listbox.curselection()[0]
                selected_book = self.book_list[selected_index]
                select_book_window.destroy()

                # Окно для обновления информации о книге
                update_book_window = tk.Toplevel(self.app.root)
                update_book_window.title("Оновлення книги")

                # Поле для названия
                tk.Label(update_book_window, text="Назва книги:").grid(row=0, column=0, padx=10, pady=5)
                title_entry = tk.Entry(update_book_window)
                title_entry.insert(0, selected_book.title)
                title_entry.grid(row=0, column=1, padx=10, pady=5)

                # Меню для выбора автора
                tk.Label(update_book_window, text="Автор:").grid(row=1, column=0, padx=10, pady=5)
                author_var = tk.StringVar(value=selected_book.author.name)
                author_menu = tk.OptionMenu(update_book_window, author_var,
                                            *[author.name for author in self.author_list])
                author_menu.grid(row=1, column=1, padx=10, pady=5)

                # Меню для выбора жанра
                tk.Label(update_book_window, text="Жанр:").grid(row=2, column=0, padx=10, pady=5)
                genre_var = tk.StringVar(value=selected_book.genre)
                genre_menu = tk.OptionMenu(update_book_window, genre_var, *GENRES)
                genre_menu.grid(row=2, column=1, padx=10, pady=5)

                # Меню для выбора страны
                tk.Label(update_book_window, text="Країна:").grid(row=3, column=0, padx=10, pady=5)
                country_var = tk.StringVar(value=selected_book.author.country)
                country_menu = tk.OptionMenu(update_book_window, country_var, *COUNTRIES)
                country_menu.grid(row=3, column=1, padx=10, pady=5)

                # Поле для выбора файла книги
                tk.Label(update_book_window, text="Файл книги:").grid(row=4, column=0, padx=10, pady=5)
                file_entry = tk.Entry(update_book_window)
                file_entry.insert(0, selected_book.file_link)
                file_entry.grid(row=4, column=1, padx=10, pady=5)

                def select_file():
                    filename = filedialog.askopenfilename(title="Виберіть файл книги")
                    if filename:
                        file_entry.delete(0, tk.END)
                        file_entry.insert(0, filename)

                tk.Button(update_book_window, text="Вибрати файл", command=select_file).grid(row=4, column=2, padx=10,
                                                                                             pady=5)

                # Поле для выбора изображения
                tk.Label(update_book_window, text="Зображення обкладинки:").grid(row=5, column=0, padx=10, pady=5)
                image_entry = tk.Entry(update_book_window)
                image_entry.insert(0, selected_book.image_link)
                image_entry.grid(row=5, column=1, padx=10, pady=5)

                def select_image():
                    filename = filedialog.askopenfilename(title="Виберіть зображення обкладинки")
                    if filename:
                        image_entry.delete(0, tk.END)
                        image_entry.insert(0, filename)

                tk.Button(update_book_window, text="Вибрати зображення", command=select_image).grid(row=5, column=2,
                                                                                                    padx=10, pady=5)

                # Поле для рейтинга
                tk.Label(update_book_window, text="Оцінка (1-5):").grid(row=6, column=0, padx=10, pady=5)
                rating_entry = tk.Entry(update_book_window)
                rating_entry.insert(0, str(selected_book.rating))
                rating_entry.grid(row=6, column=1, padx=10, pady=5)

                # Функция для сохранения обновленных данных
                def on_save():
                    title = title_entry.get().strip()
                    author_name = author_var.get().strip()
                    genre = genre_var.get().strip()
                    country = country_var.get().strip()
                    file_link = file_entry.get().strip()
                    image_link = image_entry.get().strip()
                    rating_str = rating_entry.get().strip()

                    # Проверка, что все поля заполнены
                    if not (title and author_name and genre and country and file_link and image_link and rating_str):
                        messagebox.showwarning("Помилка", "Заповніть усі поля.")
                        return

                    # Проверка, что рейтинг корректный
                    try:
                        rating = int(rating_str)
                        if rating < 1 or rating > 5:
                            raise ValueError
                    except ValueError:
                        messagebox.showwarning("Помилка", "Оцінка повинна бути числом від 1 до 5.")
                        return

                    # Обновление данных книги
                    selected_book.title = title
                    selected_book.author = next((author for author in self.author_list if author.name == author_name),
                                                None)
                    selected_book.genre = genre
                    selected_book.author.country = country
                    selected_book.file_link = file_link
                    selected_book.image_link = image_link
                    selected_book.rating = rating

                    messagebox.showinfo("Успіх", "Книгу успішно оновлено!")
                    update_book_window.destroy()

                # Кнопка для сохранения изменений
                tk.Button(update_book_window, text="Зберегти", command=on_save).grid(row=7, column=1, pady=10)

                # Кнопка для отмены
                tk.Button(update_book_window, text="Скасувати", command=update_book_window.destroy).grid(row=7,
                                                                                                         column=2,
                                                                                                         pady=10)

            except IndexError:
                messagebox.showwarning("Помилка", "Будь ласка, оберіть книгу для оновлення.")

        # Кнопка для выбора книги
        tk.Button(select_book_window, text="Обрати", command=on_select).pack(pady=5)
        tk.Button(select_book_window, text="Скасувати", command=select_book_window.destroy).pack(pady=5)

    # Пошук книги за назвою
    def search_book(self):
        title = simpledialog.askstring("Пошук", "Введіть назву книги для пошуку:")
        found_books = [book for book in self.book_list if title.lower() in book.title.lower()]
        if found_books:
            messagebox.showinfo("Результати", "\n".join(str(book) for book in found_books))
        else:
            messagebox.showinfo("Результати", "Книгу не знайдено.")

    def filter_books(self):
        # Проверяем наличие жанров
        if not GENRES:
            messagebox.showwarning("Помилка", "Список жанрів порожній.")
            return

        # Создаем окно выбора жанра
        filter_window = tk.Toplevel(self.app.root)
        filter_window.geometry("300x150")
        filter_window.title("Фільтрація за жанром")

        # Метка и выбор жанра
        genre_label = tk.Label(filter_window, text="Виберіть жанр для фільтрації:")
        genre_label.pack(pady=10)

        # Переменная для хранения выбранного жанра
        genre_var = tk.StringVar()
        genre_var.set(GENRES[0])  # Устанавливаем первый жанр как значение по умолчанию

        # Меню для выбора жанра
        genre_menu = tk.OptionMenu(filter_window, genre_var, *GENRES)
        genre_menu.pack(pady=10)

        def apply_filter():
            # Получаем выбранный жанр
            genre = genre_var.get()
            # Фильтрация книг по выбранному жанру
            filtered_books = [book for book in self.book_list if book.genre.lower() == genre.lower()]
            if filtered_books:
                # Формируем строку с результатами
                results = "\n".join(
                    f"Назва: {book.title}, Автор: {book.author.name}, Рейтинг: {book.rating}" for book in
                    filtered_books)
                messagebox.showinfo("Результати фільтрації", results)
            else:
                messagebox.showinfo("Результати фільтрації", "Книги обраного жанру не знайдено.")
            filter_window.destroy()

        # Кнопка для применения фильтрации
        filter_button = tk.Button(filter_window, text="Застосувати фільтр", command=apply_filter)
        filter_button.pack(pady=10)