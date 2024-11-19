import tkinter as tk
from PIL import Image, ImageTk  # Імпортуємо Pillow
import json
from tkinter import filedialog, messagebox
from models import Book, Author

class DataController:
    def __init__(self, app, author_list, book_list):
        self.app = app
        self.book_list = book_list
        self.author_list = author_list

    # Збереження даних у файл
    def save_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            data = {
                "books": [book.to_dict() for book in self.book_list],  # используем метод to_dict
                "authors": [author.to_dict() for author in self.author_list]  # используем метод to_dict
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
                # Используем from_dict для восстановления объектов
                self.book_list = [Book.from_dict(book) for book in data["books"]]
                self.author_list = [Author.from_dict(author) for author in data["authors"]]
            messagebox.showinfo("Завантаження", "Дані завантажено успішно!")

    # Методы для работы с книгами
    def view_books(self):
        if not self.book_list:
            messagebox.showinfo("Список книг", "Немає книг у бібліотеці.")
            return

        # Создаем окно выбора книги
        book_window = tk.Toplevel(self.app.root)
        book_window.geometry("300x300")
        book_window.title("Вибір книги")

        tk.Label(book_window, text="Оберіть книгу:").pack(pady=10)

        # Создаем Listbox для отображения списка книг
        book_listbox = tk.Listbox(book_window, height=10, width=40)
        book_listbox.pack(pady=10)

        # Заполняем Listbox списком книг
        for book in self.book_list:
            book_listbox.insert(tk.END, book.title)

        def apply_selection():
            # Получаем выбранную книгу
            selected_index = book_listbox.curselection()
            if selected_index:
                selected_book = self.book_list[selected_index[0]]
                # Открываем окно с информацией о книге
                self.open_book_info_window(selected_book)
            book_window.destroy()

        # Кнопка для применения выбора
        tk.Button(book_window, text="ОК", command=apply_selection).pack(pady=10)

    def open_book_info_window(self, book):
        # Создаем новое окно для информации о книге
        info_window = tk.Toplevel(self.app.root)
        info_window.geometry("600x600")
        info_window.title(f"Інформація про книгу: {book.title}")

        # Информация о книге
        title_label = tk.Label(info_window, text=f"Назва книги: {book.title}", font=("Arial", 14))
        title_label.pack(pady=10)

        author_label = tk.Label(info_window, text=f"Автор: {book.author.name}", font=("Arial", 12))
        author_label.pack(pady=5)

        genre_label = tk.Label(info_window, text=f"Жанр: {book.genre}", font=("Arial", 12))
        genre_label.pack(pady=5)

        rating_label = tk.Label(info_window, text=f"Рейтинг: {book.rating}/5", font=("Arial", 12))
        rating_label.pack(pady=5)

        # Область для відображення зображення
        image_frame = tk.Frame(info_window)
        image_frame.pack(pady=10)
        try:
            # Завантажуємо обкладинку
            book_image = Image.open(book.image_link)

            # Отримуємо розміри контейнера для зображення
            container_width = 200
            container_height = 300

            # Змінюємо розмір зображення з збереженням пропорцій
            book_image.thumbnail((container_width, container_height), Image.Resampling.LANCZOS)

            # Перетворення зображення у формат, який підтримує Tkinter
            book_image = ImageTk.PhotoImage(book_image)

            # Відображаємо зображення
            image_label = tk.Label(image_frame, image=book_image)
            image_label.image = book_image
            image_label.pack()

        except Exception as e:
            tk.Label(image_frame, text="Не вдалося завантажити обкладинку", anchor="center").pack()

        # Текст книги
        text_frame = tk.Frame(info_window)
        text_frame.pack(pady=10)

        text_area = tk.Text(text_frame, width=60, height=15, wrap="word", font=("Arial", 10))
        text_area.pack()

        try:
            with open(book.file_link, 'r', encoding='utf-8') as file:
                text = file.read()
                text_area.insert(tk.END, text)
        except Exception as e:
            text_area.insert(tk.END, f"Помилка при відкритті файлу: {e}")

    def update_book_info(self, book):
        # Обновляем метки с информацией о книге
        self.app.title_label.config(text=f"Назва книги: {book.title}")
        self.app.author_label.config(text=f"Автор: {book.author.name}")
        self.app.genre_label.config(text=f"Жанр: {book.genre}")
        self.app.rating_label.config(text=f"Рейтинг: {book.rating}")

        # Завантаження зображення
        try:
            # Відкриття зображення
            book_image = Image.open(f"{book.image_link}")

            # Отримуємо розміри контейнера для зображення
            container_width = 400  # Ширина контейнера
            container_height = 600  # Висота контейнера

            # Змінюємо розмір зображення з збереженням пропорцій
            book_image.thumbnail((container_width, container_height), Image.Resampling.LANCZOS)

            # Перетворення зображення у формат, який підтримує Tkinter
            book_image = ImageTk.PhotoImage(book_image)

            # Очищаємо canvas і малюємо нове зображення
            self.app.image_canvas.delete("all")
            self.app.image_canvas.create_image(0, 0, anchor="nw", image=book_image)
            self.app.image_canvas.image = book_image  # Зберігаємо посилання на зображення
        except Exception as e:
            self.app.image_canvas.delete("all")
            self.app.image_canvas.create_text(200, 300, text="Не вдалося завантажити обкладинку", anchor="center")

        # Відображення тексту книги
        self.app.text_area.delete(1.0, tk.END)
        try:
            with open(book.file_link, 'r', encoding='utf-8') as file:
                text = file.read()
                self.app.text_area.insert(tk.END, text)
        except Exception as e:
            self.app.text_area.insert(tk.END, f"Помилка при відкритті файлу: {e}")

    def view_authors(self):
        if not self.author_list:
            messagebox.showinfo("Список авторів", "Немає авторів у бібліотеці.")
            return

        # Создаем окно выбора книги
        author_window = tk.Toplevel(self.app.root)
        author_window.geometry("300x400")
        author_window.title("Список авторів")

        tk.Label(author_window, text="Оберіть автора:").pack(pady=10)


        # Добавляем Listbox для отображения авторов
        author_listbox = tk.Listbox(author_window, width=50, height=15)
        author_listbox.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Добавляем авторов в Listbox
        for author in self.author_list:
            author_listbox.insert(tk.END, author.name)

        # Функция для обработки выбора автора
        def on_select_author():
            selected_index = author_listbox.curselection()
            if selected_index:
                selected_author = self.author_list[selected_index[0]]

                # Открываем новое окно с информацией об авторе
                self.show_author_details(selected_author)

            else:
                messagebox.showwarning("Попередження", "Оберіть автора зі списку!")

        # Кнопка "Обрати" для подтверждения выбора
        select_button = tk.Button(author_window, text="Обрати", command=on_select_author)
        select_button.pack(side="bottom", pady=10)

        # Кнопка для закрытия окна
        close_button = tk.Button(author_window, text="Закрити", command=author_window.destroy)
        close_button.pack(side="bottom", pady=5)

    # Метод для отображения информации об авторе
    def show_author_details(self, author):
        # Создаем окно с информацией об авторе
        details_window = tk.Toplevel(self.app.root)
        details_window.title(f"Інформація про автора: {author.name}")
        details_window.geometry("400x300")

        # Отображаем информацию об авторе
        tk.Label(details_window, text=f"Ім'я: {author.name}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        tk.Label(details_window, text=f"Країна: {author.country}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        tk.Label(details_window,
                 text=f"Дата народження: {author.birth_date.strftime('%d.%m.%Y') if author.birth_date else 'Невідомо'}",
                 font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        tk.Label(details_window,
                 text=f"Дата смерті: {author.death_date.strftime('%d.%m.%Y') if author.death_date else 'Живий або невідомо'}",
                 font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        tk.Label(details_window, text=f"Стать: {author.gender}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)

        # Ссылка на биографию (если есть)
        if author.biography_link:
            tk.Label(details_window, text=f"Біографія: {author.biography_link}", font=("Arial", 12), fg="blue",
                     cursor="hand2").pack(anchor="w", padx=10, pady=5)

        # Кнопка для закрытия окна
        close_button = tk.Button(details_window, text="Закрити", command=details_window.destroy)
        close_button.pack(side="bottom", pady=10)
