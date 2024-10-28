from datetime import datetime, timedelta 


class Library:
    def __init__(self, library_id, extra_days_price):
        self.library_id = library_id
        self.extra_days_price = extra_days_price  # Charge per extra day
        self.books_by_barcode = {}
        self.user_inventory = {}
        self.rental_records = {}  # Maps book barcode to rental information

    def __str__(self):
        return f"Library ID: {self.library_id}, Extra Day Price: ${self.extra_days_price}"

    def add_book(self, book):
        self.books_by_barcode[book.book_barcode] = book

    def add_user(self, user):
        self.user_inventory[user.user_id] = user

    def search_by_barcode(self, barcode):
        if barcode in self.books_by_barcode:
            book = self.books_by_barcode[barcode]
            return book
        return f"Book with barcode: {barcode} not found in the inventory.\n"

    def search_by_title(self, title):
        results = [book for book in self.books_by_barcode.values() if title.lower() in book.title.lower()]
        # Returns empty list if no books are found.
        return results

    def search_by_author(self, author):
        matching_books = [book for book in self.books_by_barcode.values() if book.author.lower() == author.lower()]
        return matching_books

    def search_user(self, user_id):
        if user_id in self.user_inventory:
            return self.user_inventory[user_id]
        return f"User not found.\n"

    def return_book(self, user, barcode, return_date):
        if barcode in self.rental_records:
            record = self.rental_records[barcode]
            rented_days = (return_date - record.rented_date).days  
            book = self.search_by_barcode(barcode)
            
            if rented_days > 7 and not record.seal:
                # Calculate extra days and charge the user
                extra_days = rented_days - 7
                extra_charges = extra_days * self.extra_days_price
                user.billing += extra_charges
                print(f"Book '{book.title}' was overdue by {extra_days} days. Extra charges applied: ${extra_charges:.2f}")
            else:
                print(f"Book '{book.title}' returned on time or was sealed.")
            
            # Update book and user records
            user.rented_books -= 1
            book.book_quantity += 1
            # Remove rental record as the book is returned
            del self.rental_records[barcode]  
        else:
            print(f"No rental record found for book with barcode: {barcode}.\n")

    def seal_book(self, barcode):
        if barcode in self.rental_records:
            record = self.rental_records[barcode]
            # Mark the book as sealed
            record.seal = True  
            print(f"Book with barcode {barcode} has been sealed successfully.")
        else:
            print(f"No rental record found for book with barcode: {barcode}.\n")

class Personnel:
    def __init__(self, employee_id, library):
        self.employee_id = employee_id
        self.library = library  

    def __str__(self):
        return f"Employee ID: {self.employee_id}\n"

    def rent_book(self, user, book, rented_date):
        if user.rented_books >= 3:
            return "Can't rent book. The user has rented 3 books."
        # Checking if the book is currently rented
        if book.book_barcode in user.library.rental_records:
            rental_record = user.library.rental_records[book.book_barcode]
            if rental_record.status == "rented":
                return f"Book '{book.title}' is currently rented. \nExpected return date: {rental_record.due_date.strftime('%m-%d-%Y')}\n"
        # If book is available    
        if user.rented_books < 3 and book.book_quantity > 0:
            book.book_quantity -= 1
            user.rented_books += 1
            user.library.rental_records[book.book_barcode] = BarCode(
                book.book_barcode, rented_date, rented_date + timedelta(days=7), None, 'rented', False
            )
            return f"Book '{book.title}' rented to {user.user_id}. \nCopies left: {book.book_quantity}"
        elif book.book_quantity == 0:
            return f"The book: '{book.title}' has no copies left."
        return "Can't rent book. The user has rented 3 books."

    def return_book(self, user, book_barcode, return_date):
        user.library.return_book(user, book_barcode, return_date)

    def seal_book(self, book_barcode):
        self.library.seal_book(book_barcode) 

class Book:
    def __init__(self, book_barcode, book_quantity, title, author):
        self.book_barcode = book_barcode
        self.book_quantity = book_quantity
        self.title = title
        self.author = author

    def __str__(self):
        return f"Book: {self.title} by {self.author}, Barcode: {self.book_barcode}, Copies: {self.book_quantity}"

class User:
    def __init__(self, user_id, rented_books, billing, library):
        self.user_id = user_id
        self.rented_books = rented_books
        self.billing = billing
        self.library = library
        
    def __str__(self):
        return f"User ID: {self.user_id} has {self.rented_books} rented books and an outstanding charge of ${self.billing:.2f}"

    def make_payment(self, amount):
        if amount <= 0:
            return "Invalid payment amount.\n"
        if amount > self.billing:
            return f"Payment exceeds outstanding balance. \nCurrent balance: ${self.billing:.2f}\n"
        
        self.billing -= amount
        return f"Payment of ${amount:.2f} received. Remaining balance: ${self.billing:.2f}\n"

class BarCode:
    def __init__(self, book_id, rented_date, due_date, return_date, status, seal):
        self.book_id = book_id
        self.rented_date = rented_date
        self.due_date = due_date
        self.return_date = return_date
        self.status = status
        self.seal = seal
        
    def __str__(self):
        return f"Book ID: {self.book_id}, \nRented Date: {self.rented_date}, \nDue Date: {self.due_date}, \nReturn Date: {self.return_date}, \nStatus: {self.status}, \nSeal: {self.seal}"


def main():
    # Instances
    library_a = Library("Charlie's Library", 3.50)

    books = [
        Book("93749640957", 1, "The Sun Also Rises", "Ernest Hemingway"),
        Book("92036183926", 2, "In Cold Blood", "Truman Capote"),
        Book("74829461927", 5, "The Dark Tower", "Stephen King"),
        Book("84628390472", 3, "Dance Dance Dance", "Haruki Murakami"),
        Book("63829374631", 1, "Alice's Adventures in Wonderland", "Lewis Carroll"),
        Book("73857627463", 6, "Misery", "Stephen King"),
        Book("64728193645", 3, "The Old Man and the Sea", "Ernest Hemingway"),
        Book("12719468365", 1, "A Moveable Feast", "Ernest Hemingway"),
        Book("74829485624", 4, "Joyland", "Stephen King"),
        Book("16284657391", 2, "Joyland", "Emily Schultz"),
        Book("17583856593", 4, "Fire and Fury", "Randall Hansen"),
        Book("39104758292", 1, "Fire and Fury", "Michael Wolff")
    ]

    for book in books:
        library_a.add_book(book)

    users = [
        User("Nutria123", 0, 0.00, library_a),
        User("Foca891", 0, 0.00, library_a),
        User("Flaco628", 3, 25.00, library_a)
    ]
    
    for user in users:
        library_a.add_user(user)

    employee_a = Personnel("John97479", library_a) 

    exit = False
    while not exit:
        print("\n1. Add Book")
        print("2. Add new User")
        print("3. Search and Rent a Book")
        print("4. Return a Book")
        print("5. Seal a Book")
        print("6. Make a Payment")
        print("7. Exit\n")

        option = input("Select an option: ")
        if option == "1":
            while True:
                book_barcode = input("\nEnter book barcode: ")
                if book_barcode.isdigit() and len(book_barcode) == 12:
                    break
                else:
                    print("Invalid barcode. Please enter exactly 12 digits.\n")
            book_quantity = int(input("Enter quantity of books: "))
            title = input("Enter book title: ").title()
            author = input("Enter author's name: ").title()
            new_book = Book(book_barcode, book_quantity, title, author)
            library_a.add_book(new_book)
            print(f"\nBook '{title}' by {author} with {book_quantity} copies has been added to the library.\n")

        elif option == "2":
            user_id = input("Enter user ID: ")
            new_user = User(user_id, rented_books=0, billing=0.00, library=library_a)
            library_a.add_user(new_user)
            print(f"User '{user_id}' has been added to the library with 0 books and a billing of $0.00.\n")

        elif option == "3":
            rent_user_id = input("Enter user ID: ")
            user = library_a.search_user(rent_user_id)
            if isinstance(user, User):
                if user.rented_books >= 3:
                    print(f"User: '{user.user_id}' has already rented 3 books.\n")
                    continue
                search_choice = input("Search by (1) Barcode, (2) Title, (3) Author: ")
                if search_choice == "1":
                    rent_barcode = input("Enter book barcode: ")
                    book = library_a.search_by_barcode(rent_barcode)
                    books = [book] if isinstance(book, Book) else []
                elif search_choice == "2":
                    rent_title = input("Enter book title: ")
                    books = library_a.search_by_title(rent_title)
                elif search_choice == "3":
                    rent_author = input("Enter book author: ")
                    books = library_a.search_by_author(rent_author)
                else:
                    print("Invalid choice.")
                    continue
                if books:
                    # Display all found books with an index number
                    print("\nBooks found:")
                    for idx, book in enumerate(books, start=1):
                        print(f"{idx}. '{book.title}' by {book.author} - Copies left: {book.book_quantity}")
                    while True:
                        # Ask the user to select a book by entering its index number
                        try:
                            book_choice = int(input("\nEnter the number of the book you want to rent (0 to cancel): "))
                            if book_choice == 0:
                                print("Cancelled.\n")
                                break
                            elif 1 <= book_choice <= len(books):
                                selected_book = books[book_choice - 1]
                                
                                # Attempt to rent the selected book
                                rented_date = datetime.now()
                                rental_message = employee_a.rent_book(user, selected_book, rented_date)
                                print(rental_message)
                                # Exit after renting or showing rental info
                                break  
                            else:
                                print("Invalid choice. Please select a valid book number.")
                        except ValueError:
                            print("Please enter a valid number.")
                else:
                    print("No books found matching your search.\n")
            else:
                print(user)

        elif option == "4":
            return_user_id = input("Enter user ID: ")
            user = library_a.search_user(return_user_id)
            if isinstance(user, User):
                return_barcode = input("Enter book barcode: ")
                return_date = datetime.now()
                employee_a.return_book(user, return_barcode, return_date)
            else:
                print(user)

        elif option == "5":
            seal_barcode = input("Enter book barcode to seal: ")
            employee_a.seal_book(seal_barcode)

        elif option == "6":
            pay_user_id = input("Enter user ID: ")
            user = library_a.search_user(pay_user_id)
            if isinstance(user, User):
                print(f"Current outstanding balance: ${user.billing:.2f}\n")
                while True:
                    try: 
                        payment_amount = float(input("Enter payment amount: "))
                        payment_message = user.make_payment(payment_amount)
                        print(payment_message)
                        break
                    except ValueError:
                        print("Invalid input. Enter a valid number.")
            else:
                print(user)

        elif option == "7":
            break
        else:
            print("You chose ", option)

if __name__ == "__main__":
    main()
