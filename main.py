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

# recursion used to compute total number of physical copies having the same title
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

def run_library_system():
    print("\nWelcome to Library Management System!")
    while(True):
        print("\nPlease select an option:")
        print("1. Add a new book to the library")
        print("2. View total number of available physical books")
        print("3. Compute total physical copies of a book by title")
        option = int(input("Enter 1, 2, or 3: "))

        if option == 1:
            while True:
                add_book()
                again = input("\nWould you like to add another book? (yes/no): ").strip().lower()
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
        else:
            print("Invalid option.Type 1, 2, or 3.")
        
        anotherOption = input("\nWould you like to do another task? (yes/no): ").strip().lower()
        if anotherOption != 'yes':
            print("\nThank you for using the Library Management System!")
            break

run_library_system()
