from typing import List, Optional, Tuple
from datetime import datetime
from abc import ABC, abstractmethod
import pandas as pd
import os

#=============================================================================
# Utility Functions
#=============================================================================

def print_formatted_separator(message: str = "") -> None:
    """Creates a formatted box-style separator with an optional centered message.
    
    The separator automatically adjusts its width based on the message length
    while maintaining a minimum width of 50 characters for consistency.
    
    Args:
        message: Text to display in the separator. If empty, draws a simple line.
    
    Example:
        +================================================+
        |                   Your Message                   |
        +================================================+
    """
    min_width = 50  # Ensures consistent minimum width for aesthetics
    
    try:
        if message:
            width = max(min_width, len(message) + 4)
            print("\n+" + "=" * (width-2) + "+")
            print("|" + message.center(width-2) + "|")
            print("+" + "=" * (width-2) + "+\n")
        else:
            print("\n+" + "=" * (min_width-2) + "+\n")
    except Exception:
        print("\n" + "=" * min_width + "\n")  # Fallback for unexpected errors

def generate_test_books(size: int) -> List['Book']:
    """Generate test books for performance testing."""
    test_books = []
    for i in range(size):
        book = Book(
            f"Book {i}",
            f"Author {i}",
            "Fiction",
            2000 + (i % 24),
            round(1 + (i % 40) / 10, 1),
            True,
            1
        )
        test_books.append(book)
    return test_books

def create_bar_graph(value1: float, value2: float, label1: str = "Value 1", label2: str = "Value 2") -> str:
    """Create a simple visual comparison of two values using bar graphs."""
    max_width = 30  # Fixed width for simplicity
    
    # Calculate the bars
    max_value = max(value1, value2)
    bar1 = int((value1 / max_value) * max_width) if max_value > 0 else 0
    bar2 = int((value2 / max_value) * max_width) if max_value > 0 else 0
    
    # Create the visualization
    graph = f"\n{label1}: {value1:.6f}s\n"
    graph += "█" * bar1
    graph += f"\n\n{label2}: {value2:.6f}s\n"
    graph += "█" * bar2
    
    return graph

#=============================================================================
# Base Classes
#=============================================================================

class LibraryItem:
    """Base class for all library-related objects."""
    def __init__(self, title: str):
        self.title = title

class BookOperation(ABC):
    """Abstract base class for book operations like lending and returning."""
    
    @abstractmethod
    def can_perform(self, book: 'Book') -> bool:
        """Check if operation can be performed on the book."""
        pass
        
    @abstractmethod
    def execute(self, book: 'Book') -> bool:
        """Perform the operation on the book."""
        pass

#=============================================================================
# Book Operations
#=============================================================================

class LendOperation(BookOperation):
    """Handles book lending operations."""
    
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
    """Handles book return operations."""
    
    def can_perform(self, book: 'Book') -> bool:
        return True  # Books can always be returned
        
    def execute(self, book: 'Book') -> bool:
        book.quantity += 1
        book.availability = True
        book._add_to_history("return", "Book was returned")
        return True

#=============================================================================
# Core Book Management
#=============================================================================

class Book(LibraryItem):
    """Represents a book in the library system with all its attributes and operations."""
    
    def __init__(self, title: str, author: str, genre: str, year: int, 
                 rating: float, availability: bool, quantity: int):
        try:
            super().__init__(title)
            current_year = datetime.now().year
            if not isinstance(year, int) or year < 1500 or year > current_year:
                raise ValueError(f"Year must be between 1500 and {current_year}")
            if not isinstance(rating, (int, float)) or not 1 <= rating <= 5:
                raise ValueError("Rating must be between 1 and 5")
            if not isinstance(quantity, int) or quantity < 0:
                raise ValueError("Quantity must be a non-negative number")
            
            self.author = author
            self.genre = genre
            self.year = year
            self.rating = float(rating)
            self.availability = availability
            self.quantity = quantity
            self.history: List[Tuple[datetime, str, str]] = []
            self.inventory = None
            self._add_to_history("created", "Book added to library")
            self.lend_operation = LendOperation()
            self.return_operation = ReturnOperation()
        except Exception as e:
            raise ValueError(f"Error creating book: {str(e)}")

    def _add_to_history(self, action: str, details: str) -> None:
        self.history.append((datetime.now(), action, details))

    def update_quantity(self, new_quantity: int) -> None:
        old_quantity = self.quantity
        self.quantity = new_quantity
        self.availability = new_quantity > 0
        self._add_to_history("quantity_update", f"Quantity changed from {old_quantity} to {new_quantity}")
        if hasattr(self, 'inventory'):
            self.inventory._save_database()

    def get_history(self) -> List[Tuple[datetime, str, str]]:
        return self.history

    def lend(self) -> bool:
        try:
            success = self.lend_operation.execute(self)
            if success and hasattr(self, 'inventory'):
                self.inventory._save_database()
            return success
        except Exception as e:
            print(f"Error lending book: {str(e)}")
            return False

    def return_book(self) -> bool:
        try:
            success = self.return_operation.execute(self)
            if success and hasattr(self, 'inventory'):
                self.inventory._save_database()
            return success
        except Exception as e:
            print(f"Error returning book: {str(e)}")
            return False

    def __str__(self) -> str:
        return f"'{self.title}' by {self.author} ({self.year}) | Genre: {self.genre} | Rating: {self.rating}/5 | Available: {'Yes' if self.availability else 'No'} | Copies: {self.quantity}"

#=============================================================================
# Sorting Strategies
#=============================================================================

class SortStrategy(ABC):
    """Abstract base class for different sorting strategies."""
    
    @abstractmethod
    def sort(self, books: List['Book']) -> List['Book']:
        """Sort the books according to the strategy."""
        pass

class BubbleRatingSort(SortStrategy):
    """Bubble sort implementation for sorting by rating."""
    
    def sort(self, books: List['Book']) -> List['Book']:
        books_to_sort = books.copy()
        n = len(books_to_sort)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                if books_to_sort[j].rating < books_to_sort[j + 1].rating:
                    books_to_sort[j], books_to_sort[j + 1] = books_to_sort[j + 1], books_to_sort[j]
                    
        return books_to_sort

class MergeTitleSort(SortStrategy):
    """Merge sort implementation for sorting by title."""
    
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
    """Merge sort implementation for sorting by year."""
    
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
            if left[left_index].year >= right[right_index].year:
                merged.append(left[left_index])
                left_index += 1
            else:
                merged.append(right[right_index])
                right_index += 1
                
        merged.extend(left[left_index:])
        merged.extend(right[right_index:])
        return merged

#=============================================================================
# Book Management and Analytics
#=============================================================================

class BookInventory(LibraryItem):
    """Manages the collection of books and database operations."""
    
    def __init__(self):
        super().__init__("Library Inventory")
        self.books: List[Book] = []
        self.database_file = "library_database.csv"
        self._load_database()

    def _load_database(self):
        """Load books from CSV if it exists"""
        try:
            if os.path.exists(self.database_file):
                df = pd.read_csv(self.database_file)
                for _, row in df.iterrows():
                    try:
                        book = Book(
                            title=str(row['title']),
                            author=str(row['author']),
                            genre=str(row['genre']),
                            year=int(row['year']),
                            rating=float(row['rating']),
                            availability=bool(row['availability']),
                            quantity=int(row['quantity'])
                        )
                        book.inventory = self
                        self.books.append(book)
                    except Exception as e:
                        print(f"Skipping invalid book in CSV: {str(e)}")
                print(f"Loaded {len(self.books)} books from database.")
        except Exception as e:
            print(f"Could not load database: {str(e)}")
            self.books = []

    def _save_database(self):
        """Save current books to CSV"""
        try:
            books_data = []
            for book in self.books:
                books_data.append({
                    'title': book.title,
                    'author': book.author,
                    'genre': book.genre,
                    'year': book.year,
                    'rating': book.rating,
                    'availability': book.availability,
                    'quantity': book.quantity
                })
            df = pd.DataFrame(books_data)
            df.to_csv(self.database_file, index=False)
        except Exception as e:
            print(f"Could not save to database: {str(e)}")

    def add_book(self, book: Book) -> None:
        book.inventory = self  # Set inventory reference for the book
        self.books.append(book)
        self._save_database()  # Save after adding a book

    def remove_book(self, title: str) -> bool:
        """Remove a book from inventory and update the database"""
        try:
            book = self.find_book_by_title(title)
            if book:
                self.books.remove(book)
                self._save_database()  # Save changes to CSV
                return True
            return False
        except Exception as e:
            print(f"Error removing book: {str(e)}")
            return False

    def update_book(self, book: Book) -> None:
        """Update book and save changes"""
        if book in self.books:
            self._save_database()  # Save after any book update

    def update_book_quantity(self, book_id: int, new_quantity: int) -> bool:
        if 0 <= book_id < len(self.books):
            self.books[book_id].update_quantity(new_quantity)
            self._save_database()  # Save after updating quantity
            return True
        return False

    def practical_truth_table_search(self, genre: str, for_students: bool, borrowing_type: str) -> List[Tuple[Book, bool, bool]]:
        """
        A practical truth table-based search using real library criteria.
        
        Truth Table Variables:
        G: Genre matches (Fiction/Non-fiction/etc.)
        S: Student-friendly (Rating ≥ 4.0 AND Year ≥ 2000)
        B: Book's borrowing status:
           - 'borrow': Available for checkout (quantity > 0)
           - 'reference': In-library use only
           - 'any': Either borrowing or reference is acceptable
        
        Truth Table for Complex Search:
        G | S | B=borrow | B=reference | for_students | borrowing_type | Result
        -----------------------------------------------------------------
        1 | 1 | 1 | 0 | 1 | borrow    | 1  # Student book available for checkout
        1 | 1 | 0 | 1 | 1 | reference | 1  # Student book for in-library use
        1 | 1 | 1 | 0 | 1 | any       | 1  # Student book, any access type
        1 | 1 | 0 | 1 | 1 | any       | 1  # Student book, any access type
        1 | 0 | 1 | 0 | 0 | borrow    | 1  # General book for checkout
        1 | 0 | 0 | 1 | 0 | reference | 1  # General book for reference
        1 | 0 | - | - | 0 | any       | 1  # General book, any access type
        0 | - | - | - | - | -         | 0  # Wrong genre, automatic reject
        
        Args:
            genre: Desired genre (case-insensitive)
            for_students: Whether book needs to be student-friendly
            borrowing_type: Type of access needed ('borrow', 'reference', or 'any')
            
        Returns:
            List of books matching the criteria with practical library needs
        """
        results = []
        
        for book in self.books:
            # Evaluate each practical condition
            G = book.genre.lower() == genre.lower()  # Genre match
            S = book.rating >= 4.0 and book.year >= 2000  # Student-friendly
            
            # Determine borrowing status
            is_borrowable = book.availability and book.quantity > 0
            is_reference = not is_borrowable and book.quantity == 0  # Reference-only books
            
            # If genre doesn't match, skip immediately
            if not G:
                continue
                
            # For student requests, ensure rating and year requirements
            if for_students and not S:
                continue
                
            # Check borrowing requirements based on type
            if borrowing_type == 'borrow' and not is_borrowable:
                continue
            elif borrowing_type == 'reference' and not is_reference:
                continue
            # For 'any', we accept either borrowable or reference books
            
            # If we get here, book matches all requirements
            results.append((book, is_borrowable, is_reference))
        
        return results

    def custom_binary_search(self, target_rating: float, target_year: int) -> List[Book]:
        """Custom binary search that finds books based on rating AND year criteria"""
        try:
            if not self.books:
                print("Library is empty. No books to search.")
                return []
                
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
        except Exception as e:
            print(f"Error during search: {str(e)}")
            return []

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
    """Handles book statistics and analysis."""
    
    def __init__(self, books: List[Book]):
        super().__init__("Library Analytics")
        self.books = books
        self.rating_sort = BubbleRatingSort()
        self.title_sort = MergeTitleSort()
        self.year_sort = MergeYearSort()

    def print_formatted_separator(self, message: str = "") -> None:
        """Creates a formatted separator with an optional message."""
        print_formatted_separator(message)

    def compare_sorting_algorithms(self):
        """Compare performance of sorting algorithms using test data."""
        try:
            self.print_formatted_separator("Sorting Algorithm Performance")
            
            # Generate test dataset
            test_size = 100  # reasonable size for testing
            test_books = generate_test_books(test_size)
            print(f"Testing with {test_size} books\n")
            
            # Test Bubble Sort
            start_time = datetime.now()
            self.rating_sort.sort(test_books)
            bubble_duration = (datetime.now() - start_time).total_seconds()
            
            # Test Merge Sort
            start_time = datetime.now()
            self.title_sort.sort(test_books)
            merge_duration = (datetime.now() - start_time).total_seconds()
            
            # Display results with visual comparison
            print(create_bar_graph(
                bubble_duration, 
                merge_duration,
                "Bubble Sort",
                "Merge Sort"
            ))
            
        except Exception as e:
            print(f"Error comparing algorithms: {str(e)}")

    def get_highest_rated_books(self) -> List[Book]:
        """Returns all books that share the highest rating"""
        if not self.books:
            return []
        
        highest_rating = max(book.rating for book in self.books)
        highest_rated_books = [book for book in self.books if book.rating == highest_rating]
        return highest_rated_books

    def sort_books(self, strategy: SortStrategy) -> List[Book]:
        """Polymorphic method to sort books using different strategies"""
        try:
            if not self.books:
                print("No books to sort.")
                return []
            return strategy.sort(self.books)
        except Exception as e:
            print(f"Error sorting books: {str(e)}")
            return self.books  # Return unsorted list in case of error

#=============================================================================
# User Interface
#=============================================================================

class BookUI(LibraryItem):
    """Handles user interface and input/output operations for the library system."""
    
    # Predefined genres for college library categorization
    valid_genres = [
        "Academic",      # For textbooks and academic publications
        "Fiction",       # For novels and fictional works
        "Non-Fiction",   # For biographies, essays, and other non-fiction works
        "Science"        # For scientific publications and research papers
    ]

    def __init__(self, inventory: BookInventory, analytics: BookAnalytics):
        super().__init__("Library Interface")
        self.inventory = inventory
        self.analytics = analytics

    def print_formatted_separator(self, message: str = ""):
        """Wrapper for the global print_formatted_separator function."""
        print_formatted_separator(message)

    def add_book_ui(self):
        """Handles the book addition interface with input validation.
        
        Collects and validates all necessary book information:
        - Title and author (non-empty strings)
        - Genre (from predefined list)
        - Year (1500-current)
        - Rating (1-5)
        - Availability and quantity
        """
        try:
            self.print_formatted_separator("Enter the details of the book that you want to add.")
            
            title = input("Title: ").strip()
            author = input("Author's name: ").strip()
            
            # Display genre selection menu
            print("\nAvailable Genres:")
            for i, genre in enumerate(self.valid_genres, 1):
                print(f"{i}. {genre}")
            
            # Validate genre selection
            while True:
                try:
                    genre_choice = int(input("\nSelect genre number: "))
                    if 1 <= genre_choice <= len(self.valid_genres):
                        genre = self.valid_genres[genre_choice - 1]
                        break
                    print(f"Please enter a number between 1 and {len(self.valid_genres)}")
                except ValueError:
                    print("Please enter a valid number")

            current_year = datetime.now().year
            while True:
                try:
                    year = int(input(f"Year of publication (1500-{current_year}): ").strip())
                    if 1500 <= year <= current_year:
                        break
                    print(f"Please enter a year between 1500 and {current_year}.")
                except ValueError:
                    print("Please enter a valid number for year.")

            while True:
                try:
                    rating = float(input("Rating (between 1 to 5, e.g. 4.6): ").strip())
                    if 1 <= rating <= 5:
                        break
                    print("Rating must be between 1 and 5.")
                except ValueError:
                    print("Please enter a valid number for rating.")

            while True:
                availability_input = input("Is any physical copy available? (yes/no): ").strip().lower()
                if availability_input in ['yes', 'no']:
                    break
                print("Please enter 'yes' or 'no'.")

            quantity = 0
            if availability_input == 'yes':
                while True:
                    try:
                        quantity = int(input("How many copies are available: ").strip())
                        if quantity >= 0:
                            break
                        print("Quantity cannot be negative.")
                    except ValueError:
                        print("Please enter a valid number for quantity.")

            book = Book(title, author, genre, year, rating, availability_input == 'yes', quantity)
            self.inventory.add_book(book)
            self.print_formatted_separator("Book successfully added!")
        except Exception as e:
            print(f"Could not add book: {str(e)}")

    def display_all_books(self):
        """Displays the complete library inventory in a formatted list.
        Shows each book's details including title, author, genre, rating, and availability.
        """
        if not self.inventory.books:
            self.print_formatted_separator("No books in the library yet.")
            return
    
        self.print_formatted_separator("Complete Book Inventory")
        for idx, book in enumerate(self.inventory.books, 1):
            print(f"{idx}. {str(book)}")
        self.print_formatted_separator()

    def view_book_history(self):
        try:
            title = input("\nEnter the title of the book to view history: ").strip()
            if not title:
                self.print_formatted_separator("Title cannot be empty.")
                return

            book = self.inventory.find_book_by_title(title)
            if book:
                history = book.get_history()
                if not history:
                    self.print_formatted_separator("No history available for this book.")
                    return
                    
                self.print_formatted_separator(f"History for '{book.title}'")
                for timestamp, action, details in history:
                    print(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {action}: {details}")
                self.print_formatted_separator()
            else:
                self.print_formatted_separator(f"Book titled '{title}' not found in the library.")
        except Exception as e:
            print(f"Error viewing history: {str(e)}")

    def update_book_quantity(self):
        title = input("\nEnter the title of the book to update quantity: ").strip()
        book = self.inventory.find_book_by_title(title)
        
        if book:
            self.print_formatted_separator(f"Update Quantity for '{book.title}'")
            print(f"Current quantity: {book.quantity}")
            while True:
                try:
                    new_quantity = int(input("Enter new quantity: ").strip())
                    if new_quantity >= 0:
                        book.update_quantity(new_quantity)
                        self.print_formatted_separator("Quantity updated successfully!")
                        break
                    print("Quantity must be 0 or positive.")
                except ValueError:
                    print("Invalid quantity. Please enter a whole number.")
        else:
            self.print_formatted_separator(f"Book titled '{title}' not found in the library.")

    def display_sorted_books(self):
        try:
            if not self.inventory.books:
                self.print_formatted_separator("No books in the library yet.")
                return

            self.print_formatted_separator("Sort Books By")
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
                    print("Please enter a valid number.")

            if choice == 1:
                sorted_books = self.analytics.sort_books(self.analytics.rating_sort)
                self.print_formatted_separator("Books Sorted by Rating (Highest to Lowest)")
            elif choice == 2:
                sorted_books = self.analytics.sort_books(self.analytics.title_sort)
                self.print_formatted_separator("Books Sorted by Title (A to Z)")
            else:
                sorted_books = self.analytics.sort_books(self.analytics.year_sort)
                self.print_formatted_separator("Books Sorted by Year (Newest to Oldest)")

            if sorted_books:
                for idx, book in enumerate(sorted_books, 1):
                    print(f"{idx}. {str(book)}")
            self.print_formatted_separator()
        except Exception as e:
            print(f"Error sorting books: {str(e)}")

    def custom_search_ui(self):
        """Provides an advanced search interface using binary search algorithm.
        
        Allows users to search books by:
        - Specific rating value
        - Minimum publication year
        Results are displayed in a formatted list.
        """
        self.print_formatted_separator("Custom Binary Search")

        while True:
            try:
                target_rating = float(input("Enter the rating to search for (1-5): "))
                if 1 <= target_rating <= 5:
                    break
                print("Rating must be between 1 and 5.")
            except ValueError:
                print("Please enter a valid number.")

        while True:
            try:
                target_year = int(input("Enter the minimum year to search for: "))
                if 1000 <= target_year <= 2024:
                    break
                print("Year must be between 1000 and 2024.")
            except ValueError:
                print("Please enter a valid year.")

        results = self.inventory.custom_binary_search(target_rating, target_year)

        if results:
            self.print_formatted_separator(f"Found {len(results)} Book(s) Matching Criteria")
            print(f"Rating: {target_rating}, Year >= {target_year}")
            for idx, book in enumerate(results, 1):
                print(f"{idx}. {str(book)}")
        else:
            self.print_formatted_separator("No books found matching your criteria.")

    def practical_search_ui(self):
        """Handles advanced library search with genre, student-friendly, and access type criteria."""
        try:
            self.print_formatted_separator("Advanced Library Search")
            
            if not self.inventory.books:
                self.print_formatted_separator("Library is empty. No books to search.")
                return
                
            # Display available genres
            print("\nAvailable Genres:")
            for i, genre in enumerate(self.valid_genres, 1):
                print(f"{i}. {genre}")
            
            # Genre selection with validation
            while True:
                try:
                    genre_choice = int(input("\nSelect genre number: "))
                    if 1 <= genre_choice <= len(self.valid_genres):
                        genre = self.valid_genres[genre_choice - 1]
                        break
                    print(f"Please enter a number between 1 and {len(self.valid_genres)}")
                except ValueError:
                    print("Please enter a valid number")

            while True:
                student_input = input("Looking for student-friendly materials? (yes/no): ").strip().lower()
                if student_input in ['yes', 'no']:
                    break
                print("Please enter 'yes' or 'no'.")

            while True:
                try:
                    print("\nSelect access type needed:")
                    print("1. Borrowing (can check out)")
                    print("2. Reference (in-library use only)")
                    print("3. Any (either borrowing or reference)")
                    
                    access_choice = int(input("Enter choice (1-3): "))
                    if 1 <= access_choice <= 3:
                        break
                    print("Please enter a number between 1 and 3.")
                except ValueError:
                    print("Please enter a valid number.")

            borrowing_type = {1: 'borrow', 2: 'reference', 3: 'any'}[access_choice]
            results = self.inventory.practical_truth_table_search(genre, student_input == 'yes', borrowing_type)

            if results:
                self.print_formatted_separator(f"Found {len(results)} Matching Book(s)")
                for idx, (book, is_borrowable, is_reference) in enumerate(results, 1):
                    print(f"\n{idx}. {str(book)}")
                    print(f"   Access type: {'Can be borrowed' if is_borrowable else 'Reference only'}")
                self.print_formatted_separator()
            else:
                self.print_formatted_separator("No books found matching your criteria.")
        except Exception as e:
            print(f"Error during search: {str(e)}")

    def lend_book_ui(self):
        """Manages the book lending process.
        
        Validates book availability and updates:
        - Book quantity
        - Availability status
        - Lending history
        """
        self.print_formatted_separator("Lend a Book")
        title = input("Enter the title of the book to lend: ").strip()
        book = self.inventory.find_book_by_title(title)
        
        if book:
            if book.lend():
                self.print_formatted_separator(f"Successfully lent out: {book.title}")
            else:
                self.print_formatted_separator(f"Cannot lend: {book.title} - No copies available")
        else:
            self.print_formatted_separator(f"Book not found: {title}")

    def return_book_ui(self):
        """Manages the book return process.
        
        Updates:
        - Book quantity
        - Availability status
        - Return history
        """
        self.print_formatted_separator("Return a Book")
        title = input("Enter the title of the book to return: ").strip()
        book = self.inventory.find_book_by_title(title)
        
        if book:
            if book.return_book():
                self.print_formatted_separator(f"Successfully returned: {book.title}")
            else:
                self.print_formatted_separator(f"Error returning: {book.title}")
        else:
            self.print_formatted_separator(f"Book not found: {title}")

    def remove_book_ui(self):
        """UI for removing a book from the library"""
        try:
            self.print_formatted_separator("Remove Book from Library")
            
            if not self.inventory.books:
                self.print_formatted_separator("Library is empty. No books to remove.")
                return
                
            title = input("Enter the title of the book to remove: ").strip()
            if not title:
                self.print_formatted_separator("Title cannot be empty.")
                return
                
            confirm = input(f"Are you sure you want to remove this book? (yes/no): ").strip().lower()
            if confirm != 'yes':
                self.print_formatted_separator("Book removal cancelled.")
                return
                
            if self.inventory.remove_book(title):
                self.print_formatted_separator(f"Book '{title}' successfully removed!")
            else:
                self.print_formatted_separator(f"Book titled '{title}' not found in the library.")
        except Exception as e:
            print(f"Error removing book: {str(e)}")

    def run_library_system(self):
        """Main entry point for the library management system."""
        try:
            print("\nWelcome to Library Management System!")

            while True:
                try:
                    print("\nPlease select an option:")
                    print("1.  Add New Book to Library")
                    print("2.  View Complete Book Inventory")
                    print("3.  Find Top-Rated Books")
                    print("4.  Track Book History & Activities")
                    print("5.  Update Available Book Copies")
                    print("6.  Sort Books by Rating/Title/Year")
                    print("7.  Search Books by Rating and Year")
                    print("8.  Advanced Library Search (Genre/Student/Access)")
                    print("9.  Lend Book to Reader")
                    print("10. Process Book Return")
                    print("11. Compare Sorting Speed (Performance Test)")
                    print("12. Remove Book from Library")
                    print("13. Exit System")

                    while True:
                        try:
                            option = int(input("\nEnter option number (1-13): "))
                            if 1 <= option <= 13:
                                break
                            print("Please enter a number between 1 and 13.")
                        except ValueError:
                            print("Please enter a valid number.")

                    if option == 13:
                        print("\nThank you for using the Library Management System!")
                        break

                    if option == 1:
                        self.add_book_ui()
                    elif option == 2:
                        self.display_all_books()
                    elif option == 3:
                        highest_rated_books = self.analytics.get_highest_rated_books()
                        if highest_rated_books:
                            self.print_formatted_separator(f"Highest Rated Books (Rating: {highest_rated_books[0].rating}/5.0):")
                            for idx, book in enumerate(highest_rated_books, 1):
                                print(f"{idx}. {book.title} by {book.author}")
                        else:
                            self.print_formatted_separator("No books available in the library.")
                    elif option == 4:
                        self.view_book_history()
                    elif option == 5:
                        self.update_book_quantity()
                    elif option == 6:
                        self.display_sorted_books()
                    elif option == 7:
                        self.custom_search_ui()
                    elif option == 8:
                        self.practical_search_ui()
                    elif option == 9:
                        self.lend_book_ui()
                    elif option == 10:
                        self.return_book_ui()
                    elif option == 11:
                        self.analytics.compare_sorting_algorithms()
                    elif option == 12:
                        self.remove_book_ui()

                    print("\nPress Enter to return to main menu...")
                    input()

                except Exception as e:
                    print(f"\nAn error occurred: {str(e)}")
                    print("Please try again.")
                    print("\nPress Enter to continue...")
                    input()

        except Exception as e:
            print("\nCritical error in Library System:")
            print(str(e))
            print("\nPlease restart the application.")
            return

#=============================================================================
# Main Entry Point
#=============================================================================

if __name__ == "__main__":
    inventory = BookInventory()
    analytics = BookAnalytics(inventory.books)
    ui = BookUI(inventory, analytics)
    ui.run_library_system()
