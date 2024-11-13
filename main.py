import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from typing import List, Optional
import json
from models import Author, Book
from constants.countries import COUNTRIES
from constants.genres import GENRES
from utils.ask_date import ask_date


# Головний клас програми
class BookShelfApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Книжкова полиця")

        self.book_list: List[Book] = []
        self.author_list: List[Author] = []

        # Основне меню
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        # Меню для книг
        book_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Книги", menu=book_menu)
        book_menu.add_command(label="Додати книгу", command=self.add_book)
        book_menu.add_command(label="Видалити книгу", command=self.delete_book)
        book_menu.add_command(label="Оновити інформацію про книгу", command=self.update_book)
        book_menu.add_command(label="Пошук книги за назвою", command=self.search_book)
        book_menu.add_command(label="Фільтрація книг за жанром", command=self.filter_books)

        # Меню для авторів
        author_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Автори", menu=author_menu)
        author_menu.add_command(label="Додати автора", command=self.add_author)
        author_menu.add_command(label="Видалити автора", command=self.delete_author)
        author_menu.add_command(label="Оновити інформацію про автора", command=self.update_author)
        author_menu.add_command(label="Пошук книг за автором", command=self.search_books_by_author)

        # Меню для списків і збереження
        list_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Списки та збереження", menu=list_menu)
        list_menu.add_command(label="Перегляд усіх книг", command=self.view_books)
        list_menu.add_command(label="Перегляд усіх авторів", command=self.view_authors)
        list_menu.add_command(label="Зберегти дані", command=self.save_data)
        list_menu.add_command(label="Завантажити дані", command=self.load_data)

        # Вихід
        exit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Вихід", menu=exit_menu)
        exit_menu.add_command(label="Вихід", command=root.quit)

    # Метод додавання автора
    def add_author(self):
        # Запит імені
        name = simpledialog.askstring("Додавання автора", "Введіть ім'я автора:")
        if not name:
            return  # Якщо натиснуто Cancel

        # Вибір країни
        country = simpledialog.askstring("Країна", f"Виберіть країну {COUNTRIES}:")
        if not country:
            return  # Якщо натиснуто Cancel

        # Запит дати народження
        birth_date = ask_date("Дата народження")
        if birth_date is None:
            return  # Якщо натиснуто Cancel або невірний формат дати

        # Запит дати смерті
        death_date = ask_date("Дата смерті")
        if death_date is None:
            return  # Якщо натиснуто Cancel або невірний формат дати

        # Запит статі
        gender = simpledialog.askstring("Стать", "Введіть стать (чоловіча або жіноча):")
        if not gender:
            return  # Якщо натиснуто Cancel

        # Вибір файлу біографії
        biography_link = filedialog.askopenfilename(title="Виберіть файл біографії")
        if not biography_link:
            return  # Якщо натиснуто Cancel

        # Створення автора
        author = Author(name, country, birth_date, death_date, gender, biography_link)

        # Додавання автора до списку
        self.author_list.append(author)
        messagebox.showinfo("Success", "Author added successfully!")

    # Метод додавання книги
    def add_book(self):
        # Введення назви книги
        title = simpledialog.askstring("Input", "Enter the book title:")
        if not title:  # Якщо натиснуто Cancel
            return

        # Введення імені автора
        author_name = simpledialog.askstring("Input", "Enter the author:")
        if not author_name:  # Якщо натиснуто Cancel
            return

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
                rating = simpledialog.askinteger("Input", "Rate the book (1-5):", minvalue=1, maxvalue=5)
                if not rating:  # Якщо натиснуто Cancel
                    return

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

    # Пошук книг за автором
    def search_books_by_author(self):
        author_name = simpledialog.askstring("Пошук книг за автором", "Введіть ім'я автора:")
        found_author = self.find_author_by_name(author_name)
        if not found_author:
            messagebox.showwarning("Помилка", "Автор не знайдений.")
            return

        # Поиск книг по имени автора
        found_books = [book for book in self.book_list if
                       book.author and book.author.name.lower() == author_name.lower()]
        if found_books:
            messagebox.showinfo("Результати пошуку", "\n".join(str(book) for book in found_books))
        else:
            messagebox.showinfo("Результати пошуку", "Книги цього автора не знайдено.")

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

    # Пошук книги за назвою
    def search_book(self):
        title = simpledialog.askstring("Пошук", "Введіть назву книги для пошуку:")
        found_books = [book for book in self.book_list if title.lower() in book.title.lower()]
        if found_books:
            messagebox.showinfo("Результати", "\n".join(str(book) for book in found_books))
        else:
            messagebox.showinfo("Результати", "Книгу не знайдено.")

    # Видалення книги за назвою
    def delete_book(self):
        title = simpledialog.askstring("Видалення книги", "Введіть назву книги для видалення:")
        if title:
            self.book_list = [book for book in self.book_list if book.title.lower() != title.lower()]
            messagebox.showinfo("Результат", f"Книгу '{title}' видалено." if title else "Книгу не знайдено.")

    # Збереження даних у файл
    def save_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            data = {
                "books": [book.__dict__ for book in self.book_list],
                "authors": [author.__dict__ for author in self.author_list]
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
                self.book_list = [Book(**book) for book in data["books"]]
                self.author_list = [Author(**author) for author in data["authors"]]
            messagebox.showinfo("Завантаження", "Дані завантажено успішно!")

    # Пошук автора за ім'ям
    def find_author_by_name(self, name: str) -> Optional[Author]:
        for author in self.author_list:
            if author.name.lower() == name.lower():
                return author
        return None

    def update_author(self):
        # Создание списка имен авторов
        author_names = [author.name for author in self.author_list]
        if not author_names:
            messagebox.showinfo("Помилка", "Немає авторів для оновлення.")
            return

        # Окно для выбора автора
        update_window = tk.Toplevel(self.root)
        update_window.title("Вибір автора для оновлення")

        # Добавление списка авторов
        listbox = tk.Listbox(update_window, selectmode=tk.SINGLE)
        for name in author_names:
            listbox.insert(tk.END, name)
        listbox.pack(padx=20, pady=10)

        def on_update():
            try:
                # Получаем выбранного автора
                selected_index = listbox.curselection()[0]
                selected_author_name = author_names[selected_index]

                # Ищем автора по выбранному имени
                author_to_update = next(author for author in self.author_list if author.name == selected_author_name)

                # Запрос новой информации для каждого поля
                new_country = simpledialog.askstring("Нова країна", "Введіть нову країну:",
                                                     initialvalue=author_to_update.country)
                if new_country:  # Если введена новая страна, обновляем
                    author_to_update.country = new_country

                new_birth_date = ask_date("Нова дата народження")
                if new_birth_date:  # Если введена новая дата, обновляем
                    author_to_update.birth_date = new_birth_date

                new_death_date = ask_date("Нова дата смерті")
                if new_death_date:  # Если введена новая дата, обновляем
                    author_to_update.death_date = new_death_date

                new_gender = simpledialog.askstring("Нова стать", "Введіть нову стать:",
                                                    initialvalue=author_to_update.gender)
                if new_gender:  # Если введен новый пол, обновляем
                    author_to_update.gender = new_gender

                new_biography_link = filedialog.askopenfilename(title="Виберіть файл біографії",
                                                                initialdir=author_to_update.biography_link or "")
                if new_biography_link:  # Если выбрали новый файл, обновляем
                    author_to_update.biography_link = new_biography_link

                # Уведомление об успешном обновлении
                messagebox.showinfo("Результат", "Інформацію оновлено.")
                update_window.destroy()
            except IndexError:
                messagebox.showwarning("Помилка", "Будь ласка, виберіть автора для оновлення.")

        # Кнопка для обновления
        update_button = tk.Button(update_window, text="Оновити", command=on_update)
        update_button.pack(pady=5)

        # Кнопка для закрытия окна без изменений
        cancel_button = tk.Button(update_window, text="Скасувати", command=update_window.destroy)
        cancel_button.pack(pady=5)

    def delete_author(self):
        # Открытие диалогового окна для выбора автора из списка
        author_names = [author.name for author in self.author_list]
        if not author_names:
            messagebox.showinfo("Помилка", "Немає авторів для видалення.")
            return

        # Создаём окно для выбора автора
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Вибір автора для видалення")

        # Добавляем список авторов
        listbox = tk.Listbox(delete_window, selectmode=tk.SINGLE)
        for name in author_names:
            listbox.insert(tk.END, name)

        listbox.pack(padx=20, pady=10)

        def on_delete():
            try:
                # Получаем выбранного автора
                selected_index = listbox.curselection()[0]
                selected_author_name = author_names[selected_index]
                # Удаляем выбранного автора из списка
                self.author_list = [author for author in self.author_list if author.name != selected_author_name]
                messagebox.showinfo("Результат", f"Автор '{selected_author_name}' видалений.")
                delete_window.destroy()
            except IndexError:
                messagebox.showwarning("Помилка", "Будь ласка, виберіть автора для видалення.")

        # Кнопка для удаления
        delete_button = tk.Button(delete_window, text="Видалити", command=on_delete)
        delete_button.pack(pady=5)

        # Кнопка для закрытия окна без изменений
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



# Запуск програми
if __name__ == "__main__":
    root = tk.Tk()
    app = BookShelfApp(root)
    root.mainloop()
