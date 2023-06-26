from dataclasses import dataclass


@dataclass
class Book:
    """
    A Book class that includes a title, author, and ISBN number.

    :cvar id: A unique id for a book.
    :cvar title: A title for a book.
    :cvar author: An author for a book.
    :cvar isbn_no: An ISBN number for a book.
    """

    id: int
    title: str
    author: str
    isbn_no: str
    is_available: bool = True
