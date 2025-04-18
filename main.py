# Books in library stored as list

libraryBooks = []

# Function to create book (Variables and data types)

def create_book(title: str, author: str, genre: str, year: int, rating: float, availability: bool, quantity: int):
    # Book created as tuple
    book = (
        title, 
        author, 
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

    bookCreated = create_book(title, author, genre, year, rating, quantity, availability)
    
    libraryBooks.append(bookCreated)
    print("------------------------------------------------------------")
    print("Book successfully added!")
    print("------------------------------------------------------------")

def run_library_system():
    print("\nWelcome to Library Management System!")

    while True:
        add_book()

        again = input("\nWould you like to add another book? (yes/no): ").strip().lower()
        if again != 'yes':
            print("Thank you!")
            break

run_library_system()
