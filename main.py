# Books in library stored as list

libraryBooks = []

# Function to create book (Variables and data types)

def create_book(title: str, author: str, genre: str, year: int, rating: float, availability: bool, quantity: int):
    # Information of book stored as tuple
    book = (
        title, 
        author,
        genre, 
        year, 
        rating, 
        availability,
        quantity, 
        (title, author, genre, year), 
        )
    return book

# Taking input from librarian for creating books to be added to library (Input)

def add_book():
    print("\n------------------------------------------------------------")
    print("Enter the details of the book that you want to add.")
    print("------------------------------------------------------------")
    title = input("Title: ").strip()
    author = input("Author's name: ").strip()
    genre = input("Genre: ").strip()

    while True:
        try:
            year = int(input("Year of publication: ").strip())
            if year <= 2025:
                break
            else:
                print("Enter valid year.")
        except ValueError:
            print("Invalid year. Please enter a valid integer.")

    while True:
        try:
            rating = float(input("Rating (between 1 to 5, e.g. 4.6): ").strip())
            if 1.0 <= rating and rating <= 5.0:
                break
            else:
                print("Rating must be between 1 and 5.")
        except ValueError:
            print("Invalid rating. Please enter a decimal number like 4.6.")

    while True:
        availability_input = input("Is any physical copy available in the library? (yes/no): ").strip().lower()
        if availability_input in ['yes', 'no']:
            break
        else:
            print("Please type 'yes' or 'no'.")

    if availability_input == 'yes':
        availability = True

        while True:
            try:
                quantity = int(input("How many copies are available: ").strip())
                break
            except ValueError:
                print("Invalid quantity. Please enter a whole number.")
    else:
        availability = False
        quantity = 0

    bookCreated = create_book(title, author, genre, year, rating, availability, quantity)
    
    libraryBooks.append(bookCreated)
    print("------------------------------------------------------------")
    print("Book successfully added!")
    print("------------------------------------------------------------")

# for loop used to count the number of physically available books in the library
def count_of_all_physical_books():
    already_counted = set()
    count = 0

    for book in libraryBooks:
        title = book[0].lower()
        if title not in already_counted and book[5] == True:
            count += 1
            already_counted.add(title)

    return count

# Recursion used to compute total number of physical copies having the same title
def total_physical_copies_by_title(title, index=0, total=0, found=False):
    if index >= len(libraryBooks):
        print("------------------------------------------------------------")
        if found: 
            print(f"Total available physical copies of '{title}': {total}")
        else:
            print(f"Book titled '{title}' not found in the library.")
        print("------------------------------------------------------------")
        return
    
    book = libraryBooks[index]
    if book[0].lower() == title:
        found = True
        if book[5] == True:
            total += book[6]

    total_physical_copies_by_title(title, index + 1, total, found)

def display_all_books():
    if not libraryBooks:
        print("------------------------------------------------------------")
        print("No books in the library yet.")
        print("------------------------------------------------------------")
        return

    print("------------------------------------------------------------")
    print("All Books in the Library:")
    for idx, book in enumerate(libraryBooks, 1):
        print(f"{idx}. '{book[0]}' by {book[1]} ({book[3]}) | Genre: {book[2]} | Rating: {book[4]}/5 | Available: {'Yes' if book[5] else 'No'} | Copies: {book[6]}")
    print("------------------------------------------------------------")


# Class that includes internal functions to perform some library analytics
class LibraryAnalytics:
    def __init__(self, books):
        self.books = books

    def highest_rated_book(self):
        if len(self.books) == 0:
            print("------------------------------------------------------------")
            print("No books available in the library.")
            print("------------------------------------------------------------")
            return
        
        highest = self.books[0]
        for book in self.books[1:]:
            if book[4] >highest[4]:
                highest = book
        
        print("------------------------------------------------------------")
        print(f"Highest Rated Book: '{highest[0]}' with ({highest[4]}/5.0)")
        print("------------------------------------------------------------")

    def count_books_by_author(self, author_name):
        count = 0

        for book in self.books:
            if book[1].lower() == author_name.strip().lower():
                count += 1
        
        print("------------------------------------------------------------")
        print(f"Books by '{author_name}': {count}")
        print("------------------------------------------------------------")

    def count_books_by_genre(self, genre_name):
        count = 0

        for book in self.books:
            if book[2].lower() == genre_name.lower():
                count += 1

        print("------------------------------------------------------------")
        print(f"Books in genre '{genre_name}': {count}")
        print("------------------------------------------------------------")

def run_library_system():
    print("\nWelcome to Library Management System!")
    analytics = LibraryAnalytics(libraryBooks)

    while(True):
        print("\nPlease select an option:")
        print("1. Add a new book to the library")
        print("2. View total number of available physical books")
        print("3. Compute total physical copies of a book by title")
        print("4. Display all books in the library")
        print("5. Show highest rated book")
        print("6. Count books by a specific author")
        print("7. Count books from a specific genre")

        while(True):
            try:
                option = int(input("\nEnter 1 to 7: "))
                if option < 1 or option > 6:
                    print("Please enter a number between 1 and 7.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

        if option == 1:
            while True:
                add_book()
                again = input("\nWould you like to add another book? Type 'yes' to continue or any other key to exit: ").strip().lower()
                if again != 'yes':
                    print("\nThank you!")
                    break
        elif option == 2:
            print("\n------------------------------------------------------------")
            print(f"Total number of physically available books = {count_of_all_physical_books()}")
            print("------------------------------------------------------------")
        elif option == 3:
            print("\n------------------------------------------------------------")
            title = input("Enter the title: ").strip().lower()
            total_physical_copies_by_title(title)
        elif option == 4:
            display_all_books()
        elif option == 5:
            analytics.highest_rated_book()
        elif option == 6:
            print("\n------------------------------------------------------------")
            author = input("Enter author's name: ")
            analytics.count_books_by_author(author)
        elif option == 7:  
            print("\n------------------------------------------------------------") 
            genre = input("Enter the genre: ")
            analytics.count_books_by_genre(genre)         
        else:
            print("Invalid option.Type a number between 1 to 7.")
        
        anotherOption = input("\nWould you like to do another task? Type 'yes' to continue or any other key to exit: ").strip().lower()
        if anotherOption != 'yes':
            print("\nThank you for using the Library Management System!")
            break

run_library_system()
