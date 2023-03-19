from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Placeholder
from textual.containers import Container, Horizontal, Vertical
from bindings import bindings


class TextileApp(App):
    """A Textual app as inteface to textile."""

    CSS_PATH = "TextileApp.css"
    BINDINGS = bindings

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Vertical(
            Container(
            Placeholder("This is a custom label for p1.", id="p1"),
            Placeholder("Placeholder p2 here!", id="p2"),
            Placeholder(id="p3"),
            Placeholder(id="p4"),
            Placeholder(id="p5"),
            Placeholder(),
            Horizontal(
                     Placeholder(variant="size", id="col1"),
                     Placeholder(variant="text", id="col2"),
                     Placeholder(variant="size", id="col3"),
                     id="c1",
                 ),
                 id="bot",
             ),
             Container(
                 Placeholder(variant="text", id="left"),
                 Placeholder(variant="size", id="topright"),
                 Placeholder(variant="text", id="botright"),
                 id="top",
             ),
             id="content",
        )

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


if __name__ == "__main__":
    app = TextileApp()
    app.run()
