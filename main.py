from typing import List, Optional, Tuple
from datetime import datetime
from abc import ABC, abstractmethod  # Import for abstract base class

def print_formatted_separator(message: str = "") -> None:
    """Utility function for consistent formatting of section separators.
    
    Args:
        message: Optional message to display in the separator
    """
    print("\n------------------------------------------------------------")
    if message:
        print(message)
    print("------------------------------------------------------------")

def generate_test_books(size: int) -> List['Book']:
    """Generate a list of test books for performance testing.
    
    Args:
        size: Number of test books to generate
        
    Returns:
        List of Book objects with test data
    """
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

def create_bar_graph(value1: float, value2: float, label1: str = "Value 1", label2: str = "Value 2", max_width: int = 50) -> str:
    """Create a simple bar graph comparison of two values.
    
    Args:
        value1: First value to compare
        value2: Second value to compare
        label1: Label for first value
        label2: Label for second value
        max_width: Maximum width of the bar graph
        
    Returns:
        Formatted string containing the bar graph
    """
    # Calculate the bars
    max_value = max(value1, value2)
    bar1 = int((value1 / max_value) * max_width)
    bar2 = int((value2 / max_value) * max_width)
    
    # Create the visualization
    graph = f"\n{label1} ({value1:.6f}s)\n"
    graph += "█" * bar1
    graph += f"\n\n{label2} ({value2:.6f}s)\n"
    graph += "█" * bar2
    
    return graph

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

    def compare_sorting_algorithms(self):
        """Compare Bubble Sort and Merge Sort performance with bar graph"""
        print("\nSorting Algorithm Performance Analysis")
        print("-" * 50)
        
        # Test with different dataset sizes
        sizes = [100, 500, 1000, 5000]
        
        for size in sizes:
            print(f"\nTesting with {size} books:")
            print("-" * 30)
            
            # Create test books
            test_books = generate_test_books(size)
            
            # Test Bubble Sort
            bubble_books = test_books.copy()
            start_time = datetime.now()
            self.rating_sort.sort(bubble_books)
            end_time = datetime.now()
            bubble_duration = end_time - start_time
            
            # Test Merge Sort
            merge_books = test_books.copy()
            start_time = datetime.now()
            self.title_sort.sort(merge_books)
            end_time = datetime.now()
            merge_duration = end_time - start_time
            
            # Create bar graph visualization
            max_width = 50  # Maximum width of the bar
            bubble_time = bubble_duration.total_seconds()
            merge_time = merge_duration.total_seconds()
            
            # Scale bars relative to the slower algorithm
            max_time = max(bubble_time, merge_time)
            bubble_bar = int((bubble_time / max_time) * max_width)
            merge_bar = int((merge_time / max_time) * max_width)
            
            # Display results with bar graph
            print(f"\nBubble Sort ({bubble_time:.6f}s)")
            print("█" * bubble_bar)
            
            print(f"\nMerge Sort ({merge_time:.6f}s)")
            print("█" * merge_bar)
            
            print(f"\nBubble Sort is {bubble_time/merge_time:.2f}x slower")

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

    def print_formatted_separator(self, message: str = ""):
        print_formatted_separator(message)

    def add_book_ui(self):
        self.print_formatted_separator("Enter the details of the book that you want to add.")
        
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
        self.print_formatted_separator("Book successfully added!")

    def display_all_books(self):
        if not self.inventory.books:
            self.print_formatted_separator("No books in the library yet.")
            return

        self.print_formatted_separator()
        print("All Books in the Library:")
        for idx, book in enumerate(self.inventory.books, 1):
            print(f"{idx}. {str(book)}")
        print("------------------------------------------------------------")

    def view_book_history(self):
        title = input("\nEnter the title of the book to view history: ").strip()
        book = self.inventory.find_book_by_title(title)
        
        if book:
            self.print_formatted_separator(f"History for '{book.title}':")
            for timestamp, action, details in book.get_history():
                print(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {action}: {details}")
        else:
            self.print_formatted_separator(f"Book titled '{title}' not found in the library.")

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
                        self.print_formatted_separator("Quantity updated successfully!")
                        break
                    print("Quantity must be 0 or positive.")
                except ValueError:
                    print("Invalid quantity. Please enter a whole number.")
        else:
            self.print_formatted_separator(f"Book titled '{title}' not found in the library.")

    def display_sorted_books(self):
        if not self.inventory.books:
            self.print_formatted_separator("No books in the library yet.")
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
            self.print_formatted_separator("Books sorted by rating (highest to lowest):")
        elif choice == 2:
            sorted_books = self.analytics.sort_books(self.analytics.title_sort)
            self.print_formatted_separator("Books sorted by title (A to Z):")
        else:
            sorted_books = self.analytics.sort_books(self.analytics.year_sort)
            self.print_formatted_separator("Books sorted by year (newest to oldest):")

        for idx, book in enumerate(sorted_books, 1):
            print(f"{idx}. {str(book)}")
        print("------------------------------------------------------------")

    def custom_search_ui(self):
        """UI for the custom binary search feature"""
        self.print_formatted_separator("Custom Binary Search")
        
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
            self.print_formatted_separator(f"Found {len(results)} book(s) matching criteria:")
            print(f"Rating: {target_rating}, Year >= {target_year}")
            for idx, book in enumerate(results, 1):
                print(f"{idx}. {str(book)}")
        else:
            self.print_formatted_separator("No books found matching your criteria.")

    def practical_search_ui(self):
        """UI for the practical truth table-based search feature"""
        self.print_formatted_separator("Practical Library Search")
        print("This search helps find books based on practical library needs:")
        print("1. Genre matching")
        print("2. Student-friendly materials (Rating ≥ 4.0 AND Year ≥ 2000)")
        print("3. Access type (Borrowing or Reference)")
        
        # Get genre
        genre = input("\nEnter desired genre (e.g., Fiction, Non-fiction, Science, etc.): ").strip()
        
        # Get student-friendly requirement
        while True:
            student_input = input("Looking for student-friendly materials? (yes/no): ").strip().lower()
            if student_input in ['yes', 'no']:
                break
            print("Please type 'yes' or 'no'.")
        for_students = student_input == 'yes'

        # Get borrowing type requirement
        print("\nSelect access type needed:")
        print("1. Borrowing (can check out)")
        print("2. Reference (in-library use only)")
        print("3. Any (either borrowing or reference)")
        
        while True:
            try:
                access_choice = int(input("Enter choice (1-3): "))
                if 1 <= access_choice <= 3:
                    break
                print("Please enter a number between 1 and 3.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        borrowing_type = {1: 'borrow', 2: 'reference', 3: 'any'}[access_choice]

        # Perform search
        results = self.inventory.practical_truth_table_search(genre, for_students, borrowing_type)

        # Display results with practical information
        if results:
            self.print_formatted_separator(f"Found {len(results)} book(s) matching your needs:")
            print(f"\nSearch Criteria:")
            print(f"- Genre: {genre}")
            print(f"- Student-friendly: {'Yes' if for_students else 'Not required'}")
            print(f"- Access type: {borrowing_type.capitalize()}")
            print("\nMatching Books:")
            for idx, (book, is_borrowable, is_reference) in enumerate(results, 1):
                print(f"\n{idx}. {str(book)}")
                # Show practical status
                print(f"   Student-friendly: {'Yes' if book.rating >= 4.0 and book.year >= 2000 else 'No'}")
                print(f"   Access type: {'Can be borrowed' if is_borrowable else 'Reference only'}")
        else:
            self.print_formatted_separator("No books found matching your criteria.")
            print("\nSuggestions:")
            print("- Try a different genre")
            print("- If searching for student materials, consider allowing older books")
            print("- Try changing the access type to 'Any' for more results")

    def lend_book_ui(self):
        """UI for lending books"""
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
        """UI for returning books"""
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
            print("8. Practical library search")
            print("9. Lend a book")
            print("10. Return a book")
            print("11. Compare sorting algorithms")

            while True:
                try:
                    option = int(input("\nEnter 1 to 11: "))
                    if 1 <= option <= 11:
                        break
                    print("Please enter a number between 1 and 11.")
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
