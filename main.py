from typing import List, Optional, Tuple
from datetime import datetime

class LibraryItem:
    """Parent class for all library-related objects"""
    def __init__(self, title: str):
        self.title = title

class Book(LibraryItem):
    """Handles individual book data"""
    def __init__(self, title: str, author: str, genre: str, year: int, rating: float, availability: bool, quantity: int):
        super().__init__(title)
        self.author = author
        self.genre = genre
        self.year = year
        self.rating = rating
        self.availability = availability
        self.quantity = quantity
        self.history: List[Tuple[datetime, str, str]] = []
        self._add_to_history("created", "Book added to library")

    def _add_to_history(self, action: str, details: str) -> None:
        self.history.append((datetime.now(), action, details))

    def update_quantity(self, new_quantity: int) -> None:
        old_quantity = self.quantity
        self.quantity = new_quantity
        self.availability = new_quantity > 0
        self._add_to_history("quantity_update", f"Quantity changed from {old_quantity} to {new_quantity}")

    def get_history(self) -> List[Tuple[datetime, str, str]]:
        return self.history

    def __str__(self) -> str:
        return f"'{self.title}' by {self.author} ({self.year}) | Genre: {self.genre} | Rating: {self.rating}/5 | Available: {'Yes' if self.availability else 'No'} | Copies: {self.quantity}"

class BookInventory(LibraryItem):
    """Handles book collection and inventory management"""
    def __init__(self):
        super().__init__("Library Inventory")
        self.books: List[Book] = []

    def add_book(self, book: Book) -> None:
        self.books.append(book)

    def recursive_search_by_title(self, title: str, index: int = 0) -> Optional[Book]:
        """Recursively search for a book by title"""
        if index >= len(self.books):
            return None
        if self.books[index].title.lower() == title.lower():
            return self.books[index]
        return self.recursive_search_by_title(title, index + 1)

    def find_book_by_title(self, title: str) -> Optional[Book]:
        return self.recursive_search_by_title(title)

class BookAnalytics(LibraryItem):
    """Handles book statistics and analysis"""
    def __init__(self, books: List[Book]):
        super().__init__("Library Analytics")
        self.books = books

    def get_highest_rated_book(self) -> Optional[Book]:
        if not self.books:
            print("\n------------------------------------------------------------")
            print("No books available in the library.")
            print("------------------------------------------------------------")
            return None
        return max(self.books, key=lambda x: x.rating)

class BookUI(LibraryItem):
    """Handles user interface and input/output operations"""
    def __init__(self, inventory: BookInventory, analytics: BookAnalytics):
        super().__init__("Library Interface")
        self.inventory = inventory
        self.analytics = analytics

    def print_separator(self, message: str = ""):
        print("\n------------------------------------------------------------")
        if message:
            print(message)
            print("------------------------------------------------------------")

    def add_book_ui(self):
        self.print_separator("Enter the details of the book that you want to add.")
        
        title = input("Title: ").strip()
        author = input("Author's name: ").strip()
        genre = input("Genre: ").strip()

        while True:
            try:
                year = int(input("Year of publication: ").strip())
                if year <= 2025:
                    break
                print("Enter valid year.")
            except ValueError:
                print("Invalid year. Please enter a valid integer.")

        while True:
            try:
                rating = float(input("Rating (between 1 to 5, e.g. 4.6): ").strip())
                if 1.0 <= rating <= 5.0:
                    break
                print("Rating must be between 1 and 5.")
            except ValueError:
                print("Invalid rating. Please enter a decimal number like 4.6.")

        while True:
            availability_input = input("Is any physical copy available in the library? (yes/no): ").strip().lower()
            if availability_input in ['yes', 'no']:
                break
            print("Please type 'yes' or 'no'.")

        quantity = 0
        if availability_input == 'yes':
            availability = True
            while True:
                try:
                    quantity = int(input("How many copies are available: ").strip())
                    if quantity >= 0:
                        break
                    print("Quantity must be 0 or positive.")
                except ValueError:
                    print("Invalid quantity. Please enter a whole number.")
        else:
            availability = False

        book = Book(title, author, genre, year, rating, availability, quantity)
        self.inventory.add_book(book)
        self.print_separator("Book successfully added!")

    def display_all_books(self):
        if not self.inventory.books:
            self.print_separator("No books in the library yet.")
            return

        self.print_separator()
        print("All Books in the Library:")
        for idx, book in enumerate(self.inventory.books, 1):
            print(f"{idx}. {str(book)}")
        print("------------------------------------------------------------")

    def view_book_history(self):
        title = input("\nEnter the title of the book to view history: ").strip()
        book = self.inventory.find_book_by_title(title)
        
        if book:
            self.print_separator(f"History for '{book.title}':")
            for timestamp, action, details in book.get_history():
                print(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {action}: {details}")
        else:
            self.print_separator(f"Book titled '{title}' not found in the library.")

    def update_book_quantity(self):
        title = input("\nEnter the title of the book to update quantity: ").strip()
        book = self.inventory.find_book_by_title(title)
        
        if book:
            print(f"Current quantity: {book.quantity}")
            while True:
                try:
                    new_quantity = int(input("Enter new quantity: ").strip())
                    if new_quantity >= 0:
                        book.update_quantity(new_quantity)
                        self.print_separator("Quantity updated successfully!")
                        break
                    print("Quantity must be 0 or positive.")
                except ValueError:
                    print("Invalid quantity. Please enter a whole number.")
        else:
            self.print_separator(f"Book titled '{title}' not found in the library.")

    def run_library_system(self):
        print("\nWelcome to Library Management System!")

        while True:
            print("\nPlease select an option:")
            print("1. Add a new book to the library")
            print("2. Display all books in the library")
            print("3. Show highest rated book")
            print("4. View book history")
            print("5. Update book quantity")

            while True:
                try:
                    option = int(input("\nEnter 1 to 5: "))
                    if 1 <= option <= 5:
                        break
                    print("Please enter a number between 1 and 5.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            if option == 1:
                while True:
                    self.add_book_ui()
                    again = input("\nWould you like to add another book? Type 'yes' to continue or any other key to exit: ").strip().lower()
                    if again != 'yes':
                        print("\nThank you!")
                        break
            elif option == 2:
                self.display_all_books()
            elif option == 3:
                highest_rated = self.analytics.get_highest_rated_book()
                if highest_rated:
                    self.print_separator(f"Highest Rated Book: '{highest_rated.title}' with ({highest_rated.rating}/5.0)")
            elif option == 4:
                self.view_book_history()
            elif option == 5:
                self.update_book_quantity()
            
            anotherOption = input("\nWould you like to do another task? Type 'yes' to continue or any other key to exit: ").strip().lower()
            if anotherOption != 'yes':
                print("\nThank you for using the Library Management System!")
                break

# Create instances and run the system
inventory = BookInventory()
analytics = BookAnalytics(inventory.books)
ui = BookUI(inventory, analytics)

if __name__ == "__main__":
    ui.run_library_system()
