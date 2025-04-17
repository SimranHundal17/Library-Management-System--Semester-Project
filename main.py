# Variables and data types

def create_book(title: str, author: str, genre: str, year: int, rating: float, availability: bool, quantity: int):
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

# Inputs

def add_book():
    print("Enter the details of the book that you want to add.")
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

    book1 = create_book(title, author, genre, year, rating, quantity, availability)
    print("\n Book successfully created!")

    return book1

add_book()

