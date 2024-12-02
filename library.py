import json
import os
from typing import List, Dict, Optional


class Book:
    def __init__(
        self,
        book_id: int,
        title: str,
        author: str,
        year: int,
        status: str = "в наличии",
    ):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict[str, any]:
        return {
            "id": self.book_id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: Dict[str, any]) -> "Book":
        return Book(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data["status"],
        )


class Library:
    def __init__(self, file_path: str = "books.json"):
        self.file_path = file_path
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding='utf-8') as file:
                data = json.load(file)
                self.books = [Book.from_dict(book) for book in data]

    def save_books(self) -> None:
        with open(self.file_path, "w", encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, indent=4)

    def add_book(self, title: str, author: str, year: int) -> None:
        book_id = len(self.books) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_books()

    def delete_book(self, book_id: int) -> None:
        self.books = [book for book in self.books if book.book_id != book_id]
        self.save_books()

    def search_books(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[int] = None,
    ) -> List[Book]:
        results = self.books
        if title:
            results = [book for book in results if title.lower() in book.title.lower()]
        if author:
            results = [
                book for book in results if author.lower() in book.author.lower()
            ]
        if year:
            results = [book for book in results if book.year == year]
        return results

    def display_books(self) -> None:
        for book in self.books:
            print(
                f"ID: {book.book_id}, Заголовок: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}"
            )

    def change_book_status(self, book_id: int, new_status: str) -> None:
        for book in self.books:
            if book.book_id == book_id:
                book.status = new_status
                self.save_books()
                break


def main():
    library = Library()

    while True:
        print("\nСистема управления библиотекой")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменение статуса книги")
        print("6. Выход")

        choice = input("Выберите вариант: ")

        if choice == "1":
            title = input("Введите заголовок: ")
            author = input("Введите имя автора: ")
            year = int(input("Введите год: "))
            library.add_book(title, author, year)
            print("Книга успешно добавлена.")

        elif choice == "2":
            book_id = int(input("Введите ID книги для удаления: "))
            library.delete_book(book_id)
            print("Книга успешно удалена.")

        elif choice == "3":
            title = input("Введите заголовок (или оставьте пустым): ")
            author = input("Введите имя автора (или оставьте пустым): ")
            year = input("Введите год (или оставьте пустым): ")
            year = int(year) if year else None
            results = library.search_books(title, author, year)
            for book in results:
                print(
                    f"ID: {book.book_id}, Заголовок: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}"
                )

        elif choice == "4":
            library.display_books()

        elif choice == "5":
            book_id = int(input("Введите ID книги для изменения статуса: "))
            new_status = input("Укажите новый статус ('в наличии' or 'выдана'): ")
            library.change_book_status(book_id, new_status)
            print("Статус успешно обновлен.")

        elif choice == "6":
            break

        else:
            print("Неизвестный выбор. Попробуйте еще раз.")


if __name__ == "__main__":
    main()
