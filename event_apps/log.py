from textual.app import App, ComposeResult
from textual.widgets import Static, TextLog

TEXT = """log widget ready"""


class LogApp(Static):
    """An app with a simple log."""

    def compose(self) -> ComposeResult:
        yield TextLog()

    def on_ready(self) -> None:
        log = self.query_one(TextLog)
        log.write_line(TEXT)


if __name__ == "__main__":
    app = LogApp()
    app.run()