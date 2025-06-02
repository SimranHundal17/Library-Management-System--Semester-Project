from typing import List, Optional, Tuple
from datetime import datetime
from abc import ABC, abstractmethod  # Import for abstract base class

class LibraryItem:
    """Parent class for all library-related objects"""
    def __init__(self, title: str):
        self.title = title

class BookOperation(ABC):
    """Abstract base class for book operations like lending and returning"""
    
    @abstractmethod
    def can_perform(self, book: 'Book') -> bool:
        """Check if operation can be performed on the book"""
        pass
        
    @abstractmethod
    def execute(self, book: 'Book') -> bool:
        """Perform the operation on the book"""
        pass

class LendOperation(BookOperation):
    """Concrete implementation for lending books"""
    
    def can_perform(self, book: 'Book') -> bool:
        return book.availability and book.quantity > 0
        
    def execute(self, book: 'Book') -> bool:
        if self.can_perform(book):
            book.quantity -= 1
            book.availability = book.quantity > 0
            book._add_to_history("lend", "Book was lent out")
            return True
        return False

class ReturnOperation(BookOperation):
    """Concrete implementation for returning books"""
    
    def can_perform(self, book: 'Book') -> bool:
        return True  # Books can always be returned
        
    def execute(self, book: 'Book') -> bool:
        book.quantity += 1
        book.availability = True
        book._add_to_history("return", "Book was returned")
        return True

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
        # Add operations
        self.lend_operation = LendOperation()
        self.return_operation = ReturnOperation()

    def _add_to_history(self, action: str, details: str) -> None:
        self.history.append((datetime.now(), action, details))

    def update_quantity(self, new_quantity: int) -> None:
        old_quantity = self.quantity
        self.quantity = new_quantity
        self.availability = new_quantity > 0
        self._add_to_history("quantity_update", f"Quantity changed from {old_quantity} to {new_quantity}")

    def get_history(self) -> List[Tuple[datetime, str, str]]:
        return self.history

    def lend(self) -> bool:
        """Attempt to lend the book using LendOperation"""
        return self.lend_operation.execute(self)

    def return_book(self) -> bool:
        """Return the book using ReturnOperation"""
        return self.return_operation.execute(self)

    def __str__(self) -> str:
        return f"'{self.title}' by {self.author} ({self.year}) | Genre: {self.genre} | Rating: {self.rating}/5 | Available: {'Yes' if self.availability else 'No'} | Copies: {self.quantity}"

class BookInventory(LibraryItem):
    """Handles book collection and inventory management"""
    def __init__(self):
        super().__init__("Library Inventory")
        self.books: List[Book] = []

    def add_book(self, book: Book) -> None:
        self.books.append(book)

    def custom_binary_search(self, target_rating: float, target_year: int) -> List[Book]:
        """Custom binary search that finds books based on rating AND year criteria.
        Uses binary search with rating as primary key, then evaluates year condition.
        Returns books where:
        1. Book rating is equal to target_rating AND
        2. Book year is greater than or equal to target_year
        
        This is a custom implementation that:
        - Uses binary search pattern but with multiple criteria
        - Implements logical AND in the evaluation
        - Works on sorted and unsorted portions of data
        - Handles duplicate ratings
        """
        # First sort books by rating (primary search key)
        sorted_books = sorted(self.books, key=lambda x: x.rating)
        results = []
        
        def binary_search_with_criteria(books: List[Book], left: int, right: int) -> None:
            """Recursive binary search that also checks year criteria"""
            if left > right:
                return
            
            mid = (left + right) // 2
            current_book = books[mid]
            
            # Complex logical expression evaluation:
            # 1. Check if rating matches (primary condition)
            # 2. If rating matches, check year condition
            if current_book.rating == target_rating:
                # When we find a rating match, we need to:
                # a) Check if it meets the year condition
                # b) Look for more matches in both directions
                
                # Check current book against all criteria
                if current_book.year >= target_year:
                    results.append(current_book)
                
                # Look for more matches to the left
                # This handles cases where same rating appears multiple times
                temp_left = mid - 1
                while temp_left >= 0 and books[temp_left].rating == target_rating:
                    if books[temp_left].year >= target_year:
                        results.append(books[temp_left])
                    temp_left -= 1
                
                # Look for more matches to the right
                temp_right = mid + 1
                while temp_right <= right and books[temp_right].rating == target_rating:
                    if books[temp_right].year >= target_year:
                        results.append(books[temp_right])
                    temp_right += 1
                
                # Continue searching in both halves for any other matches
                binary_search_with_criteria(books, left, temp_left)
                binary_search_with_criteria(books, temp_right, right)
                
            elif current_book.rating < target_rating:
                # Search in right half if current rating is less than target
                binary_search_with_criteria(books, mid + 1, right)
            else:
                # Search in left half if current rating is greater than target
                binary_search_with_criteria(books, left, mid - 1)
        
        # Start the recursive search
        binary_search_with_criteria(sorted_books, 0, len(sorted_books) - 1)
        return results

    def recursive_search_by_title(self, title: str, index: int = 0) -> Optional[Book]:
        """Recursively search for a book by title"""
        if index >= len(self.books):
            return None
        if self.books[index].title.lower() == title.lower():
            return self.books[index]
        return self.recursive_search_by_title(title, index + 1)

    def find_book_by_title(self, title: str) -> Optional[Book]:
        return self.recursive_search_by_title(title)

class SortStrategy(ABC):
    """Abstract base class for different sorting strategies"""
    
    @abstractmethod
    def sort(self, books: List['Book']) -> List['Book']:
        """Sort the books according to the strategy"""
        pass

class BubbleRatingSort(SortStrategy):
    """Concrete bubble sort strategy for sorting by rating"""
    
    def sort(self, books: List['Book']) -> List['Book']:
        books_to_sort = books.copy()
        n = len(books_to_sort)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                if books_to_sort[j].rating < books_to_sort[j + 1].rating:
                    books_to_sort[j], books_to_sort[j + 1] = books_to_sort[j + 1], books_to_sort[j]
                    
        return books_to_sort

class MergeTitleSort(SortStrategy):
    """Concrete merge sort strategy for sorting by title"""
    
    def sort(self, books: List['Book']) -> List['Book']:
        if len(books) <= 1:
            return books.copy()
            
        mid = len(books) // 2
        left_half = self.sort(books[:mid])
        right_half = self.sort(books[mid:])
        
        return self._merge(left_half, right_half)
    
    def _merge(self, left: List['Book'], right: List['Book']) -> List['Book']:
        merged = []
        left_index = right_index = 0
        
        while left_index < len(left) and right_index < len(right):
            if left[left_index].title.lower() <= right[right_index].title.lower():
                merged.append(left[left_index])
                left_index += 1
            else:
                merged.append(right[right_index])
                right_index += 1
                
        merged.extend(left[left_index:])
        merged.extend(right[right_index:])
        return merged

class MergeYearSort(SortStrategy):
    """Concrete merge sort strategy for sorting by year"""
    
    def sort(self, books: List['Book']) -> List['Book']:
        if len(books) <= 1:
            return books.copy()
            
        mid = len(books) // 2
        left_half = self.sort(books[:mid])
        right_half = self.sort(books[mid:])
        
        return self._merge(left_half, right_half)
    
    def _merge(self, left: List['Book'], right: List['Book']) -> List['Book']:
        merged = []
        left_index = right_index = 0
        
        while left_index < len(left) and right_index < len(right):
            if left[left_index].year >= right[right_index].year:  # Descending order
                merged.append(left[left_index])
                left_index += 1
            else:
                merged.append(right[right_index])
                right_index += 1
                
        merged.extend(left[left_index:])
        merged.extend(right[right_index:])
        return merged

class BookAnalytics(LibraryItem):
    """Handles book statistics and analysis"""
    def __init__(self, books: List[Book]):
        super().__init__("Library Analytics")
        self.books = books
        # Initialize sorting strategies
        self.rating_sort = BubbleRatingSort()
        self.title_sort = MergeTitleSort()
        self.year_sort = MergeYearSort()

    def get_highest_rated_books(self) -> List[Book]:
        """Returns all books that share the highest rating"""
        if not self.books:
            return []
        
        highest_rating = max(book.rating for book in self.books)
        highest_rated_books = [book for book in self.books if book.rating == highest_rating]
        return highest_rated_books

    def sort_books(self, strategy: SortStrategy) -> List[Book]:
        """Polymorphic method to sort books using different strategies"""
        return strategy.sort(self.books)

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

    def display_sorted_books(self):
        if not self.inventory.books:
            self.print_separator("No books in the library yet.")
            return

        print("\nSort books by:")
        print("1. Rating (Bubble Sort)")
        print("2. Title (Merge Sort)")
        print("3. Year (Merge Sort)")
        
        while True:
            try:
                choice = int(input("\nEnter your choice (1-3): "))
                if 1 <= choice <= 3:
                    break
                print("Please enter a number between 1 and 3.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Use polymorphism to select sorting strategy
        if choice == 1:
            sorted_books = self.analytics.sort_books(self.analytics.rating_sort)
            self.print_separator("Books sorted by rating (highest to lowest):")
        elif choice == 2:
            sorted_books = self.analytics.sort_books(self.analytics.title_sort)
            self.print_separator("Books sorted by title (A to Z):")
        else:
            sorted_books = self.analytics.sort_books(self.analytics.year_sort)
            self.print_separator("Books sorted by year (newest to oldest):")

        for idx, book in enumerate(sorted_books, 1):
            print(f"{idx}. {str(book)}")
        print("------------------------------------------------------------")

    def custom_search_ui(self):
        """UI for the custom binary search feature"""
        self.print_separator("Custom Binary Search")
        
        # Get rating to search for
        while True:
            try:
                target_rating = float(input("Enter the rating to search for (1-5): "))
                if 1 <= target_rating <= 5:
                    break
                print("Rating must be between 1 and 5.")
            except ValueError:
                print("Please enter a valid number.")

        # Get minimum year
        while True:
            try:
                target_year = int(input("Enter the minimum year to search for: "))
                if 1000 <= target_year <= 2024:
                    break
                print("Year must be between 1000 and 2024.")
            except ValueError:
                print("Please enter a valid year.")

        # Perform search
        results = self.inventory.custom_binary_search(target_rating, target_year)

        # Display results
        if results:
            self.print_separator(f"Found {len(results)} book(s) matching criteria:")
            print(f"Rating: {target_rating}, Year >= {target_year}")
            for idx, book in enumerate(results, 1):
                print(f"{idx}. {str(book)}")
        else:
            self.print_separator("No books found matching your criteria.")

    def lend_book_ui(self):
        """UI for lending books"""
        self.print_separator("Lend a Book")
        title = input("Enter the title of the book to lend: ").strip()
        book = self.inventory.find_book_by_title(title)
        
        if book:
            if book.lend():
                self.print_separator(f"Successfully lent out: {book.title}")
            else:
                self.print_separator(f"Cannot lend: {book.title} - No copies available")
        else:
            self.print_separator(f"Book not found: {title}")

    def return_book_ui(self):
        """UI for returning books"""
        self.print_separator("Return a Book")
        title = input("Enter the title of the book to return: ").strip()
        book = self.inventory.find_book_by_title(title)
        
        if book:
            if book.return_book():
                self.print_separator(f"Successfully returned: {book.title}")
            else:
                self.print_separator(f"Error returning: {book.title}")
        else:
            self.print_separator(f"Book not found: {title}")

    def run_library_system(self):
        print("\nWelcome to Library Management System!")

        while True:
            print("\nPlease select an option:")
            print("1. Add a new book to the library")
            print("2. Display all books in the library")
            print("3. Show highest rated books")
            print("4. View book history")
            print("5. Update book quantity")
            print("6. Sort and display books")
            print("7. Custom binary search")
            print("8. Lend a book")
            print("9. Return a book")

            while True:
                try:
                    option = int(input("\nEnter 1 to 9: "))
                    if 1 <= option <= 9:
                        break
                    print("Please enter a number between 1 and 9.")
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
                highest_rated_books = self.analytics.get_highest_rated_books()
                if highest_rated_books:
                    self.print_separator(f"Highest Rated Books (Rating: {highest_rated_books[0].rating}/5.0):")
                    for idx, book in enumerate(highest_rated_books, 1):
                        print(f"{idx}. {book.title} by {book.author}")
                else:
                    self.print_separator("No books available in the library.")
            elif option == 4:
                self.view_book_history()
            elif option == 5:
                self.update_book_quantity()
            elif option == 6:
                self.display_sorted_books()
            elif option == 7:
                self.custom_search_ui()
            elif option == 8:
                self.lend_book_ui()
            elif option == 9:
                self.return_book_ui()
            
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
