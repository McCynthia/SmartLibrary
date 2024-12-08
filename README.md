```markdown
# Library Management System

A Python-based library management system designed to streamline book rentals, returns, overdue charge calculations, and user account management. This project demonstrates Object-Oriented Programming (OOP) principles, data handling, and practical problem-solving skills.

## Features

- **Book Inventory Management:** Add, search, and seal books by barcode, title, or author.
- **User Account Management:** Add users, track their rented books, and manage billing.
- **Rental System:** Rent books with automated tracking of due dates and overdue charges.
- **Billing and Payments:** Calculate overdue fees, apply charges, and handle payments.
- **Sealed Book Handling:** Mark books as sealed to exempt them from overdue charges.

## Key Concepts Demonstrated

- **Object-Oriented Programming (OOP)**: Classes for `Library`, `Book`, `User`, `Personnel`, and more, showcasing encapsulation and modularity.
- **Data Handling**: Dynamic inventory and user tracking using dictionaries and lists.
- **Error Handling**: Robust input validation and user-friendly error messages.
- **Datetime Operations**: Automated due date calculations and overdue charge handling.

## Prerequisites

- Python 3.7 or later
- Basic understanding of Python and OOP concepts

## Installation

1. Clone the repository:
   `git clone https://github.com/yourusername/library-management-system.git`
2. Navigate to the project directory:
   `cd library-management-system`
3. Run the program:
   `python main.py`

## Usage

Upon running the program, you'll interact with a menu-driven interface to:
1. Add books or users.
2. Search for books by title, author, or barcode.
3. Rent, return, or seal books.
4. Manage user payments and view their account details.

## File Structure

- `main.py`: The main script that includes the program logic and menu-driven interface.
- `library.py`: Contains the `Library` class and related functionalities.
- `user.py`: Defines the `User` class for user account management.
- `book.py`: Contains the `Book` class for managing book details.
- `personnel.py`: Defines the `Personnel` class for employee functionalities.

## Future Enhancements

- Database integration for persistent storage.
- Web-based interface for easier access.
- Advanced search filters (e.g., by genre or publication year).
