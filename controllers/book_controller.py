import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from constants.countries import COUNTRIES
from constants.genres import GENRES
from models import Author, Book


class BookController:
    def __init__(self, app, book_list):
        self.app = app
        self.book_list = book_list  # Теперь у контроллера есть доступ к списку книг

    # Метод додавання книги
    def add_book(self):
        # Введення назви книги
        title = None
        while not title:  # Цикл будет продолжаться, пока не введено название
            title = simpledialog.askstring("Input", "Enter the book title:")
            if title is None:  # Якщо натиснуто Cancel або закрито вікно
                return
            if not title:  # Якщо залишено порожнім
                messagebox.showwarning("Warning", "Please enter a title for the book.")

        # Введення імені автора
        author_name = None
        while not author_name:  # Цикл буде продовжуватися, поки не введено ім'я автора
            author_name = simpledialog.askstring("Input", "Enter the author:")
            if author_name is None:  # Якщо натиснуто Cancel або закрито вікно
                return
            if not author_name:  # Якщо залишено порожнім
                messagebox.showwarning("Warning", "Please enter the author's name.")

        # Створення вікна для вибору жанру
        genre_window = tk.Toplevel()
        genre_window.title("Select Genre")
        genre_label = tk.Label(genre_window, text="Choose a genre:")
        genre_label.pack()

        genre_var = tk.StringVar()
        genre_var.set(GENRES[0])  # За замовчуванням перший жанр

        genre_menu = tk.OptionMenu(genre_window, genre_var, *GENRES)
        genre_menu.pack()

        def select_genre():
            genre = genre_var.get()
            genre_window.destroy()

            # Вибір країни
            country_window = tk.Toplevel()
            country_window.title("Select Country")
            country_label = tk.Label(country_window, text="Choose a country:")
            country_label.pack()

            country_var = tk.StringVar()
            country_var.set(COUNTRIES[0])  # За замовчуванням перша країна

            country_menu = tk.OptionMenu(country_window, country_var, *COUNTRIES)
            country_menu.pack()

            def select_country():
                country = country_var.get()
                country_window.destroy()

                # Вибір файлів
                file_link = filedialog.askopenfilename(title="Select a file")
                if not file_link:  # Якщо натиснуто Cancel
                    return

                image_link = filedialog.askopenfilename(title="Select an image file")
                if not image_link:  # Якщо натиснуто Cancel
                    return

                # Оцінка книги
                rating = None
                while rating is None:  # Цикл для оцінки книги, поки не введено значення
                    rating = simpledialog.askinteger("Input", "Rate the book (1-5):", minvalue=1, maxvalue=5)
                    if rating is None:  # Якщо натиснуто Cancel або закрито вікно
                        return
                    if not (1 <= rating <= 5):  # Перевірка на діапазон
                        messagebox.showwarning("Warning", "Please rate the book between 1 and 5.")

                # Перевірка всіх полів
                if title and author_name and genre and country:
                    # Створення автора
                    author = Author(name=author_name, country=country, birth_date=None, death_date=None, gender="",
                                    biography_link="")

                    # Створення книги з автором
                    book = Book(title, author, genre, file_link, image_link, rating)

                    # Додавання книги до списку
                    self.book_list.append(book)
                    messagebox.showinfo("Success", "Book added successfully!")
                else:
                    messagebox.showwarning("Incomplete Data", "Please fill all the fields to add a book.")

            # Кнопка вибору країни
            select_country_button = tk.Button(country_window, text="Select", command=select_country)
            select_country_button.pack()

        # Кнопка вибору жанру
        select_genre_button = tk.Button(genre_window, text="Select", command=select_genre)
        select_genre_button.pack()

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

    # Оновлення інформації про книгу
    def update_book(self):
        title = simpledialog.askstring("Оновлення книги", "Введіть назву книги для оновлення:")
        for book in self.book_list:
            if book.title.lower() == title.lower():
                new_title = simpledialog.askstring("Нова назва", "Введіть нову назву:", initialvalue=book.title)
                book.title = new_title or book.title  # оновити назву, якщо введено нове значення
                messagebox.showinfo("Результат", "Інформацію оновлено.")
                return
        messagebox.showinfo("Результат", "Книгу не знайдено.")

    # Пошук книги за назвою
    def search_book(self):
        title = simpledialog.askstring("Пошук", "Введіть назву книги для пошуку:")
        found_books = [book for book in self.book_list if title.lower() in book.title.lower()]
        if found_books:
            messagebox.showinfo("Результати", "\n".join(str(book) for book in found_books))
        else:
            messagebox.showinfo("Результати", "Книгу не знайдено.")

    # Добавляем метод фильтрации книг по жанру
    def filter_books(self):
        genre = simpledialog.askstring("Фільтрація за жанром", f"Введіть жанр для фільтрації {GENRES}:")
        if genre not in GENRES:
            messagebox.showwarning("Помилка", "Обраний жанр не існує в списку.")
            return
        filtered_books = [book for book in self.book_list if book.genre.lower() == genre.lower()]
        if filtered_books:
            messagebox.showinfo("Результати фільтрації", "\n".join(str(book) for book in filtered_books))
        else:
            messagebox.showinfo("Результати фільтрації", "Книги обраного жанру не знайдено.")