import unittest
from datetime import datetime, timedelta
from library import Library, User, Book, Personnel, BarCode

class TestLibrarySystem(unittest.TestCase):

    def setUp(self):
        """Setup for all test cases"""
        # Creating a library instance
        self.library = Library("Charlie's Library", 3.50)

        # Creating books and adding them to the library
        self.book1 = Book("93749640957", 1, "The Sun Also Rises", "Ernest Hemingway")
        self.book2 = Book("92036183926", 2, "In Cold Blood", "Truman Capote")
        self.library.add_book(self.book1)
        self.library.add_book(self.book2)

        # Creating users
        self.user1 = User("Nutria123", 0, 0.00, self.library)
        self.user2 = User("Foca891", 0, 0.00, self.library)
        self.user3 = User("Flaco628", 3, 25.00, self.library)
        self.library.add_user(self.user1)
        self.library.add_user(self.user2)
        self.library.add_user(self.user3)

        # Creating an employee
        self.employee = Personnel("John97479", self.library)

    def test_add_book(self):
        new_book = Book("12345678901", 5, "1984", "George Orwell")
        self.library.add_book(new_book)
        self.assertIn(new_book.book_barcode, self.library.books_by_barcode)
        self.assertEqual(self.library.books_by_barcode[new_book.book_barcode], new_book)

    def test_search_by_barcode(self):
        book = self.library.search_by_barcode("93749640957")
        self.assertEqual(book, self.book1)
        
        result = self.library.search_by_barcode("00000000000")
        self.assertEqual(result, "Book with barcode: 00000000000 not found in the inventory.\n")

    def test_search_by_title(self):
        results = self.library.search_by_title("The Sun Also Rises")
        self.assertIn(self.book1, results)
        
        results = self.library.search_by_title("Unknown Book")
        self.assertEqual(results, [])

    def test_search_user(self):
        user = self.library.search_user("Nutria123")
        self.assertEqual(user, self.user1)
        
        result = self.library.search_user("UnknownUser")
        self.assertEqual(result, "User not found.\n")

    def test_rent_book(self):
        rent_date = datetime.now()
        rent_message = self.employee.rent_book(self.user1, self.book1, rent_date)
        self.assertIn("rented", rent_message)
        self.assertEqual(self.user1.rented_books, 1)
        self.assertEqual(self.book1.book_quantity, 0)

    def test_rent_book_limit(self):
        # Test renting a book when the user has reached the rental limit (3)
        rent_date = datetime.now()
        rent_message = self.employee.rent_book(self.user3, self.book2, rent_date)
        self.assertEqual(rent_message, "Can't rent book. The user has already rented 3 books.")

    def test_return_book_on_time(self):
        rent_date = datetime.now()
        self.employee.rent_book(self.user1, self.book1, rent_date)
        return_date = rent_date + timedelta(days=3)
        self.employee.return_book(self.user1, self.book1.book_barcode, return_date)
        self.assertEqual(self.user1.rented_books, 0)
        self.assertEqual(self.book1.book_quantity, 1)

    def test_return_book_overdue(self):
        rent_date = datetime.now()
        self.employee.rent_book(self.user1, self.book1, rent_date)
        return_date = rent_date + timedelta(days=10)
        self.employee.return_book(self.user1, self.book1.book_barcode, return_date)
         # 3 extra days * $3.50 each
        self.assertEqual(self.user1.billing, 10.50) 

    def test_seal_book(self):
        rent_date = datetime.now()
        self.employee.rent_book(self.user1, self.book1, rent_date)
        self.employee.seal_book(self.book1.book_barcode)
        rental_record = self.library.search_rental_record(self.book1.book_barcode, self.user1.user_id)
        self.assertTrue(rental_record.seal)

    def test_make_payment(self):
        self.user1.billing = 20.00
        payment_message = self.user1.make_payment(10.00)
        self.assertEqual(self.user1.billing, 10.00)
        self.assertEqual(payment_message, "Payment of $10.00 received. Remaining balance: $10.00\n")

    def test_make_payment_invalid_amount(self):
        self.user1.billing = 20.00
        payment_message = self.user1.make_payment(0)
        self.assertEqual(payment_message, "Invalid payment amount.\n")

    def test_make_payment_exceeds_balance(self):
        # Test payment exceeding outstanding balance
        self.user1.billing = 20.00
        payment_message = self.user1.make_payment(25.00)
        self.assertEqual(payment_message, "Payment exceeds outstanding balance. \nCurrent balance: $20.00\n")

    def test_return_book_no_rental_record(self):
        rent_date = datetime.now()
        self.employee.rent_book(self.user1, self.book1, rent_date)
        self.employee.return_book(self.user1, "12345678901", rent_date)
        # No rental record should trigger the correct message
        self.assertEqual(self.library.rental_records.get(("12345678901", self.user1.user_id)), None)

    def test_search_by_author(self):
        books_by_hemingway = self.library.search_by_author("Ernest Hemingway")
        self.assertIn(self.book1, books_by_hemingway)

if __name__ == '__main__':
    unittest.main()
