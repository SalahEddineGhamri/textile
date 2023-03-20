from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Placeholder, TextLog
from textual.containers import Container, Horizontal, Vertical
from rich.table import Table
from rich.syntax import Syntax

import csv
import io

from bindings import bindings

CSV = """lane,swimmer,country,time
4,Joseph Schooling,Singapore,50.39
2,Michael Phelps,United States,51.14
5,Chad le Clos,South Africa,51.14
6,László Cseh,Hungary,51.14
3,Li Zhuhao,China,51.26
8,Mehdy Metella,France,51.58
7,Tom Shields,United States,51.73
1,Aleksandr Sadovnikov,Russia,51.84"""


CODE = '''\
def loop_first_last(values: Iterable[T]) -> Iterable[tuple[bool, bool, T]]:
    """Iterate and generate a tuple with a flag for first and last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    first = True
    for value in iter_values:
        yield first, False, previous_value
        first = False
        previous_value = value
    yield first, True, previous_value\
'''


class TextileApp(App):
    """A Textual app as inteface to textile."""

    CSS_PATH = "TextileApp.css"
    BINDINGS = bindings

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield TextLog(highlight=True, markup=True, id="text")
        yield TextLog(highlight=True, markup=True, id="analysis")

    def on_ready(self) -> None:
        """Called  when the DOM is ready."""
        text_log = self.query_one("#text")
        analysis_log = self.query_one("#analysis")

        text_log.write(Syntax(CODE, "python", indent_guides=True))
        analysis_log.write(Syntax(CODE, "python", indent_guides=True))

        rows = iter(csv.reader(io.StringIO(CSV)))
        table = Table(*next(rows))
        for row in rows:
            table.add_row(*row)

        text_log.write(table)
        text_log.write("[bold magenta]Write text or any Rich renderable!")

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


if __name__ == "__main__":
    app = TextileApp()
    app.run()
