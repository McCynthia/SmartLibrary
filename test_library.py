import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from library import Library, Personnel, Book, User, BarCode

class TestLibrarySystem(unittest.TestCase):

    def setUp(self):
        # Set up a library, books, users, and personnel for each test
        self.library = Library("Test Library", 3.50)
        self.book1 = Book("1234567890", 5, "1984", "George Orwell")
        self.book2 = Book("0987654321", 2, "Brave New World", "Aldous Huxley")
        self.book3 = Book("567890123456", 1, "Animal Farm", "George Orwell")
        self.book4 = Book("678901234567", 3, "Homage to Catalonia", "George Orwell")
        self.user1 = User("User123", 0, 0.00, self.library)
        self.user2 = User("User456", 1, 3.50, self.library)
        self.employee = Personnel("Employee001", self.library)

        # Add books and users to the library
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        self.library.add_book(self.book3)
        self.library.add_book(self.book4)
        self.library.add_user(self.user1)
        self.library.add_user(self.user2)

    def test_add_book(self):
        # Test if a book is added correctly
        new_book = Book("1111111111", 10, "To Kill a Mockingbird", "Harper Lee")
        self.library.add_book(new_book)
        self.assertIn("1111111111", self.library.books_by_barcode)
        self.assertEqual(self.library.books_by_barcode["1111111111"].title, "To Kill a Mockingbird")

    def test_add_user(self):
        # Test if a user is added correctly
        new_user = User("User789", 0, 0.00, self.library)
        self.library.add_user(new_user)
        self.assertIn("User789", self.library.user_inventory)

    def test_search_by_barcode(self):
        # Test searching for a book by barcode
        result = self.library.search_by_barcode("1234567890")
        self.assertIsInstance(result, Book)
        self.assertEqual(result.title, "1984")

        # Test invalid barcode
        result = self.library.search_by_barcode("0000000000")
        self.assertEqual(result, "Book with barcode: 0000000000 not found in the inventory.\n")

    def test_search_by_author_multiple_books(self):
        # Test searching by an author with multiple books
        result = self.library.search_by_author("George Orwell")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(book.author == "George Orwell" for book in result))

    def test_search_by_author_single_book(self):
        # Test searching by an author with a single book
        result = self.library.search_by_author("Aldous Huxley")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Brave New World")

    def test_search_by_author_no_books(self):
        # Test searching by an author with no books in the library
        result = self.library.search_by_author("Unknown Author")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_search_by_title_multiple_books(self):
        # Test searching by a title keyword that returns multiple books
        result = self.library.search_by_title("198")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "1984")

    def test_search_by_title_single_book(self):
        # Test searching by a title that returns exactly one book
        result = self.library.search_by_title("Brave New World")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Brave New World")

    def test_search_by_title_no_books(self):
        # Test searching by a title that returns no books
        result = self.library.search_by_title("Unknown Title")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_rent_book(self):
        # Test renting a book 
        rented_date = datetime.now()
        result = self.employee.rent_book(self.user1, self.book1, rented_date)
        self.assertIn("Book '1984' rented to User123.", result)
        self.assertEqual(self.book1.book_quantity, 4) 

        # Test renting when user has already rented 3 books
        self.user1.rented_books = 3
        result = self.employee.rent_book(self.user1, self.book1, rented_date)
        self.assertEqual(result, "Can't rent book. The user has rented 3 books.")

    def test_return_book_on_time(self):
        # Test returning a book without any extra charges
        rented_date = datetime.now() - timedelta(days=6)  
        self.employee.rent_book(self.user1, self.book1, rented_date)
        return_date = datetime.now()  
        
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = return_date
            self.employee.return_book(self.user1, self.book1.book_barcode, return_date)

        self.assertEqual(self.user1.billing, 0.00) 
        self.assertEqual(self.book1.book_quantity, 5)  

    def test_return_book_late(self):
        # Test returning a book with late fees
        rented_date = datetime.now() - timedelta(days=10) 
        self.employee.rent_book(self.user1, self.book1, rented_date)
        return_date = datetime.now() 
        
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = return_date
            self.employee.return_book(self.user1, self.book1.book_barcode, return_date)

        # 10 days rented, 7 days allowed, 3 extra days => 3 * 3.50 = 10.50
        self.assertEqual(self.user1.billing, 10.50)
        self.assertEqual(self.book1.book_quantity, 5)  

    def test_seal_book(self):
        # Test sealing a book 
        rented_date = datetime.now()
        self.employee.rent_book(self.user1, self.book1, rented_date)
        self.employee.seal_book(self.book1.book_barcode)
        rental_record = self.library.rental_records[self.book1.book_barcode]
        self.assertTrue(rental_record.seal)  

    def test_user_not_found(self):
        # Test searching for a non-existing user
        result = self.library.search_user("NonExistentUser")
        self.assertEqual(result, "User not found.\n")

    def test_book_not_available(self):
        # Test renting a book with no available copies
        self.book2.book_quantity = 0
        result = self.employee.rent_book(self.user1, self.book2, datetime.now())
        self.assertEqual(result, f"The book: '{self.book2.title}' has no copies left.")

if __name__ == "__main__":
    unittest.main()
