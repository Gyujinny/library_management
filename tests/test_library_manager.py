from faker import Faker
from unittest import TestCase

from ..library_manager import Book, Members, Library


class TestLibrary(TestCase):
    """
    Tests for the library manager.
    """

    def setUp(self):
        """
        Set up the library manager.
        """
        self.library = Library()
        self.faker = Faker()
        self.fake_book = dict(
            id=self.faker.random_int(),
            title=self.faker.sentence(),
            author=self.faker.name(),
            isbn_no=self.faker.isbn13(),
            is_available=True,
        )
        self.fake_member = dict(
            id=self.faker.random_int(),
            name=self.faker.name(),
            member_id=self.faker.random_int(),
            books_borrowed=[],
        )

    def tearDown(self):
        """
        Tear down the library manager.
        """
        self.library = None

    def test_add_book(self):
        """
        Test adding a book to the library.
        """
        book = Book(**self.fake_book)
        self.library.add_book(book)

        self.assertIn(book, self.library._books)

    def test_remove_book(self):
        """
        Test removing a book from the library.
        """
        book = Book(**self.fake_book)
        self.library.add_book(book)
        self.library.remove_book(book)

        self.assertNotIn(book, self.library._books)

    def test_add_member(self):
        """
        Test adding a member to the library.
        """
        member = Members(**self.fake_member)
        self.library.add_member(member)

        self.assertIn(member, self.library._members)

    def test_remove_member(self):
        """
        Test removing a member from the library.
        """
        member = Members(**self.fake_member)
        self.library.add_member(member)
        self.library.remove_member(member)

        self.assertNotIn(member, self.library._members)

    def test_lend_book(self):
        """
        Test lending a book to a member.
        """
        member = Members(**self.fake_member)
        book = Book(**self.fake_book)
        self.library.add_member(member)
        self.library.add_book(book)
        self.library.lend_book(member, book)

        self.assertIn(book, member.books_borrowed)
        self.assertFalse(book.is_available)

    def test_return_book(self):
        """
        Test returning a book to the library.
        """
        member = Members(**self.fake_member)
        book = Book(**self.fake_book)
        self.library.add_member(member)
        self.library.add_book(book)
        self.library.lend_book(member, book)
        self.library.return_book(member, book)

        self.assertNotIn(book, member.books_borrowed)
        self.assertTrue(book.is_available)

    def test_lend_book_fail_not_available(self):
        """
        Test lending a book to a member.
        """
        member = Members(**self.fake_member)
        book = Book(**self.fake_book)
        self.library.add_member(member)
        self.library.add_book(book)
        self.library.lend_book(member, book)

        with self.assertRaises(Exception):
            self.library.lend_book(member, book)
        self.assertFalse(book.is_available)

    def test_return_book_fail_not_lended(self):
        """
        Test returning a book that is not lended to a member.
        """
        member = Members(**self.fake_member)
        book = Book(**self.fake_book)
        self.library.add_member(member)
        self.library.add_book(book)

        with self.assertRaises(Exception):
            self.library.return_book(member, book)
