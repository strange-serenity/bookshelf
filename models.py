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
        return f"{self.title} by {self.author.name} - {self.genre} - Rating: {self.rating}/5"
