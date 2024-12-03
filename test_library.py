import unittest
import os
from library import Library, Book


class TestLibrary(unittest.TestCase):
    """
    Класс для тестирования функционала библиотеки.
    """

    def setUp(self):
        """
        Настройка перед каждым тестом.
        Создает временный файл для хранения данных о книгах.
        """
        self.test_file = 'test_books.json'
        self.library = Library(self.test_file)

    def tearDown(self):
        """
        Очистка после каждого теста.
        Удаляет временный файл, если он существует.
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_book(self):
        """
        Тест добавления книги в библиотеку.
        """
        self.library.add_book("Тестовое название", "Тестовый автор", 2023)
        books = self.library.books
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Тестовое название")
        self.assertEqual(books[0].author, "Тестовый автор")
        self.assertEqual(books[0].year, 2023)
        self.assertEqual(books[0].status, "в наличии")

    def test_delete_book(self):
        """
        Тест удаления книги из библиотеки.
        """
        self.library.add_book("Тестовое название", "Тестовый автор", 2023)
        book_id = self.library.books[0].book_id
        message = self.library.delete_book(book_id)
        self.assertEqual(message, f"Книга с ID {book_id} успешно удалена.")
        books = self.library.books
        self.assertEqual(len(books), 0)

    def test_delete_nonexistent_book(self):
        """
        Тест удаления несуществующей книги.
        """
        message = self.library.delete_book(999)
        self.assertEqual(message, "Ошибка: Книга с ID 999 не найдена.")

    def test_search_books(self):
        """
        Тест поиска книг по заданным критериям.
        """
        self.library.add_book("Тестовое название", "Тестовый автор", 2023)
        self.library.add_book("Другое название", "Другой автор", 2022)
        results = self.library.search_books(title="Тестовое название")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Тестовое название")

        results = self.library.search_books(author="Другой автор")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Другой автор")

        results = self.library.search_books(year=2023)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].year, 2023)

    def test_change_book_status(self):
        """
        Тест изменения статуса книги.
        """
        self.library.add_book("Тестовое название", "Тестовый автор", 2023)
        book_id = self.library.books[0].book_id
        self.library.change_book_status(book_id, "выдана")
        book = self.library.books[0]
        self.assertEqual(book.status, "выдана")


if __name__ == '__main__':
    unittest.main()
