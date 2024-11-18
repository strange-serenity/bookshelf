import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from constants.countries import COUNTRIES
from models import Author
from datetime import datetime


class AuthorController:
    def __init__(self, app, author_list, book_list):
        self.app = app
        self.author_list = author_list
        self.book_list = book_list

    def add_author(self):
        # Створення вікна додавання автора
        add_author_window = tk.Toplevel(self.app.root)
        add_author_window.title("Додавання автора")

        # Робимо щоб додаткове вікно було вище за основне
        add_author_window.grab_set()  # Захват фокуса
        add_author_window.transient(self.app.root)  # Зробили вікно залежним від основного

        # Поле для вводу імені
        tk.Label(add_author_window, text="Ім'я автора:").grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(add_author_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Меню вибору країни
        tk.Label(add_author_window, text="Країна:").grid(row=1, column=0, padx=10, pady=5)
        country_var = tk.StringVar(value=COUNTRIES[0])
        country_menu = tk.OptionMenu(add_author_window, country_var, *COUNTRIES)
        country_menu.grid(row=1, column=1, padx=10, pady=5)

        # Поле для вводу даты народження
        tk.Label(add_author_window, text="Дата народження (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
        birth_date_entry = tk.Entry(add_author_window)
        birth_date_entry.grid(row=2, column=1, padx=10, pady=5)

        # Поле для вводу дати смерті
        tk.Label(add_author_window, text="Дата смерті (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5)
        death_date_entry = tk.Entry(add_author_window)
        death_date_entry.grid(row=3, column=1, padx=10, pady=5)

        # Радіокнопки для выбору статі
        tk.Label(add_author_window, text="Стать:").grid(row=4, column=0, padx=10, pady=5)
        gender_var = tk.StringVar(value="чоловіча")  # Значение по умолчанию

        tk.Radiobutton(add_author_window, text="Чоловіча", variable=gender_var, value="чоловіча").grid(row=4, column=1,
                                                                                                       sticky="w")
        tk.Radiobutton(add_author_window, text="Жіноча", variable=gender_var, value="жіноча").grid(row=4, column=2,
                                                                                                   sticky="w")

        # Кнопка для выбору файлу біографії
        tk.Label(add_author_window, text="Біографія (файл):").grid(row=5, column=0, padx=10, pady=5)
        biography_link_entry = tk.Entry(add_author_window)
        biography_link_entry.grid(row=5, column=1, padx=10, pady=5)

        def select_file():
            filename = filedialog.askopenfilename(title="Виберіть файл біографії")
            if filename:
                biography_link_entry.insert(0, filename)

        tk.Button(add_author_window, text="Вибрати файл", command=select_file).grid(row=5, column=2, padx=10, pady=5)

        # Обработчик кнопки OK
        def on_ok():
            name = name_entry.get().strip()
            country = country_var.get()
            birth_date_str = birth_date_entry.get().strip()
            death_date_str = death_date_entry.get().strip()
            gender = gender_var.get()
            biography_link = biography_link_entry.get().strip()

            # Перевірка полей на заповненність
            if not all([name, country, birth_date_str, death_date_str, gender, biography_link]):
                messagebox.showwarning("Помилка", "Усі поля повинні бути заповнені.")
                return

            # Преобразовання дат зі строки в datetime
            try:
                birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
                death_date = datetime.strptime(death_date_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Помилка", "Невірний формат дати. Використовуйте формат РРРР-ММ-ДД.")
                return

            # Створення и додавання автору
            author = Author(name, country, birth_date, death_date, gender, biography_link)
            self.author_list.append(author)
            messagebox.showinfo("Успіх", "Автор успішно доданий!")
            add_author_window.destroy()

        # Кнопка OK
        tk.Button(add_author_window, text="OK", command=on_ok).grid(row=6, column=0, columnspan=2, pady=10)

        # Кнопка Cancel
        tk.Button(add_author_window, text="Скасувати", command=add_author_window.destroy).grid(row=6, column=1, pady=10)

    pass

    def delete_author(self):
        # Відкриття діалогового вікна для вибору автора зі списка
        author_names = [author.name for author in self.author_list]
        if not author_names:
            messagebox.showinfo("Помилка", "Немає авторів для видалення.")
            return

        # Робимо вікно для выбору автора
        delete_window = tk.Toplevel(self.app.root)
        delete_window.title("Вибір автора для видалення")

        # Додаємо список авторів
        listbox = tk.Listbox(delete_window, selectmode=tk.SINGLE)
        for name in author_names:
            listbox.insert(tk.END, name)

        listbox.pack(padx=20, pady=10)

        def on_delete():
            try:
                # Отримуємо обраного автора
                selected_index = listbox.curselection()[0]
                selected_author_name = author_names[selected_index]
                # Видаляєм обраного автора зі списка
                self.author_list = [author for author in self.author_list if author.name != selected_author_name]
                messagebox.showinfo("Результат", f"Автор '{selected_author_name}' видалений.")
                delete_window.destroy()
            except IndexError:
                messagebox.showwarning("Помилка", "Будь ласка, виберіть автора для видалення.")

        # Кнопка для видалення
        delete_button = tk.Button(delete_window, text="Видалити", command=on_delete)
        delete_button.pack(pady=5)

        # Кнопка для закритяя вікна без змін
        cancel_button = tk.Button(delete_window, text="Скасувати", command=delete_window.destroy)
        cancel_button.pack(pady=5)

    def update_author(self):
        # Створення списку імен авторів
        author_names = [author.name for author in self.author_list]
        if not author_names:
            messagebox.showinfo("Помилка", "Немає авторів для оновлення.")
            return

        # Вікно для вибору автора
        select_author_window = tk.Toplevel(self.app.root)
        select_author_window.title("Вибір автора для оновлення")

        # Робимо, щоб окно вікно було поверх основного
        select_author_window.grab_set()  # Захват фокусу
        select_author_window.transient(self.app.root)  # Зробити вікно залежним від основного

        # Список авторів
        listbox = tk.Listbox(select_author_window, selectmode=tk.SINGLE)
        for name in author_names:
            listbox.insert(tk.END, name)
        listbox.pack(padx=20, pady=10)

        def open_update_window():
            try:
                # Отримуємо вибранного автора
                selected_index = listbox.curselection()[0]
                selected_author_name = author_names[selected_index]
                # Шукаємо автора за ім'ям
                author_to_update = next(author for author in self.author_list if author.name == selected_author_name)

                # Створення вікна редагування автору
                update_author_window = tk.Toplevel(self.app.root)
                update_author_window.title("Оновлення автора")

                # Поля вводу с текущими значеннями автору
                tk.Label(update_author_window, text="Ім'я автора:").grid(row=0, column=0, padx=10, pady=5)
                name_entry = tk.Entry(update_author_window)
                name_entry.insert(0, author_to_update.name)
                name_entry.grid(row=0, column=1, padx=10, pady=5)

                # Меню вибору країни с текущим значенням
                tk.Label(update_author_window, text="Країна:").grid(row=1, column=0, padx=10, pady=5)
                country_var = tk.StringVar(value=author_to_update.country)
                country_menu = tk.OptionMenu(update_author_window, country_var, *COUNTRIES)
                country_menu.grid(row=1, column=1, padx=10, pady=5)

                # Поле для вводу дати нарождення с текущим значенням
                tk.Label(update_author_window, text="Дата народження (YYYY-MM-DD):").grid(row=2, column=0, padx=10,
                                                                                          pady=5)
                birth_date_entry = tk.Entry(update_author_window)
                birth_date_entry.insert(0, author_to_update.birth_date.strftime("%Y-%m-%d"))
                birth_date_entry.grid(row=2, column=1, padx=10, pady=5)

                # Поле для вводу дати смерті с текущим значенням
                tk.Label(update_author_window, text="Дата смерті (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5)
                death_date_entry = tk.Entry(update_author_window)
                death_date_entry.insert(0, author_to_update.death_date.strftime("%Y-%m-%d"))
                death_date_entry.grid(row=3, column=1, padx=10, pady=5)

                # Радіокнопки для выбору статі с текущим значенням
                tk.Label(update_author_window, text="Стать:").grid(row=4, column=0, padx=10, pady=5)
                gender_var = tk.StringVar(value=author_to_update.gender)
                tk.Radiobutton(update_author_window, text="Чоловіча", variable=gender_var, value="чоловіча").grid(row=4,
                                                                                                                  column=1,
                                                                                                                  sticky="w")
                tk.Radiobutton(update_author_window, text="Жіноча", variable=gender_var, value="жіноча").grid(row=4,
                                                                                                              column=2,
                                                                                                              sticky="w")

                # Поле для файлу біографії с текущим значенням
                tk.Label(update_author_window, text="Біографія (файл):").grid(row=5, column=0, padx=10, pady=5)
                biography_link_entry = tk.Entry(update_author_window)
                biography_link_entry.insert(0, author_to_update.biography_link)
                biography_link_entry.grid(row=5, column=1, padx=10, pady=5)

                def select_file():
                    filename = filedialog.askopenfilename(title="Виберіть файл біографії")
                    if filename:
                        biography_link_entry.delete(0, tk.END)
                        biography_link_entry.insert(0, filename)

                tk.Button(update_author_window, text="Вибрати файл", command=select_file).grid(row=5, column=2, padx=10,
                                                                                               pady=5)

                # Обработчик кнопки OK
                def on_ok():
                    # Оброблюємо оновленні дані
                    author_to_update.name = name_entry.get().strip()
                    author_to_update.country = country_var.get()
                    author_to_update.gender = gender_var.get()
                    author_to_update.biography_link = biography_link_entry.get().strip()

                    # Преобразування дат зі строки в datetime
                    try:
                        author_to_update.birth_date = datetime.strptime(birth_date_entry.get().strip(), "%Y-%m-%d")
                        author_to_update.death_date = datetime.strptime(death_date_entry.get().strip(), "%Y-%m-%d")
                    except ValueError:
                        messagebox.showwarning("Помилка", "Невірний формат дати. Використовуйте формат РРРР-ММ-ДД.")
                        return

                    # Закрыття вікна и повідомлення про успії
                    messagebox.showinfo("Результат", "Інформацію оновлено.")
                    update_author_window.destroy()
                    select_author_window.destroy()

                # Кнопка OK
                tk.Button(update_author_window, text="Оновити", command=on_ok).grid(row=6, column=0, columnspan=2,
                                                                                    pady=10)

                # Кнопка Cancel
                tk.Button(update_author_window, text="Скасувати", command=update_author_window.destroy).grid(row=6,
                                                                                                             column=1,
                                                                                                             pady=10)

            except IndexError:
                messagebox.showwarning("Помилка", "Будь ласка, виберіть автора для оновлення.")

        # Кнопка для відкриття вікна оновлення
        tk.Button(select_author_window, text="Обрати", command=open_update_window).pack(pady=5)
        tk.Button(select_author_window, text="Скасувати", command=select_author_window.destroy).pack(pady=5)

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

        # Пошук книг за ім'ям автора
        found_books = [book for book in self.book_list if
                       book.author and book.author.name.lower() == author_name.lower()]
        if found_books:
            messagebox.showinfo("Результати пошуку", "\n".join(str(book) for book in found_books))
        else:
            messagebox.showinfo("Результати пошуку", "Книги цього автора не знайдено.")
