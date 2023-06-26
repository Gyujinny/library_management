from dataclasses import dataclass
from typing import List

from book import Book

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



@dataclass
class Members:
    """
    A Members class that includes a list of books borrowed.

    :cvar id: A unique id for a member.
    :cvar name: A name for a member.
    :cvar member_id: A unique id for a member.
    :cvar books_borrowed: A list of books borrowed.
    """
    id: int
    name: str
    member_id: int
    books_borrowed: List[Book]

    def borrow_book(self, book: Book) -> None:
        """
        Borrow a book.
        """
        book.is_available = False
        self.books_borrowed.append(book)

    def return_book(self, book: Book) -> None:
        """
        Return a book.
        """
        book.is_available = True
        self.books_borrowed.remove(book)
