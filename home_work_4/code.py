from pydantic import BaseModel, EmailStr, field_validator

# 1.

class Book(BaseModel):
    title: str
    author: str
    year: int
    available: bool
    categories: list[str]

    @field_validator('categories')
    def unique_categories(cls, categories: list[str]) -> list[str]:
        if len(categories) != len(set(categories)):
            raise ValueError("categories must be unique")
        return categories

class User(BaseModel):
    name: str
    email: EmailStr
    membership_id: str

# book1 = Book(
#     title="The Great Gatsby",
#     author="F. Scott Fitzgerald",
#     year=1925,
#     available=True,
#     categories=["Fiction", "Classic"],
# )

# 2.

books: list[Book] = []

def add_book(book: Book) -> None:
    books.append(book)

def find_book(title: str) -> Book | None:
    for book in books:
        if book.title == title:
            return book
    return None

def is_book_borrow(book: Book) -> None:
    """Borrows a book"""
    if not book.available:
        raise BookNotAvailable("book is not available")

    book.available = False

def return_book(book: Book) -> None:
    book.available = True

# 3.

class Library(BaseModel):
    books: list[Book] = []
    users: list[User] = []

    def total_books(self) -> int:
        return len(self.books)

# library = Library(
#     books=[book1],
#     users=[User(
#         name="John Doe",
#         email="john.doe@example.com",
#         membership_id="1234567890",
#     )],
# )

# print("total books:", library.total_books())

# 4.

class BookNotAvailable(Exception):
    pass

# add_book(book1)
# is_book_borrow(book1)
# return_book(book1)
# print(find_book("The Great Gatsby"))