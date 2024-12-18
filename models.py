import json
from datetime import datetime
from typing import Optional


# Клас "Автор"
class Author:
    def __init__(self, name: str, country: str, birth_date: Optional[datetime], death_date: Optional[datetime],
                 gender: str, biography_link: Optional[str]):
        self.name = name
        self.country = country
        self.birth_date = birth_date
        self.death_date = death_date
        self.gender = gender
        self.biography_link = biography_link

    def __str__(self):
        return f"{self.name} ({self.country})"

    # Метод для збереження автора в словник
    def to_dict(self):
        return {
            "name": self.name,
            "country": self.country,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "death_date": self.death_date.isoformat() if self.death_date else None,
            "gender": self.gender,
            "biography_link": self.biography_link
        }

    # Метод для створення об'єкта автора з словника
    @classmethod
    def from_dict(cls, data):
        birth_date = datetime.fromisoformat(data['birth_date']) if data['birth_date'] else None
        death_date = datetime.fromisoformat(data['death_date']) if data['death_date'] else None
        return cls(data['name'], data['country'], birth_date, death_date, data['gender'], data['biography_link'])


# Клас "Книга"
class Book:
    def __init__(self, title: str, author: Author, genre: str, file_link: str, image_link: str, rating: float):
        self.title = title
        self.author = author
        self.genre = genre
        self.file_link = file_link
        self.image_link = image_link
        self.rating = rating

    def __str__(self):
        return f"{self.title} від {self.author.name} - {self.genre} - Рейтинг: {self.rating}/5"

    # Метод для збереження книги в словник
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author.to_dict(),
            "genre": self.genre,
            "file_link": self.file_link,
            "image_link": self.image_link,
            "rating": self.rating
        }

    # Метод для створення об'єкта книги з словника
    @classmethod
    def from_dict(cls, data):
        author = Author.from_dict(data['author'])
        return cls(data['title'], author, data['genre'], data['file_link'], data['image_link'], data['rating'])


# Клас для роботи з бібліотекою
class Library:
    def __init__(self):
        self.books = []

    # Метод для додавання книги
    def add_book(self, book: Book):
        self.books.append(book)

    # Метод для збереження даних у файл
    def save_to_file(self, filename: str):
        with open(filename, 'w', encoding='utf-8') as file:
            data = [book.to_dict() for book in self.books]
            json.dump(data, file, ensure_ascii=False, indent=4)

    # Метод для завантаження даних з файлу
    def load_from_file(self, filename: str):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.books = [Book.from_dict(book_data) for book_data in data]
        except FileNotFoundError:
            print(f"Файл {filename} не знайдено.")
        except json.JSONDecodeError:
            print(f"Помилка при читанні даних з файлу {filename}.")
