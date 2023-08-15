import asyncio
import json
from typing import Callable

from rich.json import JSON
from textual import on
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, VerticalScroll
from textual.widgets import ContentSwitcher, Button, Footer, Header, Input, Static, Label, TextLog

from library_manager import LibraryManager, Book

lm = LibraryManager()

BOOK_EXAMPLE = """
{"id": Book ID Number, "title": "Sample Title", "author": "Author Name", "isbn_no": "ISBN Number"}
"""

MEMBER_EXAMPLE = """
{"id": Member ID Number, "name": Name, "phone": Phone Number}
"""

MEMBER_BOOK_EXAMPLE = MEMBER_EXAMPLE + ",  " + BOOK_EXAMPLE

TEXT = f"""
    Please enter the details in the following format:
    """


###############
#   Widgets   #
###############


class BookManagerBaseClass(Static):
    """
    A Base class for the Book Manager.
    """

    def compose(self) -> ComposeResult:
        """A method to compose a screen of a library."""
        yield Header(name="Library Manager")
        yield Label(TEXT + BOOK_EXAMPLE)
        yield Input(placeholder="Please enter the details here")
        yield Button("Submit the details")

    def accepts_book(self, function: Callable, msg: str) -> None:
        """ A function to handle the event when the user presses the enter key or button."""
        input = self.query_one(Input)
        data = input.value
        self.mount(Label(data))
        if not data:
            self.mount(Label("Please enter the details"))
            return
        try:
            book = Book(**json.loads(data))
            function(book)
            self.mount(Label(msg))
        except ValueError as e:
            self.mount(Label(str(e)))
        input.value = ""


class AddBookManagerBaseClass(BookManagerBaseClass):
    """
    A widget to add a book to the library.
    """

    @on(Input.Submitted)
    @on(Button.Pressed)
    def accepts_add_book(self) -> None:
        """ A method to handle the event when the user presses the enter key."""
        self.accepts_book(lm.library.add_book, "Book added successfully")


class RemoveBookManagerBaseClass(BookManagerBaseClass):
    """
    A widget to remove a book from the library.
    """

    @on(Input.Submitted)
    @on(Button.Pressed)
    def accepts_add_book(self) -> None:
        """ A method to handle the event when the user presses the enter key."""
        self.accepts_book(lm.library.remove_book, "Book removed successfully")


class MemberManagerBaseClass(Static):
    """
    A Base class for the Member Manager.
    """

    def compose(self) -> ComposeResult:
        """A method to compose a screen of a library."""
        yield Header(name="Library Manager")
        yield Label(TEXT + MEMBER_EXAMPLE)
        yield Input(placeholder="Please enter the details here")
        yield Button("Submit the details")

    def accepts_member(self, function: Callable, msg: str) -> None:
        """ A method to handle the event when the user presses the enter key."""
        input = self.query_one(Input)
        data = input.value
        self.mount(Label(data))
        if not data:
            self.mount(Label("Please enter the details"))
            return
        try:
            member = Book(**json.loads(data))
            function(member)
            self.mount(Label(msg))
        except ValueError as e:
            self.mount(Label(str(e)))
        input.value = ""


class AddMemberManagerBaseClass(MemberManagerBaseClass):
    """
    A widget to add a member to the library.
    """

    @on(Input.Submitted)
    @on(Button.Pressed)
    def accepts_add_member(self) -> None:
        """ A method to handle the event when the user presses the enter key."""
        self.accepts_member(lm.library.add_member, "Member added successfully")


class RemoveMemberManagerBaseClass(MemberManagerBaseClass):
    """
    A widget to remove a member from the library.
    """

    @on(Input.Submitted)
    @on(Button.Pressed)
    def accepts_remove_member(self) -> None:
        """ A method to handle the event when the user presses the enter key."""
        self.accepts_member(lm.library.remove_member, "Member removed successfully")


class LibrarianBaseClass(Static):
    """
    A Base class for the Librarian.
    """

    def compose(self) -> ComposeResult:
        """A method to compose a screen of a library."""
        yield Header(name="Librarian")
        yield Label(TEXT + MEMBER_BOOK_EXAMPLE)
        yield Input(placeholder="Please enter the details here")
        yield Button("Submit the details")

    def accepts_member_book(self, function: Callable, msg: str) -> None:
        input = self.query_one(Input)
        data = input.value
        self.mount(Label(data))
        if not data:
            self.mount(Label("Please enter the details"))
            return
        try:
            data = Book(**json.loads(data))
            member = data[0]
            book = data[1]
            function(member, book)
            self.mount(Label(msg))
        except ValueError as e:
            self.mount(Label(str(e)))
        input.value = ""


class LendBook(LibrarianBaseClass):
    """
    A widget to lend a book to a member.
    """

    @on(Input.Submitted)
    @on(Button.Pressed)
    def accepts_lend_book(self) -> None:
        """ A method to handle the event when the user presses the enter key."""
        self.accepts_member_book(lm.library.lend_book, "Book lent successfully")


class ReturnBook(LibrarianBaseClass):
    """
    A widget to return a book to the library.
    """

    @on(Input.Submitted)
    @on(Button.Pressed)
    def accepts_add_member(self) -> None:
        """ A method to handle the event when the user presses the enter key."""
        self.accepts_member_book(lm.library.return_book, "Book returned successfully")


###############
#     Log     #
###############
class Screen(Static):
    """
    A class to represent the screen of a library. Disabled for now.
    """
    TITLE = "Screen"
    SUB_TITLE = "Please enter details here"

    def compose(self) -> ComposeResult:
        """A method to compose a screen of a library."""
        yield Header(name="Library Manager")
        yield Input(placeholder="Please enter Book Id", id="book_id")
        yield Input(placeholder="Please enter Book title", id="book_title")
        yield Input(placeholder="Please enter Book author", id="book_author")
        yield Input(placeholder="Please enter Book isbn_no", id="book_isbn_no")

    async def on_input_changed(self, message: Input.Changed) -> None:
        """A coroutine to handle a text changed message."""
        if message.value:
            # Look up the word in the background
            asyncio.create_task(self.lookup_word(message.value))
        else:
            # Clear the results
            self.query_one("#results", Static).update()

    async def lookup_word(self, word: str) -> None:
        """Looks up a word."""

        # if word == self.query_one(Input).value:
        self.query_one("#results", Static).update(JSON(word))


class LogWidget(Static):
    """
    A widget to represent a terminal widget."""

    def compose(self) -> ComposeResult:
        """A method to compose a log widget."""
        yield TextLog()

    def on_ready(self) -> None:
        log = self.query_one(TextLog)
        log.write_line("Log widget ready")


###############
#     Menu    #
###############
class LibraryMenu(Static):
    """
    A Widget to represent the menu of a library.
    """

    def compose(self) -> ComposeResult:
        """A method to compose the status of a library."""
        yield Button("1. Add a book", variant="primary", id="add_book")
        yield Button("2. Remove a book", variant="error", id="remove_book")
        yield Button("3. Add a member", variant="primary", id="add_member")
        yield Button("4. Remove a member", variant="error", id="remove_member")
        yield Button("5. Lend a book", variant="primary", id="lend_book")
        yield Button("6. Return a book", variant="error", id="return_book")
        yield Button("Log", id="log")


###############
#     APP     #
###############
class LibraryApp(App):
    """The main Textual app to manage library."""

    BINDINGS = [
        ("q", "exit", "Exit"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ("1", "add_book", "Add book"),
        ("2", "remove_book", "Remove book"),
        ("3", "add_memer", "Add member"),
        ("4", "remove_member", "Remove member"),
        ("5", "lend_book", "Lend book"),
        ("6", "return_book", "Return book"),
    ]

    CSS_PATH = "library_textual.css"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

        # Menu
        with ScrollableContainer(id="menu_container"):
            yield LibraryMenu("Library Menu", classes="box")

        # Widgets for each menu item
        with ContentSwitcher(initial="log"):
            yield LogWidget("Log", classes="box", id="log")
            with VerticalScroll(id="add_book"):
                yield AddBookManagerBaseClass("Add Book", classes="box")
            with VerticalScroll(id="remove_book"):
                yield RemoveBookManagerBaseClass("Remove Book", classes="box")
            with VerticalScroll(id="add_member"):
                yield AddMemberManagerBaseClass("Add Member", classes="box")
            with VerticalScroll(id="remove_member"):
                yield RemoveMemberManagerBaseClass("Remove Member", classes="box")
            with VerticalScroll(id="lend_book"):
                yield LendBook("Lend Book", classes="box")
            with VerticalScroll(id="return_book"):
                yield ReturnBook("Return Book", classes="box")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """A method to handle the event when a button is pressed."""
        self.query_one(ContentSwitcher).current = event.button.id

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_add_book(self) -> None:
        """An action to add a book."""
        pass

    def action_remove_book(self) -> None:
        """An action to remove a book."""
        pass

    def action_add_member(self) -> None:
        """An action to add a member."""
        pass

    def action_remove_member(self) -> None:
        """An action to remove a member."""
        pass

    def action_lend_book(self) -> None:
        """An action to lend a book."""
        pass

    def action_return_book(self) -> None:
        """An action to return a book."""
        pass

    def action_exit(self) -> None:
        """An action to exit the app."""
        self.exit()


if __name__ == "__main__":
    lm = LibraryManager()
    app = LibraryApp()
    app.run()
