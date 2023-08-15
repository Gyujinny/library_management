import asyncio
import json

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
    Please enter the details of the book in the following format:
    """


class BookManager(Static):

    def compose(self) -> ComposeResult:
        """A method to compose a screen of a library."""
        yield Header(name="Library Manager")
        yield Label(TEXT + BOOK_EXAMPLE)
        yield Input(placeholder="Please enter the details here")
        yield Button("Submit the details")


class AddBookManager(BookManager):
    @on(Input.Submitted)
    @on(Button.Pressed)
    def accepts_add_book(self):
        """ A method to handle the event when the user presses the enter key."""
        input = self.query_one(Input)
        data = input.value
        self.mount(Label(data))
        book = Book(**json.loads(data))
        lm.library.add_book(book)
        self.mount(Label("Book added successfully"))
        input.value = ""


class RemoveBookManager(BookManager):
    @on(Input.Submitted)
    @on(Button.Pressed)
    def accepts_remove_book(self):
        """ A method to handle the event when the user presses the enter key."""
        input = self.query_one(Input)
        data = input.value
        self.mount(Label(data))
        book = Book(**json.loads(data))
        lm.library.remove_book(book)
        self.mount(Label("Book removed successfully"))
        input.value = ""


class MemberManager(Static):

    def compose(self) -> ComposeResult:
        """A method to compose a screen of a library."""
        yield Header(name="Library Manager")
        yield Label(TEXT + MEMBER_EXAMPLE)
        yield Input(placeholder="Please enter the details here")
        yield Button("Submit the details")


class AddMemberManager(MemberManager):
    @on(Input.Submitted)
    @on(Button.Pressed)
    def accepts_add_member(self):
        """ A method to handle the event when the user presses the enter key."""
        input = self.query_one(Input)
        data = input.value
        self.mount(Label(data))
        member = Book(**json.loads(data))
        lm.library.add_meber(member)
        self.mount(Label("Member added successfully"))
        input.value = ""


class RemoveMemberManager(MemberManager):
    @on(Input.Submitted)
    @on(Button.Pressed)
    def accepts_add_member(self):
        """ A method to handle the event when the user presses the enter key."""
        input = self.query_one(Input)
        data = input.value
        self.mount(Label(data))
        member = Book(**json.loads(data))
        lm.library.remove_meber(member)
        self.mount(Label("Member removed successfully"))
        input.value = ""


class Librarian(Static):

    def compose(self) -> ComposeResult:
        """A method to compose a screen of a library."""
        yield Header(name="Librarian")
        yield Label(TEXT + MEMBER_BOOK_EXAMPLE)
        yield Input(placeholder="Please enter the details here")
        yield Button("Submit the details")

    @on(Input.Submitted, "#lend_book")
    @on(Button.Pressed, "#lend_book")
    def accepts_add_member(self):
        """ A method to handle the event when the user presses the enter key."""
        input = self.query_one(Input)
        data = input.value
        self.mount(Label(data))
        data = Book(**json.loads(data))
        member = data[0]
        book = data[1]
        lm.library.lend_book(member, book)
        self.mount(Label("Member added successfully"))
        input.value = ""

    @on(Input.Submitted, "#return_book")
    @on(Button.Pressed, "#return_book")
    def accepts_add_member(self):
        input = self.query_one(Input)
        data = input.value
        self.mount(Label(data))
        data = Book(**json.loads(data))
        member = data[0]
        book = data[1]
        lm.library.lend_book(member, book)
        self.mount(Label("Member added successfully"))
        input.value = ""


class Screen(Static):
    """A class to represent the screen of a library."""
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


class LogWidget(App):
    """A class to represent a terminal widget."""

    def compose(self) -> ComposeResult:
        """A method to compose a log widget."""
        yield TextLog()

    def on_ready(self) -> None:
        log = self.query_one(TextLog)
        log.write_line("Log widget ready")


class LibraryMenu(Static):
    """A class to represent the status of a library."""

    def compose(self):
        """A method to compose the status of a library."""
        yield Button("1. Add a book", variant="primary", id="add_book")
        yield Button("2. Remove a book", variant="error", id="remove_book")
        yield Button("3. Add a member", variant="primary", id="add_member")
        yield Button("4. Remove a member", variant="error", id="remove_member")
        yield Button("5. Lend a book", variant="primary", id="lend_book")
        yield Button("6. Return a book", variant="error", id="return_book")


class LibraryApp(App):
    """A Textual app to manage library."""

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
        with ScrollableContainer(id="menu_container"):
            yield Button("1. Add a book", variant="primary", id="add_book")
            yield Button("2. Remove a book", variant="error", id="remove_book")
            yield Button("3. Add a member", variant="primary", id="add_member")
            yield Button("4. Remove a member", variant="error", id="remove_member")
            yield Button("5. Lend a book", variant="primary", id="lend_book")
            yield Button("6. Return a book", variant="error", id="return_book")
        with ContentSwitcher(initial="screen"):
            yield Screen("Screen", classes="box", id="screen")
            with VerticalScroll(id="add_book"):
                yield AddBookManager("Add Book", classes="box")
            with VerticalScroll(id="remove_book"):
                yield RemoveBookManager("Remove Book", classes="box")
            with VerticalScroll(id="add_member"):
                yield AddMemberManager("Add Member", classes="box")
            with VerticalScroll(id="remove_member"):
                yield RemoveMemberManager("Remove Member", classes="box")
            with VerticalScroll(id="lend_book"):
                yield Librarian("Lend Book", classes="box")
            with VerticalScroll(id="return_book"):
                yield Librarian("Return Book", classes="box")

    def on_button_pressed(self, event: Button.Pressed) -> None:
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
