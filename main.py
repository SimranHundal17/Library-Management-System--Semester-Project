#Variables and data types

def create_book(title: str, author: str, genre: str, year: int, rating: float, quantity: int, availability: bool):
    book = (
        title, 
        author, 
        year, 
        rating, 
        quantity, 
        availability, 
        (title, author, genre, year), 
        )
    return book

book1 = create_book("Harry Potter", "J.K. Rowling", "Magic", 1997, 4.9, 10, True)

