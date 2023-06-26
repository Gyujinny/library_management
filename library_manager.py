import logging
import re
import sys
from dataclasses import dataclass
from typing import List

import unidecode as unidecode

logger = logging.getLogger(__name__)

sys.setrecursionlimit(3)


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


def _clean_input(input_str: str) -> str:
    """
    Clean input string.
    """
    return unidecode.unidecode(re.sub('[.,();]:', '', input_str.lower().rstrip()))


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

    def search_book(self, book_info: dict) -> Book:
        """
        Search a book by title.

        :param book_info: A dictionary of book information.{id: int, title: str, author: str, isbn_no: str}
        """
        try:
            # TODO: Add more search options. now checking only one field that is available in book_info by priority.
            for book in self._books:
                if book_info['id'] == book.id:
                    return book
                elif book_info['isbn_no'] == book.isbn_no:
                    return book
                # ToDO: Add more search options.
                elif _clean_input(book_info['author']) in _clean_input(book.author):
                    return book
                # ToDO: Add more search options.
                elif _clean_input(book_info['title']) in _clean_input(book.title):
                    return book

        except Exception as e:
            logger.error(e, 'Please try again with different input.')

        return logger.error(e, 'Book not found. Please try again with different input.')


class LibraryManager:
    """
    A Library Management System that includes Library, Book, and Members.
    """

    def __init__(self) -> None:
        """
        Initialize a library management system.
        """
        self.library = Library()
        self.command_dict = {
            '1': 'Add a book',
            '2': 'Remove a book',
            '3': 'Add a member',
            '4': 'Remove a member',
            '5': 'Lend a book',
            '6': 'Return a book',
            '7': 'Search a book',
            '8': 'Search a member'}

    def get_command(self) -> None:
        """
        Get a command from the user.
        """
        try:
            while True:
                self.get_command()
                command = input('Enter a command: ')
                if command == '1':
                    book_info = self._get_book_info()
                    book = Book(**book_info)
                    self.library.add_book(book)
                elif command == '2':
                    book_info = self._get_book_info()
                    book = self.library.search_book(book_info)
                    if book is None:
                        self.interface()
                    self.library.remove_book(book)
                elif command == '3':
                    member_info = self._get_member_info()
                    member = Members(**member_info)
                    self.library.add_member(member)
                elif command == '4':
                    member_info = self._get_member_info()
                    member = self.library.search_member(member_info)
                    self.library.remove_member(member)
                elif command == '5':
                    member_info = self._get_member_info()
                    member = self.library.search_member(member_info)
                    book_info = self._get_book_info()
                    book = self.library.search_book(book_info)
                    self.library.lend_book(member, book)
                elif command == '6':
                    member_info = self._get_member_info()
                    member = self.library.search_member(member_info)
                    book_info = self._get_book_info()
                    book = self.library.search_book(book_info)
                    self.library.return_book(member, book)
                elif command == '7':
                    break
                else:
                    print('Invalid command.')
        except Exception as e:
            logger.error(e)
            self.interface()

    def interface(self) -> None:
        """
        An interface for the Library Management System.
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
        self.get_command()

    def _get_book_info(self, command_number: int) -> dict:
        """
        Get book information from the user.
        """

        print(f"""In order to do {self.command_dict[command_number]},
        the book info is necessary. Please enter book information:""")

        try:
            book_info = {}
            book_info['id'] = int(input('Enter book id: '))
            book_info['title'] = input('Enter book title: ')
            book_info['author'] = input('Enter book author: ')
            book_info['isbn_no'] = input('Enter book isbn_no: ')
            return book_info

        except Exception as e:
            logger.error(e)
            print("""Book information in invalid. Please select an option:
                    1. Go back to the main menu
                    2. Try again""")
            option = input('Enter an option: ')
            if option == '1':
                self.interface()
            elif option == '2':
                print('Please try again with different input.')
                self._get_book_info(command_number)
            else:
                print('Invalid option. Going back to the main menu.')
                self.interface()

    def _get_member_info(self, command_number: int) -> dict:
        """
        Get member information from the user.
        """
        print(f"""In order to do {self.command_dict[command_number]},
                the book info is necessary. Please enter book information:""")

        try:
            member_info = {}
            member_info['id'] = int(input('Enter member id: '))
            member_info['name'] = input('Enter member name: ')
            member_info['phone'] = input('Enter member phone: ')
            return member_info
        except Exception as e:
            logger.error(e)
            print("""Member information in invalid. Please select an option:
                1. Go back to the main menu
                2. Try again""")
            option = input('Enter an option: ')
            if option == '1':
                self.interface()
            elif option == '2':
                print('Please try again with different input.')
                self._get_member_info(command_number)
            else:
                print('Invalid option. Going back to the main menu.')
                self.interface()


def main() -> None:
    """
    A main function of a Library Management System that includes Library, Book, and Members.
    """

    logger.info('Starting library management system...')
    library_manager = LibraryManager()
    library_manager.interface()


if __name__ == '__main__':
    main()
