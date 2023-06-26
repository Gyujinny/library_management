import logging
from dataclasses import dataclass
from typing import List

logger = logging.getLogger(__name__)


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


class Library:
    """
    A Library class that includes a list of books and a list of members.
    """
    _books: List[Book]
    _members: List[Members]

    def __init__(self) -> None:
        """
        Initialize a library with an empty list of books and an empty list of members.

        :cvar books: A list of books.
        :cvar members: A list of members.
        """
        self._books: List[Book] = []
        self._members: List[Members] = []

    def add_book(self, book: Book) -> None:
        """
        Add a book to the library.
        """
        self._books.append(book)

    def remove_book(self, book: Book) -> None:
        """
        Remove a book from the library.
        """
        self._books.remove(book)

    def add_member(self, member: Members) -> None:
        """
        Add a member to the library.
        """
        self._members.append(member)

    def remove_member(self, member: Members) -> None:
        """
        Remove a member from the library.
        """
        self._members.remove(member)

    def lend_book(self, member: Members, book: Book) -> None:
        """
        Lend a book to a member.
        """
        if not self._is_valid_member(member.id):
            raise Exception('Member not found.')

        if not self._is_book_available(book):
            raise Exception('Book not available.')

        member.borrow_book(book)

    def return_book(self, member: Members, book: Book) -> None:
        """
        Return a book to the library.
        """
        if not self._is_valid_member(member.id):
            raise Exception('Member not found.')

        if self._is_book_available(book):
            raise Exception('Book not borrowed.')

        member.return_book(book)

    def _is_book_available(self, book: Book) -> bool:
        """
        Check if a book is available in the library.
        """
        if book.is_available:
            return True

        return False

    def _find_member_by_id(self, member_id: int) -> Exception:
        """
        Find a member by id.
        """
        for member in self._members:
            if member_id == member.id:
                return member
        return Exception('Member not found.')

    def _is_valid_member(self, member_id: int) -> bool:
        """
        Check if a member is valid.
        """
        for member in self._members:
            if member_id == member.id:
                return True
            continue
        return False


class LibraryManager:
    """
    A Library Management System that includes Library, Book, and Members.
    """

    def __init__(self) -> None:
        pass

    def get_command(self) -> None:
        """
        Get a command from the user.
        """
        print("""
        Welcome to the Library Management System.

        Please select an option:
        1. Add a book
        2. Remove a book
        3. Add a member
        4. Remove a member
        5. Lend a book
        6. Return a book
        7. Exit
        """)


def main() -> None:
    """
    A main function of a Library Management System that includes Library, Book, and Members.
    """

    logger.info('Starting library management system...')
    library_manager = LibraryManager()
    library_manager.interface()


if __name__ == '__main__':
    main()
