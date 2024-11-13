import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog

from constants.countries import COUNTRIES
from models import Author
from utils.ask_date import ask_date


class AuthorController:
    def __init__(self, app, author_list, book_list):
        self.app = app
        self.author_list = author_list
        self.book_list = book_list

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
    pass

    def delete_author(self):
        # Открытие диалогового окна для выбора автора из списка
        author_names = [author.name for author in self.author_list]
        if not author_names:
            messagebox.showinfo("Помилка", "Немає авторів для видалення.")
            return

        # Создаём окно для выбора автора
        delete_window = tk.Toplevel(self.app.root)
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

    def update_author(self):
        # Создание списка имен авторов
        author_names = [author.name for author in self.author_list]
        if not author_names:
            messagebox.showinfo("Помилка", "Немає авторів для оновлення.")
            return

        # Окно для выбора автора
        update_window = tk.Toplevel(self.app.root)
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

    # Пошук авторів
    def find_author_by_name(self, name):
        return next((author for author in self.author_list if author.name.lower() == name.lower()), None)

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
